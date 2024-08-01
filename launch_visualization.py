import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import seaborn as sns 
import matplotlib.pyplot as plt

# Load the data using pandas
data = pd.read_csv('data/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# List of years 
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
   
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
    html.Div([
    html.Div(id='output-container')])
    
    ])
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

#Callback for plotting
# Define the callback function to update the output container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')])


def update_output_container(report_type,input_year):
   if report_type == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        


#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig=px.line(yearly_rec, x='Year', y='Automobile_Sales',markers=True,title="Average Automobile Sales fluctuation over Recession Period")
        fig.update_traces(marker=dict(color='LightSkyBlue',size=8))
        R_chart1 = dcc.Graph(figure=fig)
#Plot 2 Calculate the average number of vehicles sold by vehicle type       
        
        # use groupby to create relevant data for plotting
       
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2  = dcc.Graph(
            figure=px.bar( average_sales,
            x='Vehicle_Type',
            y='Automobile_Sales',
            color='Vehicle_Type',
            title="Average Automobile Sales by vehicle Type over All Recession Periods"))
        
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # grouping data for plotting
	
        exp_rec= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,values=exp_rec.values,names=list(exp_rec.index),
            title="Total Advertising Expenditure by Vehicle type During Recessions"))

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        #grouping data for plotting
	
        unemp_data= recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_data,x='unemployment_rate',y='Automobile_Sales',color='Vehicle_Type',
        labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
        title='Effect of Unemployment Rate on Vehicle Type and Sales'))
        return [
             html.Div(className='chart-grid', children=[html.Div(children=R_chart1, style={'width': '50%','display': 'inline-block'}),html.Div(children=R_chart2,style={'width': '50%','display': 'inline-block'}),]),
            html.Div(className='chart-grid', children=[html.Div(children=R_chart3,style={'width': '50%','display': 'inline-block'}),html.Div(children=R_chart4,style={'width': '50%','display': 'inline-block'})])
            ]
      


        
# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

