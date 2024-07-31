import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import seaborn as sns 


# Load the data using pandas
data = pd.read_csv('./historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# List of years 
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard",style={'textAlign': 'center', 'color': '#503D36','font-size': 24}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(id='dropdown-statistics', 
        options=[ {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                  {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                ],
        placeholder='Select a report type',
       value='Select Statistics',
        style = {'width' : '80%', 'padding' : '3px',  'font-size': '20px', 'text-align-last' : 'center'}
        )
    ]),
    html.Div([html.Label("Select Year:"),
            dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='Select-year',
            placeholder='Select-year',
            style = {'width' : '80%', 'padding' : '3px',  'font-size': '20px', 'text-align-last' : 'center'}
        )]),
    html.Div([#TASK 2.3: Add a division for output display
    html.Div(id='output-container')])
    
    ])

