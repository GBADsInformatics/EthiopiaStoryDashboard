# Ethiopia Story Dashboard
# Date of last revision: July 28, 2022

import dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import dash_table
from dash_extensions.enrich import DashProxy, Output, Input, State, ServersideOutput, html, dcc, ServersideOutputTransform, FileSystemStore
import pandas as pd

external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
fss = FileSystemStore(cache_dir='ethdash_cache')
app = DashProxy(transforms=[ServersideOutputTransform(backend=fss)], external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# GBADS LOGO #
GBADSLOGOB = "https://i0.wp.com/animalhealthmetrics.org/wp-content/uploads/2019/10/GBADs-LOGO-Black-sm.png"
GBADSLOGOW = "https://i0.wp.com/animalhealthmetrics.org/wp-content/uploads/2019/10/GBADs-LOGO-White-sm.png"

# VARIABLES DECLARATION #

# TAB STYLING #
## Could not resolve this in CSS for some reason ##
activeLabelStyle = {
    'backgroundColor': '#C4C4C4',
    'color': 'black',
}

# PAGE LAYOUT #
app.layout = html.Div([
    
    # === PAGE HEADER === #
    html.Div(
        id='page-header',
        children=[
            html.Div([html.Img(src=GBADSLOGOW, className="top")], id='logo-img'),
            html.Div([html.Div('Ethiopia Case Study')], id='dashboard-title'),
        ]
    ),

    # === PAGE BODY === #
    html.Div(
        id='page-body',
        children=[
        
        # ----- LEFT PANEL ----- #
        html.Div(
            id='left-panel',
            children=[

                # --- COLLAPSE BUTTON --- #
                html.Div(
                    id='collapse-btn-container',
                    children=[
                        html.Button(
                            id='collapse-btn',
                            children=[
                                html.I(className='fa-solid fa-angle-left')
                            ]
                        )
                    ]
                ),

                # --- SIDE MENU --- #
                html.Div(
                    id='side-menu',
                    className='side-menu-default',
                    children=[
                        html.Div(
                            id='side-menu-content',
                            children=[

                                # TITLE #
                                html.Div('Species', id='side-menu-title'),

                                html.Hr(className='separator-line'),

                                # OPTION BUTTONS #
                                html.Div(
                                    id='side-menu-options',
                                    children=[
                                        html.Button('Cattle', id='cattle-btn', className='options-btn'),
                                        html.Button('Camels', id='camels-btn', className='options-btn'),
                                        html.Button('Goats', id='goats-btn', className='options-btn'),
                                        html.Button('Sheep', id='sheep-btn', className='options-btn'),
                                    ]
                                )

                            ]
                        ),
                ]),


            ]
        ),

        # ----- RIGHT PANEL ----- #
        html.Div(
            id='right-panel',
            children=[

                # --- TABS --- #
                dbc.Tabs(
                    children=[

                        # === REPORTS === #
                        dbc.Tab(
                            label='Reports',
                            label_class_name='tab-label',
                            tab_class_name='tab',
                            active_label_style=activeLabelStyle,
                            class_name='tab-content',
                            children=[
                                html.Div('Report stuff')
                                # html.Div(
                                #     class_name='tab-content',   
                                #     children=['Report stuff']
                                # )
                            ],
                        ),

                        # === METADATA === #
                        dbc.Tab(
                            label='Metadata',
                            label_class_name='tab-label',
                            tab_class_name='tab',
                            active_label_style=activeLabelStyle,
                            class_name='tab-content',
                            children=[
                                html.Div('Metadata stuff')
                            ],
                        )
                ])
            ]
        ),


        
        ]
    ),

], id='dashboard-page')


# CALLBACKS #

# COLLAPSE BUTTON STYLE CHANGE #
@app.callback(
    Output('collapse-btn', 'children'),
    Output('side-menu', 'className'),
    Input('collapse-btn', 'n_clicks'),
)
def change_button_icon(n_clicks):
    if  n_clicks is None:
        raise PreventUpdate

    if n_clicks%2 == 1:
        return [
            html.I(className='fa-solid fa-angle-right'),
            'side-menu-closed',
            ]
    else:
        return [
            html.I(className='fa-solid fa-angle-left'),
            'side-menu-default',
        ]


# RUN APP #
if __name__ == '__main__':
    # app.run_server(use_reloader=True, debug=False, dev_tools_ui=False, dev_tools_props_check=False, host="0.0.0.0",     port="8050")
    app.run_server(use_reloader=True, debug=True, dev_tools_ui=True, dev_tools_props_check=True, host="0.0.0.0", port="8050")