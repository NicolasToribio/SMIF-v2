import pandas as pd 
import plotly.express as px



df = pd.DataFrame([['AAPL', 100], ['ADBE', 120], ['ADP', 80], ['ALL', 50], ['AMZN', 200]], columns = ['Tickers', 'Weight'])

fig = px.pie(df, names='Tickers', values='Weight',hole=0.5)
fig.update_traces(
    textinfo='percent+label', 
    hovertemplate='%{label}<br>Price: $%{value}<br>Weight: (%{percent})<extra></extra>'
)
fig.show()


