from django.shortcuts import render
import xlwings as xw
import pandas as pd
import plotly.express as px
import time
from pywintypes import com_error  # To catch RPC errors

def home(request):
    import requests
    import json

    file_path = "SMIF Portfolio Tracker.xlsx"
    max_retries = 10
    retry_delay = 2  #Set to 2 for stability, try reducing later

    def get_cell_value(sheet, cell): #Gets a single cell value from an Excel sheet. Takes the excel sheet object and a single cell as parameters.
        if sheet is None:
            print("Error: The sheet does not exist or Excel connection is lost.")
            return None
        try:
            value = sheet[cell].value
            return value if value is not None else None
        except Exception as e:
            print(f"Error retrieving value from {cell}: {e}")
            return None

    def get_range_values(sheet, cell_range): #Gets a range of values as a DataFrame from an Excel sheet. Takes the excel sheet object and cell_range (ex. 'B5:H100') as parameters.
        if sheet is None:
            print("Error: The sheet does not exist or Excel connection is lost.")
            return pd.DataFrame()
        try:
            data = sheet.range(cell_range).options(pd.DataFrame, header=1, index=False).value
            if data is None or data.empty:
                return pd.DataFrame()
            return data.dropna(how='any')
        except Exception as e:
            print(f"Error retrieving values from {cell_range}: {e}")
            return pd.DataFrame()

    for attempt in range(1, max_retries + 1): #Loop to attempt to retrieve data multiple times
        try:
            app = xw.App(visible=False) #Reinitialize Excel instance on each retry
            wb = app.books.open(file_path) #Open the workbook/spreadsheet
            transaction_sheet = wb.sheets['Transaction'] #Select the specific sheets needed
            dashboard_sheet = wb.sheets['Dashboard']

            wb.api.RefreshAll() #Refresh all external data connections
            time.sleep(retry_delay) #Gives Excel some time to update to prevent #CONNECT! error
            app.calculate() #Ensure all formulas and links are recalculated

            smifytd = get_cell_value(dashboard_sheet, 'J7')
            spytd = get_cell_value(dashboard_sheet, 'J12')

            # Convert to percentage and round if there is a value there, otherwise return None
            smifytd = round(smifytd * 100, 2) if smifytd is not None else None
            spytd = round(spytd * 100, 2) if spytd is not None else None

            if smifytd is not None and smifytd > 10000:  #Catch integer overflows from None values being processed incorrectly
                raise ValueError(f"Unrealistic SMIF YTD: {smifytd}")
            if spytd is not None and spytd > 10000:
                raise ValueError(f"Unrealistic S&P500 YTD: {spytd}")

            portfolio_data = get_range_values(transaction_sheet, "B5:H100")

            wb.close() #Close and quit Excel to ensure full retry
            app.quit() 

            if smifytd is not None and spytd is not None and not portfolio_data.empty:
                break  #Data is valid, continue
            else:
                print(f"Attempt {attempt}/{max_retries} failed. Retrying...")
                time.sleep(retry_delay)
        except com_error as e: #Error handling for RPC errors, wait and close Excel
            print(f"RPC Error on attempt {attempt}: {e}")
            time.sleep(retry_delay)
            app.quit()  

    else:
        raise ValueError("Failed to fetch valid data after 10 retries.")

    #DataFrame for year-to-date performance
    ytd_data = { 
        "Portfolio": ["S&P500", "SMIF"],
        "Gain (%)": [spytd, smifytd],
    }
    ytd_df = pd.DataFrame(ytd_data)

    #Bar chart for portfolio YTD performance
    bar_chart = px.bar(
        ytd_df, 
        x="Portfolio", 
        y="Gain (%)", 
        title="Portfolio Performance YTD", 
        text="Gain (%)",
        color="Portfolio",
        color_discrete_map={"S&P500": "#ef553b", "SMIF": "#636efa"}
    )
    bar_chart.update_layout(width=700, height=500, bargap=0.4, showlegend=False)
    bar_chart.show()

    #Pie chart for portfolio distribution
    donut_chart = px.pie(
        portfolio_data, 
        names='Ticker', 
        values='Weight',
        custom_data=['Live Price', 'Purchase Price', 'Quantity', 'Total Value'],
        title='Portfolio Distribution',
        hole=0.5, 
    )

    donut_chart.update_traces(
        textinfo='percent+label', 
        hovertemplate="""
        <b>%{label}</b><br>
        Live Price: $%{customdata[0][0]:,.2f}<br>
        Purchase Price: $%{customdata[0][1]:,.2f}<br>
        Quantity: %{customdata[0][2]:.0f}<br>
        Total Value: $%{customdata[0][3]:,.2f}<br>
        Weight: %{percent}<extra></extra>
        """
    )
    
    donut_chart.update_layout(autosize=False, width=900, height=900, showlegend=False)
    donut_chart.show()

    return render(request, 'home.html', {'exceldata': portfolio_data})

def about(request):
    return render(request, 'about.html', {}) #Allow us to pass stuff into the webpage and use it in the HTML page in Python
