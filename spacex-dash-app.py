# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

print('-->BEGIN')
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                         {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                     ],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,  max=10000, step=1000,
                                    marks={0: '0',
                                           100: '100'},
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

#TAREA 1:
    


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    
    print('-->get_pie_chart:: begin')

    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class'] == 1]
       
        fig = px.pie(filtered_df, values='class', 
                names='Launch Site', 
                title='Total success launches by Site')
        return fig
    else:


        # Filtrar por sitio
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

        # Contar cantidad de éxitos (1) y fallos (0)
        counts = filtered_df['class'].value_counts().reset_index()
        counts.columns = ['class', 'count']

        # Crear gráfico de torta
        fig = px.pie(counts, 
                  values='count', 
                     names='class', 
                     title='Total success launches for ' + entered_site)

        return fig


    print('-->get_pie_chart:: end')


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
        Output(component_id='success-payload-scatter-chart', component_property='figure'),
        [Input(component_id='site-dropdown', component_property='value'), 
        Input(component_id='payload-slider', component_property='value')]
    )
def get_scatter(entered_site, payload):
    print('-->get_scatter:: begin')
    print(payload)

    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] <= payload[1]) & (spacex_df['Payload Mass (kg)'])]

    if entered_site == 'ALL':
        fig = px.scatter(
                filtered_df,
                x='Payload Mass (kg)',
                y='class',
                color='Booster Version Category',
                title='Correlation between Payload and Success for all Sites'
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.scatter(
                filtered_df,
                x='Payload Mass (kg)',
                y='class',
                color='Booster Version Category',
                title='Correlation between Payload and Success for site: ' + entered_site
        )
        return fig
    print('-->get_scatter:: end')

print('-->END')

# Run the app
if __name__ == '__main__':
    app.run()
