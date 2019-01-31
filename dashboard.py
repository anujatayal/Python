import dash
import dash_table
import pandas as pd
import json
import numpy as np
from pprint import pprint
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import plotly.graph_objs as go


with open('hello.json') as data_file:
    data=json.load(data_file)

df = pd.DataFrame.from_dict(data, orient='columns')
#df['published']=pd.to_datetime(df['published']).dt.strftime("%x")
df['published']=pd.to_datetime(df['published'])

df['impact']=pd.to_numeric(df['impact'])
df['impact'].fillna(0,inplace=True)

df['intensity']=pd.to_numeric(df['intensity'])
df['intensity'].fillna(0,inplace=True)

df['likelihood']=pd.to_numeric(df['likelihood'])
df['likelihood'].fillna(0,inplace=True)

df['relevance']=pd.to_numeric(df['relevance'])
df['relevance'].fillna(0,inplace=True)

#print df.dtypes
del df['added']
#columns=list(df)
columns=['title','topic','intensity','sector','region','pestle']
#print columns
#print df[columns].head()
measures=df[['intensity','relevance','impact','likelihood']]
axis_names=df[['sector','region','topic','pestle','country']]
axis_column=list(axis_names)
measures_column=list(measures)
#print(df['sector'])
#topic_names= df['topic'].dropna().unique()
#sector_names= df['sector'].dropna().unique()
#pestle_names= df['pestle'].dropna().unique()

app=dash.Dash()
app.layout=html.Div(children=[
        html.H1(children='Dash Tutorials'),
        html.Div([
                  html.H3(children='X Axis'),
                  dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i}
                             for i in axis_column],
                    value='sector'
                     )],
                 #style={'width': '28%', 'float': 'right'}
                 ),
        html.Hr(),
        html.Div([
                html.H3(children='Y Axis'),
                dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i}
                            for i in axis_column],
                value='region'
                )],
                 #style={'width': '28%', 'float': 'right'}
                 ),

                              
        html.Div([
                html.H3(children='Measures'),
                dcc.Dropdown(
                id='measures-column',
                options=[{'label': i, 'value': i}
                for i in measures_column],
                value='intensity'
                )],
                 #style={'width': '28%', 'float': 'right'}
                 ),

    
        html.Div(children=[
                html.H3(id='display-first-option'),
                  dcc.Dropdown(id='first-dropdown')]),
        html.Div(children=[
                html.H3(id='display-second-option'),
                dcc.Dropdown(id='second-dropdown')]),
        html.Div(children=[
                html.H3(id='display-third-option'),
                dcc.Dropdown(id='third-dropdown')]),
        html.Div([
                dcc.Graph(id='Blackcoffer',
#                hoverData={'points': [{'customdata': 'Japan'}]}
                    )
                  ],  #style={"height" : "50vh", "width" : "70%"}
                 ),
        dcc.Textarea(
                placeholder='Enter a value...',
                value='This is a TextArea component',
                style={'width': '100%'}
            ),
    dash_table.DataTable(
    id='table',
    data=df.to_dict("rows"),
    columns=[{"name": i, "id": i} for i in columns],
    pagination_settings={
            'current_page':0,
            'page_size':10
    },
#    style_cell={'minWidth': '80px','maxWidth': '180px','textAlign': 'left','textOverflow': 'ellipsis'},
   style_table={'maxHeight':'300px','overflowX':'scroll', 'border': 'thin lightgrey solid'},
#    n_fixed_rows=1,
    style_cell_conditional=[
    {'if': {'column_id': 'title'},
    'width': '45%'},
    {'if': {'column_id': 'topic'},
    'width': '8%'},
    {'if': {'column_id': 'intensity'},
    'width': '6%'},
    {'if': {'column_id': 'sector'},
    'width': '15%'},
    {'if': {'column_id': 'region'},
    'width': '15%'},
    {'if': {'column_id': 'pestle'},
     'width': '10%'}],

    style_cell={
            'minWidth': '20px', 'maxWidth': '100px',
             'whiteSpace': 'normal',
            'textAlign': 'left'
            },
#    css=[{
#        'selector': '.dash-cell div.dash-cell-value',
#        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
#         }],
    
    filtering=True,
    sorting=True,
#
            ),
    dcc.Slider(
            min=0,
            max=9,
            marks={i: 'Label {}'.format(i) for i in range(10)},
            value=5,
            ),
    dcc.DatePickerSingle(
            id='date-picker-single',
            date=dt(1997, 5, 10)
            )
      ])
#@app.callback(
#              dash.dependencies.Output('display-first-option', 'children'),
#              [dash.dependencies.Input('xaxis-column', 'value'),
#               dash.dependencies.Input('yaxis-column', 'value')])

#First Dropdown

@app.callback(
              dash.dependencies.Output('display-first-option', 'children'),
              [dash.dependencies.Input('xaxis-column', 'value'),
               dash.dependencies.Input('yaxis-column', 'value')])
def set_display_children(x_option,y_option):
    print "First 1", x_option
    axis_column.remove(x_option)
    axis_column.remove(y_option)
    print "First 2", axis_column
    print "First 3", axis_column[0]
    return axis_column[0]

@app.callback(
              dash.dependencies.Output('first-dropdown', 'options'),
              [dash.dependencies.Input('display-first-option', 'children')])
def set_dropdown_options(option):
    print "First 4", option
    options=df[option].unique()
    print "First 5", options
    return [{'label': i, 'value': i} for i in options]

#setting default value in dropdown
@app.callback(
              dash.dependencies.Output('first-dropdown', 'value'),
              [dash.dependencies.Input('first-dropdown', 'options')])
def set_dropdown_value(available_options):
    return available_options[0]

#-------------------------------------------------------------------------
#Second Dropdown
@app.callback(
              dash.dependencies.Output('display-second-option', 'children'),
              [dash.dependencies.Input('display-first-option', 'children')])
def set_display_children(option):
    print "Second 1", option
    axis_column.remove(option)
    print "Second 2", axis_column
    print "Second 3", axis_column[0]
    return axis_column[0]

@app.callback(
              dash.dependencies.Output('second-dropdown', 'options'),
              [dash.dependencies.Input('display-second-option', 'children')])
def set_dropdown_options(option):
    print "Second 4", option
    options=df[option].unique()
    print "Second 5", options
    return [{'label': i, 'value': i} for i in options]

#setting default value in dropdown
@app.callback(
              dash.dependencies.Output('second-dropdown', 'value'),
              [dash.dependencies.Input('second-dropdown', 'options')])
def set_dropdown_value(available_options):
    return available_options[0]

#-------------------------------------------------------------------------
#Third Dropdown

@app.callback(
              dash.dependencies.Output('display-third-option', 'children'),
              [dash.dependencies.Input('display-second-option', 'children')])
def set_display_children(option):
    print "Third 1", option
    axis_column.remove(option)
    print "Third 2", axis_column
    print "Third 3", axis_column[0]
    return axis_column[0]

@app.callback(
              dash.dependencies.Output('third-dropdown', 'options'),
              [dash.dependencies.Input('display-third-option', 'children')])
def set_dropdown_options(option):
    print "Third 4", option
    options=df[option].unique()
    print "Third 5", options
    return [{'label': i, 'value': i} for i in options]

#setting default value in dropdown
@app.callback(
              dash.dependencies.Output('third-dropdown', 'value'),
              [dash.dependencies.Input('third-dropdown', 'options')])
def set_dropdown_value(available_options):
    return available_options[0]

#-------------------------------------------------------------------------
@app.callback(
      dash.dependencies.Output('Blackcoffer', 'figure'),
      [dash.dependencies.Input('xaxis-column', 'value'),
       dash.dependencies.Input('yaxis-column', 'value'),
       dash.dependencies.Input('measures-column','value'),
       dash.dependencies.Input('display-first-option','children'),
       dash.dependencies.Input('display-second-option','children'),
       dash.dependencies.Input('display-third-option','children'),
       dash.dependencies.Input('first-dropdown','value'),
       dash.dependencies.Input('second-dropdown','value'),
       dash.dependencies.Input('third-dropdown','value')])
def update_graph(xaxis_column_name, yaxis_column_name, measures_column_name,first_dropdown_option, second_dropdown_option, third_dropdown_option,first_dropdown,second_dropdown, third_dropdown):
#def update_graph(xaxis_column_name, yaxis_column_name, measures_column_name):
    print xaxis_column_name
    print yaxis_column_name
    print measures_column_name
    print type(first_dropdown)
    print first_dropdown['value']
    print second_dropdown
    print third_dropdown
    print first_dropdown_option
    print second_dropdown_option
    print third_dropdown_option
    x1=df[[xaxis_column_name, yaxis_column_name, measures_column_name,first_dropdown_option]]
    x2=x1.loc[x1[first_dropdown_option]==first_dropdown['value']]
    print x2.head()
    print x2.shape

    #print x1[[first_dropdown]]
# x1=df[[xaxis_column_name, yaxis_column_name, measures_column_name, first_dropdown, second_dropdown, third_dropdown]]
    print x1.head()
    #print x1['intensity']
    #print df['intensity'].max()
    return {
        'data': [go.Heatmap(
                            x=x2[xaxis_column_name],
                            y=x2[yaxis_column_name],
                            z=x2[measures_column_name],
                            colorscale='Viridis'
                            )],
                            #                            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
                            #mode='markers',
                            #marker={
                            ##'size': 15,
                            #'opacity': 0.5,
                            #'line': {'width': 0.5, 'color': 'white'}
            'layout': go.Layout(
                                title='Blackcofffer Heatmap',
                                xaxis={
                                'title': xaxis_column_name,
                                #'type': 'linear'
                                },
                                yaxis={
                                'title': yaxis_column_name,
                                #'type': 'linear'
                                },
                                margin={'l': 100, 'b': 40, 't': 20, 'r': 30},
                                hovermode='closest'
                                )
            }


if __name__=='__main__':
    app.run_server(debug=True)
