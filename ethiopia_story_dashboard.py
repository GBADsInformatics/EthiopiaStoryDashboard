# Ethiopia Story Dashboard
# Date of last revision: July 26, 2022

import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash.exceptions import PreventUpdate 
import pandas as pd
import numpy as np
import json
from dash import dash_table
from dash_extensions.enrich import DashProxy, Output, Input, State, ServersideOutput, html, dcc, ServersideOutputTransform, FileSystemStore


external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

#  IMAGES
# Example images set for the dashboard template, used for logos of the company/entity that is
# showcasing the data visualization. Add more by adding local files to \assets or by image URL.
GBADSLOGOB = "https://i0.wp.com/animalhealthmetrics.org/wp-content/uploads/2019/10/GBADs-LOGO-Black-sm.png"
GBADSLOGOW = "https://i0.wp.com/animalhealthmetrics.org/wp-content/uploads/2019/10/GBADs-LOGO-White-sm.png"


# TAB STYLING
# This is the styling that is applied to the selected tab.
selectedTabStyle = {
    'border': '3px solid white',
    'backgroundColor': 'white',
    'color': 'black'
}

# ******************* LAYOUT *******************
app.layout = html.Div([
    
    html.Div([
        html.Div([html.Img(src=GBADSLOGOW, className="top")], style={'display': 'inline-block'}),
        html.Div([html.H1('Ethiopia Case Study')], style={'display': 'inline-block', 'margin-left': '35%'}),
    ]),
    
    html.Div([

        # ================= LEFT DIV ================= #
        # This div includes all the components for the sidebar menu.
        html.Div(
            id="left-div",
            children=[
                html.Div([
                    html.Div([

                        # ====== SPECIES ====== #
                        html.Div([
                                # --- PANEL HEADING ---
                                html.Div('Species', className='panel-heading'),
                                html.Hr(style={"width": "90%"}),

                                # --- OPTIONS ---
                                html.Div([
                                    html.Button('Cattle', id='cattle-report-btn', className='metadata-button')
                                ], className='metadata-btn-container jc-center'),

                                html.Div([
                                    html.Button('Camels', id='camel-report-btn', className='metadata-button'),
                                ], className='metadata-btn-container jc-center'),

                                html.Div([
                                    html.Button('Goats', id='goat-report-btn', className='metadata-button'),
                                ], className='metadata-btn-container jc-center'),

                                html.Div([
                                    html.Button('Sheep', id='sheep-report-btn', className='metadata-button'),
                                ], className='metadata-btn-container jc-center'),

                            ], className='dropdown-t'),

                        # ====== SPECIES OPTIONS ====== #
                        # html.Div([

                        #     html.Div([
                        #         html.Button('Cattle', id='cattle-report-btn', className='metadata-button')
                        #     ], className='metadata-btn-container jc-center'),

                        #     html.Div([
                        #         html.Button('Camels', id='camel-report-btn', className='metadata-button'),
                        #     ], className='metadata-btn-container jc-center'),

                        #     html.Div([
                        #         html.Button('Goats', id='goat-report-btn', className='metadata-button'),
                        #     ], className='metadata-btn-container jc-center'),

                        #     html.Div([
                        #         html.Button('Sheep', id='sheep-report-btn', className='metadata-button'),
                        #     ], className='metadata-btn-container jc-center'),

                        # ], className='dropdown-b'),

                    ], className='dropdown-container'),

                    # --- SIDEBAR ---
                    html.Div ([
                        # dbc.Button(children="<", id="left-button", className='buttonstyle'),
                        dbc.Button(
                            children=[
                                html.I(className="fa-solid fa-angle-left")
                            ],
                            id='left-button', className='buttonstyle'
                        )
                    ], className="slider"),

                ], className='left-container'),
            ], 
            
            className="options-left"),

            # ================= RIGHT DIV ================= #
            html.Div(
                id="right-div",
                children=[
                    html.Div([

                            dcc.Tabs(
                                id='tabs',
                                children=[
                                
                                # ====== REPORTS ====== #
                                dcc.Tab(
                                    label='Reports', 
                                    children=[
                                        html.Div([
                                            html.Div([
                                                html.H3('Report portion', style={'color':'black'}),
                                                # dcc.Loading(
                                                #     id='faostat-graph-loading-2',
                                                #     children=[dcc.Graph(id='faostat-graph-2', className='graph-size')],
                                                #     type='circle'
                                                # )
                                            ]),
                                        ], className="f-h-scroll-div"),
                                    ],  
                                    className='cattabs',
                                    selected_style=selectedTabStyle
                                ),

                                # ====== METADATA ====== #
                                dcc.Tab(
                                    label='Metadata', 
                                    children=[
                                        html.Div([
                                            html.Div([
                                                html.H3('Metadata portion', style={'color':'black'}),
                                                # dcc.Textarea(
                                                #     id='all-terms',
                                                #     value = 'Fill this in',
                                                #     readOnly=True,
                                                #     className='graph-size',
                                                # ),
                                            ]),
                                        ], className="f-h-scroll-div"),
                                    ],  
                                    className='cattabs',
                                    selected_style=selectedTabStyle
                                ),

                            ]),
                    ], className="r tab-panel"),
                ], className="options-right"),
        ], className='mid'),
        
], className="main-div")


# ******************* CALLBACKS *******************

# Sidebar Callbacks
# Callback to update the sidebar.
@app.callback(
    Output('left-button', 'children'), 
    Input('left-button', 'n_clicks')
)
def change_button_icon(n_clicks):
    if n_clicks%2 == 1:
        return html.I(className="fa-solid fa-angle-right")
    else:
        return html.I(className="fa-solid fa-angle-left")

@app.callback(
    Output('right-div', 'className'), 
    Input('left-button', 'n_clicks')
)
def extend_div(n_clicks):
    if n_clicks%2 == 1:
        return "options-right-open"
    else:
        return "options-right"
@app.callback(
    Output('left-div', 'className'), 
    Input('left-button', 'n_clicks')
)
def slide_div_in(n_clicks):
    if n_clicks%2 == 1:
        return "options-left-closed"
    else:
        return "options-left"


# Callback to handle changing the page based on the pathname provided.
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/dash/':
        layout = page_1
    else:
        layout = "404"
    return layout

# ===== Run app =====
if __name__ == '__main__':
    # app.run_server(use_reloader=True, debug=False, dev_tools_ui=False, dev_tools_props_check=False, host="0.0.0.0", port="8050")
    app.run_server(use_reloader=True, debug=True, dev_tools_ui=True, dev_tools_props_check=True, host="0.0.0.0", port="8050")