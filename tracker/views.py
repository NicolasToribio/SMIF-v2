from django.shortcuts import render
import xlwings as xw
import pandas as pd
import plotly.express as px
import time


def home(request): #Whenever someone visits our website, their browser requests our page. We pass that request into our function
    
    import requests #requests stuff from the internet
    import json #javascript object notation, default format for what most APIs return

    file_path = "SMIF Portfolio Tracker.xlsx"
    app = xw.App(visible=False)  # app gives you more control by specifying an instance of the spreadsheet, set visible=True for debugging
    wb = app.books.open(file_path)
    sheet = wb.sheets['Transaction'] #rename to transaction later
    dashsheet = wb.sheets['Dashboard']

    try:
        wb.api.RefreshAll()  # Refresh external data connections
        time.sleep(2) #Gives Excel some time to update to prevent #CONNECT! error, adjust as needed 
        app.calculate()  # Ensure formulas and links are updated

        def safe_get_value(sheet, cell): #error handling to avoid Attribute Error from #CONNECT!
            value = sheet[cell].value
            if value is None:
                return 0  # fallback value
            return value

        smifytd = safe_get_value(dashsheet, 'J7')
        smifytd = round(smifytd * 100, 2)

        spytd = safe_get_value(dashsheet, 'J12')
        spytd = round(spytd * 100, 2)

        print(f"Raw smifytd value: {dashsheet['J7'].value}")
        print(f"Raw spytd value: {dashsheet['J12'].value}")

        ytddata = {
        "Portfolio": ["S&P500", "SMIF"],
        "Gain (%)": [spytd, smifytd],
        }
        ytddf = pd.DataFrame(ytddata)
        #print(ytddf)

        exceldata = sheet.range("B5:H100").options(pd.DataFrame, header=1, index=False).value
        exceldata = exceldata.dropna(how='any') #Drop rows where all elements are NaN
        #print(exceldata)
    finally: #finally block always executes after normal termination of try block or after try block terminates due to some exception.
        wb.close()
        app.quit()

    barchart = px.bar(
        ytddf, 
        x="Portfolio", 
        y="Gain (%)", 
        title="Portfolio Performance YTD", 
        text="Gain (%)",
        color ="Portfolio",
        color_discrete_map={"S&P500": "#ef553b", "SMIF": "#636efa"}
        )
    
    #barchart.update_yaxes(range=[0, 35])
    barchart.update_layout(
        width=700, 
        height=500, 
        bargap=0.4,
        showlegend=False
        )

    barchart.show()

    donutchart = px.pie(
        exceldata, 
        names='Ticker', 
        values='Weight',
        custom_data=['Live Price', 'Purchase Price', 'Quantity', 'Total Value'],
        title='Portfolio Distribution',
        hole=0.5, 
        )

    donutchart.update_traces(
    textinfo='percent+label', 
    hovertemplate=
    "<b>%{label}</b><br>" +
    "Live Price: $%{customdata[0][0]:,.2f}<br>" +
    "Purchase Price: $%{customdata[0][1]:,.2f}<br>" +
    "Quantity: %{customdata[0][2]:.0f}<br>" +
    "Total Value: $%{customdata[0][3]:,.2f}<br>" +
    "Weight: %{percent}" +
    "<extra></extra>"
    )
    
    donutchart.update_layout(
    autosize=False,
    width=900,
    height=900,
    showlegend=False
    )

  

    donutchart.show()

    return render(request, 'home.html', {'exceldata': exceldata}) #and return our home page | context dictionary, we pass the api variable into our homepage and can now access it

def about(request):
    return render(request, 'about.html', {}) #Allow us to pass stuff into the webpage and use it in the HTMl page in Python



'''
    sampledf = pd.DataFrame([['AAPL', 100], ['ADBE', 120], ['ADP', 80], ['ALL', 50], ['AMZN', 200]], columns = ['Tickers', 'Weight'])

    fig = px.pie(sampledf, names='Tickers', values='Weight',hole=0.5)
    fig.update_traces(
        textinfo='percent+label', 
        hovertemplate='%{label}<br>Price: $%{value}<br>Weight: (%{percent})<extra></extra>'
    )
    fig.show()
'''

#Old views.py from xlwings
'''
from django.shortcuts import render
import xlwings as xw


def home(request): #Whenever someone visits our website, their browser requests our page. We pass that request into our function
    
    import requests #requests stuff from the internet
    import json #javascript object notation, default format for what most APIs return

    smif_wb = xw.Book("SMIF Portfolio Tracker.xlsx")

    portfolio_s = smif_wb.sheets["Portfolio"]

    data_range = portfolio_s.range('B6:I7')

    data = data_range.value #Gets the values of the range specified in data_range

    print(data)

    return render(request, 'home.html', {'data': data}) #and return our home page | context dictionary, we pass the api variable into our homepage and can now access it

def about(request):
    return render(request, 'about.html', {}) #Allow us to pass stuff into the webpage and use it in the HTMl page in Python


'''

#Old views.py from Tiingo API
'''from django.shortcuts import render

def home(request): #Whenever someone visits our website, their browser requests our page. We pass that request into our function
    
    import requests #requests stuff from the internet
    import json #javascript object notation, default format for what most APIs return


    headers = { #explained in notes
        'Content-Type': 'application/json',
        'Authorization': 'Token INSERT_API_KEY_HERE'
        }
    
    tickers = ['aapl','adbe','adp', 'all', 'amzn']
    stock_data = []

    for ticker in tickers:
        api_request = requests.get(f"https://api.tiingo.com/tiingo/daily/{ticker}/prices", headers=headers) #"https://api.tiingo.com/api/test?token=934aff6d72127c613a4b3d0093d49b5565184e27"
        try:
            api = json.loads(api_request.content) #trying to parse the data collected in api_requests from Tiingo
            stock_data.append({ 'ticker': ticker, 'data': api })
        except Exception as e:
            stock_data.append({'ticker': ticker, 'data': 'Error...'})


    return render(request, 'home.html', {'stock_data': stock_data}) #and return our home page | context dictionary, we pass the api variable into our homepage and can now access it

def about(request):
    return render(request, 'about.html', {}) #Allow us to pass stuff into the webpage and use it in the HTMl page in Python'''