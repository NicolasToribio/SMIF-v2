from django.shortcuts import render
import pandas as pd
import plotly.express as px


def home(request): #Whenever someone visits our website, their browser requests our page. We pass that request into our function
    
    import requests #requests stuff from the internet
    import json #javascript object notation, default format for what most APIs return

    exceldf = pd.read_excel('SMIF Portfolio Tracker.xlsx', sheet_name='Transaction', usecols='B:H', skiprows=4)
    exceldf = exceldf.dropna(how='any')  # Drop rows where all elements are NaN
    print(exceldf)
    print("Column Names: ")
    print(exceldf.columns)

    donutchart = px.pie(
        exceldf, 
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

    return render(request, 'home.html', {'exceldf': exceldf}) #and return our home page | context dictionary, we pass the api variable into our homepage and can now access it

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

    #934aff6d72127c613a4b3d0093d49b5565184e27
    headers = { #explained in notes
        'Content-Type': 'application/json',
        'Authorization': 'Token 934aff6d72127c613a4b3d0093d49b5565184e27'
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