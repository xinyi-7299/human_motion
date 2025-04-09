from dash import Dash, dcc, html, Output, Input, State, ctx
import dash
import plotly.graph_objects as go
import json
import dash_extensions.javascript as dj
import requests
import random
import os

# Load JSON data from files
with open('data/bone_0.json', 'r') as file:
    data_p0 = file.read()
with open('data/bone_1.json', 'r') as file:
    data_p1 = file.read()
with open('data/bone_2.json', 'r') as file:
    data_p2 = file.read()
with open('data/bone_3.json', 'r') as file:
    data_p3 = file.read()
with open('data/bone_4.json', 'r') as file:
    data_p4 = file.read()
with open('data/bone_5.json', 'r') as file:
    data_p5 = file.read()

with open('data/data_A01.json', 'r') as file:
    data_A01 = json.load(file)
with open('data/data_A02.json', 'r') as file:
    data_A02 = json.load(file)
with open('data/data_A03.json', 'r') as file:
    data_A03 = json.load(file)
with open('data/data_A04.json', 'r') as file:
    data_A04 = json.load(file)
with open('data/data_A05.json', 'r') as file:
    data_A05 = json.load(file)
with open('data/data_A06.json', 'r') as file:
    data_A06 = json.load(file)

with open('data/athlete.json', 'r') as file:
    athlete_data = json.load(file)


data_list = [data_p0, data_p1, data_p2, data_p3, data_p4, data_p5]

# Application initialization --------------------------------------------------
app = Dash(__name__)  # Create Dash app instance
server = app.server  # Get Flask server instance for deployment
port = os.getenv("PORT", 8050)  # Get port from environment variable or default

# 3D visualization preprocessing ----------------------------------------------
# Define the number of time steps
time_steps = 120
figs = []

# Loop through the data to create figures
for n in range(0, 6):
    # Define connection orders for the lines
    coordinates = json.loads(data_list[n])
    connection_order_1 = [0, 1]
    connection_order_2 = [4, 3, 2, 5, 6, 7]
    connection_order_3 = [2, 8, 11, 5]
    connection_order_4 = [8, 9, 10]
    connection_order_5 = [11, 12, 13]

    x_lines = []
    y_lines = []
    z_lines = []

    # Loop through each time step to create lines
    for t in range(time_steps):
        x_t = [coordinates[t]['x'][i] if coordinates[t]['x'][i] != 0.0 else None for i in connection_order_1] + [None] + [coordinates[t]['x'][i] if coordinates[t]['x'][i] != 0.0 else None for i in connection_order_2] + [None] + [coordinates[t]['x'][i] if coordinates[t]['x']
                                                                                                                                                                                                                                     [i] != 0.0 else None for i in connection_order_3] + [None] + [coordinates[t]['x'][i] if coordinates[t]['x'][i] != 0.0 else None for i in connection_order_4] + [None] + [coordinates[t]['x'][i] if coordinates[t]['x'][i] != 0.0 else None for i in connection_order_5]

        y_t = [coordinates[t]['y'][i] if coordinates[t]['x'][i] != 0.0 else None for i in connection_order_1] + [None] + [coordinates[t]['y'][i] if coordinates[t]['x'][i] != 0.0 else None for i in connection_order_2] + [None] + [coordinates[t]['y'][i] if coordinates[t]['x']
                                                                                                                                                                                                                                     [i] != 0.0 else None for i in connection_order_3] + [None] + [coordinates[t]['y'][i] if coordinates[t]['x'][i] != 0.0 else None for i in connection_order_4] + [None] + [coordinates[t]['y'][i] if coordinates[t]['x'][i] != 0.0 else None for i in connection_order_5]

        z_t = [coordinates[t]['z'][i] if coordinates[t]['x'][i] != 0.0 else None for i in connection_order_1] + [None] + [coordinates[t]['z'][i] if coordinates[t]['x'][i] != 0.0 else None for i in connection_order_2] + [None] + [coordinates[t]['z'][i] if coordinates[t]['x']
                                                                                                                                                                                                                                     [i] != 0.0 else None for i in connection_order_3] + [None] + [coordinates[t]['z'][i] if coordinates[t]['x'][i] != 0.0 else None for i in connection_order_4] + [None] + [coordinates[t]['z'][i] if coordinates[t]['x'][i] != 0.0 else None for i in connection_order_5]

        x_lines.append(x_t)
        y_lines.append(y_t)
        z_lines.append(z_t)

    # Create frames for the animation
    frames = [go.Frame(
        data=[go.Scatter3d(
            x=x_lines[t], y=y_lines[t], z=z_lines[t],
            mode='lines+markers', line=dict(color='red', width=3),
            marker=dict(size=4, color='green')
        )],
        name=f"frame_{t}"
    ) for t in range(time_steps)]

    # Create the initial figure
    fig = go.Figure(
        data=[go.Scatter3d(
            x=x_lines[0],
            y=y_lines[0],
            z=z_lines[0],
            mode='lines+markers', line=dict(color='red', width=3),
            marker=dict(size=4, color='green')
        )],
        layout=go.Layout(
            width=600,
            height=500,
            margin=dict(t=50, l=1),
            title="skeleton",
            scene=dict(
                xaxis=dict(title='X Axis',),
                yaxis=dict(title='Y Axis',),
                zaxis=dict(title='Z Axis', range=[0, 2]),
                camera=dict(
                    eye=dict(x=1, y=-2, z=0.3)
                )
            )
        ),
        frames=frames
    )
    # list to store the figures
    figs.append(fig)

app.layout = html.Div(
    className="all",
    children=[
        html.Div(
            className="visual_video",
            children=[
                html.Div(
                    className="visual",
                    children=[
                        html.Div(id='text', children="Please select an athlete to view their information.",
                                 style={'marginTop': '20px', 'fontSize': '18px'}),
                        html.Div(
                            children=[
                                dcc.Store(id='figure-store', data=''),
                                dcc.Graph(
                                    id='3d-sport-graph',
                                    figure=figs[0],
                                ),
                                dcc.RadioItems(
                                    className="checklist",
                                    id='checklist',
                                    options=[
                                        {'label': 'A01', 'value': 0},
                                        {'label': 'A02', 'value': 1},
                                        {'label': 'A03', 'value': 3},
                                        {'label': 'A04', 'value': 2},
                                        {'label': 'A05', 'value': 4},
                                        {'label': 'A06', 'value': 5},
                                    ],
                                    value=0,
                                    inline=True
                                )
                            ]
                        ),
                        html.Div(
                            className="button",
                            children=[
                                html.Button("▶️", id="play-button",
                                            n_clicks=0, style={"width": "50px"}),
                                dcc.Dropdown(
                                    className="control-button",
                                    id="dropdown",
                                    options=[
                                        {"label": "0.25X", "value": 0.25},
                                        {"label": "0.5X", "value": 0.5},
                                        {"label": "1.0X", "value": 1.0}
                                    ],
                                    value=1.0,
                                    clearable=False,
                                    style={"width": "90px"}

                                ),
                                dcc.Store(id="video-value"),

                            ]


                        ),



                    ]
                ),
                html.Div(
                    className="video_graph",
                    children=[
                        html.Div(
                            className="video",
                            children=html.Video(
                                id="video-player",
                                controls=True,
                                src="assets/output.mp4",
                                autoPlay=False,
                                loop=True,
                                muted=True,
                                style={"width": "600px"}
                            )
                        ),
                        html.Div(
                            className="graph",
                            children=[
                                html.H3(),
                                dcc.Graph(
                                    id="chart_1",
                                    figure=fig
                                )
                            ]
                        ),
                        html.Div(id="dummy-output", style={"display": "none"})
                    ]
                ),
            ]
        ),
        html.Div(
            className="play-slider",
            children=[
                html.Div(
                    className="time-slider",
                    children=[
                        dcc.Slider(
                            id='time-slider',
                            min=0,
                            max=120,
                            step=1,
                            value=0,
                        ),
                        # Control the automatically transfer video frame to slider
                        dcc.Interval(
                            id='interval',
                            interval=30,
                            n_intervals=0,
                            # disabled=True
                        )
                    ]),

            ]),
    ])


# @app.callback(
#     Output('time-slider', 'value'),
#     [Input("interval", "n_intervals"),
#      Input("update-value", "n_clicks"),
#      State('time-slider', 'value'),
#      State('video-value', 'data')]
# )
# def updateValue(n_intervals, n_clicks, value, data):
#     triggered_id = ctx.triggered_id
#     if triggered_id == "update-value":
#         return data if data is not None else 0
#     elif triggered_id == "interval":
#         return (value + 1) % 120 if value is not None else 0
#     return 0

@app.callback(
    Output('time-slider', 'value'),
    [Input("interval", "n_intervals"),
     State('time-slider', 'value'),
     State('video-value', 'data')]
)
def updateValue(n_intervals, value, data):
    # if value is None or data is None:
    #     return 0
    # if abs(value - data) >= 10:
    #     print(f"data: {data}")
    #     return data
    # else:
    #     print(f"value: {value + 1}")
    #     return (value + 1) % 120
    return n_intervals


@app.callback(
    Output('text', 'children'),
    [Input('checklist', 'value'),
     Input('time-slider', 'value')]
)
def update_text(value, n):
    num = int(value)+1
    athlete = athlete_data[f"A0{num}"]
    if value == 0:
        sport_data = data_A01[n]["height"]
        return html.Div(className="info", children=[
            html.Div(f"name: {athlete['name']}",
                     style={"margin-right": "20px"}),
            html.Div(f"height: {athlete['height']}cm",
                     style={"margin-right": "20px"}),
            html.Div(f"weight: {athlete['weight']}kg",
                     style={"margin-right": "20px"}),
            html.Div(f"sport: {athlete['sport']}",
                     style={"margin-right": "20px"}),
            html.Div(f"kick height: {sport_data}m"),
        ])
    elif value == 1:
        sport_data = data_A02[n]["speed"]
        return html.Div(className="info", children=[
            html.Div(f"name: {athlete['name']}",
                     style={"margin-right": "20px"}),
            html.Div(f"height: {athlete['height']}cm",
                     style={"margin-right": "20px"}),
            html.Div(f"weight: {athlete['weight']}kg",
                     style={"margin-right": "20px"}),
            html.Div(f"sport: {athlete['sport']}",
                     style={"margin-right": "20px"}),
            html.Div(f"jogging speed: {sport_data}m/s"),
        ])
    elif value == 2:
        sport_data = data_A04[n]["height"]
        return html.Div(className="info", children=[
            html.Div(f"name: {athlete['name']}",
                     style={"margin-right": "20px"}),
            html.Div(f"height: {athlete['height']}cm",
                     style={"margin-right": "20px"}),
            html.Div(f"weight: {athlete['weight']}kg",
                     style={"margin-right": "20px"}),
            html.Div(f"sport: {athlete['sport']}",
                     style={"margin-right": "20px"}),
            html.Div(f"jump height: {sport_data}m"),
        ])
    elif value == 3:
        sport_data = data_A03[n]["height"]
        return html.Div(className="info", children=[
            html.Div(f"name: {athlete['name']}",
                     style={"margin-right": "20px"}),
            html.Div(f"height: {athlete['height']}cm",
                     style={"margin-right": "20px"}),
            html.Div(f"weight: {athlete['weight']}kg",
                     style={"margin-right": "20px"}),
            html.Div(f"sport: {athlete['sport']}",
                     style={"margin-right": "20px"}),
            html.Div(f"throw height: {sport_data}m"),
        ])
    elif value == 4:
        sport_data = data_A05[n]["speed"]
        return html.Div(className="info", children=[
            html.Div(f"name: {athlete['name']}",
                     style={"margin-right": "20px"}),
            html.Div(f"height: {athlete['height']}cm",
                     style={"margin-right": "20px"}),
            html.Div(f"weight: {athlete['weight']}kg",
                     style={"margin-right": "20px"}),
            html.Div(f"sport: {athlete['sport']}",
                     style={"margin-right": "20px"}),
            html.Div(f"boxing speed: {sport_data}m/s"),
        ])
    elif value == 5:
        sport_data = data_A06[n]["speed"]
        return html.Div(className="info", children=[
            html.Div(f"name: {athlete['name']}",
                     style={"margin-right": "20px"}),
            html.Div(f"height: {athlete['height']}cm",
                     style={"margin-right": "20px"}),
            html.Div(f"weight: {athlete['weight']}kg",
                     style={"margin-right": "20px"}),
            html.Div(f"sport: {athlete['sport']}",
                     style={"margin-right": "20px"}),
            html.Div(f"swim speed: {sport_data}m/s"),
        ])


@app.callback(
    Output('interval', 'interval'),
    Input('dropdown', 'value'),
)
def update_speed(value):
    speed = 30
    if value == 0.25:
        speed = 100
    if value == 0.5:
        speed = 50
    return speed


@app.callback(
    Output('3d-sport-graph', 'figure'),
    [Input('time-slider', 'value'),
     Input('checklist', 'value')]
)
def update_figure(value, n):
    a = int(n)
    fig = figs[a]
    fig.update_traces(x=fig.frames[value].data[0].x,
                      y=fig.frames[value].data[0].y,
                      z=fig.frames[value].data[0].z,
                      line=dict(color='red', width=3),
                      marker=dict(
        color=fig.frames[value].data[0].marker.color, size=frames[value].data[0].marker.size))
    # fig.update_layout(
    #     width=600,
    #     height=500,
    #     margin=dict(t=50, l=1),
    #     xaxis=dict(
    #         range=[-1, 2.5]
    #     )
    # )
    return fig


# @app.callback(
#     Output('interval', 'disabled'),
#     Output('play-button', 'children'),
#     Input('play-button', 'n_clicks'),
#     prevent_initial_call=False
# )
# def toggle_play_pause(n_clicks):
#     if n_clicks % 2 == 1:
#         return False, "⏸️"
#     else:
#         return True, "▶️"


app.clientside_callback(
    """
    function updatePlay(video_id, n_clicks, value) {
        const video = document.getElementById(video_id)
        if (n_clicks % 2 === 1){
            video.play()
        }
        else {
            video.pause()
        }
        if (value && value){
            video.playbackRate = value;
        }
    }
    """,
    Output("dummy-output", "children"),
    Input("video-player", "id"),
    Input("play-button", "n_clicks"),
    Input("dropdown", "value")
)

app.clientside_callback(
    """
    function updateCurrentFrame(video_id) {
        const video = document.getElementById(video_id);
        if (!video) return null;
        const FPS = 33.3;
        return new Promise(resolve => {
            video.addEventListener("timeupdate", () => {
                const currentFrame = Math.floor(video.currentTime * FPS);
                //console.log(video.currentTime)
                if (currentFrame <= 120) {
                    //console.log(currentFrame);  // Log the current frame value
                    resolve(currentFrame);  // Resolve the Promise with current frame
                } else {
                    resolve(0);  // If frame exceeds, resolve with 0
                }

             });
         });
     }
     """,
    Output("video-value", "data"),
    Input("video-player", "id"),
    Input("interval", "n_intervals")
)

# app.clientside_callback(
#     """
#     function playbackRate(video_id, value) {
#         const video = document.getElementById(video_id);
#         if (video && value) {
#             video.playbackRate = value;
#         }
#      """,
#     Input("video-player", "id"),
#     Input("dropdown", "value")
# )


@app.callback(
    Output("chart_1", "figure"),
    [Input("time-slider", "value"),
     Input("checklist", "value")]
)
def update_chart(i, n):
    fig = go.Figure()
    if n == 0:
        data = data_A01[0:i+1]
        data_x = [item["frame"] for item in data]
        data_y = [item["height"] for item in data]
        fig.add_trace(go.Scatter(x=data_x, y=data_y, line=dict(color="blue")))
        fig.update_layout(
            title="kick height",
            xaxis=dict(title="frame"),
            yaxis=dict(title="height(m)"),
            width=700,
            height=350,
            margin=dict(t=50, l=1)
        )
    elif n == 1:
        data = data_A02[0:i+1]
        data_x = [item["frame"] for item in data]
        data_y = [item["speed"] for item in data]
        fig.add_trace(go.Scatter(x=data_x, y=data_y, line=dict(color="blue")))
        fig.update_layout(
            title="jogging speed",
            xaxis=dict(title="frame"),
            yaxis=dict(title="speed(m/s)"),
            width=700,
            height=350,
            margin=dict(t=50, l=1)
        )
    elif n == 2:
        data = data_A04[0:i+1]
        data_x = [item["frame"] for item in data]
        data_y = [item["height"] for item in data]
        fig.add_trace(go.Scatter(x=data_x, y=data_y, line=dict(color="blue")))
        fig.update_layout(
            title="jump height",
            xaxis=dict(title="frame"),
            yaxis=dict(title="height(m)"),
            width=700,
            height=350,
            margin=dict(t=50, l=1)
        )
    elif n == 3:
        data = data_A03[0:i+1]
        data_x = [item["frame"] for item in data]
        data_y = [item["height"] for item in data]
        fig.add_trace(go.Scatter(x=data_x, y=data_y, line=dict(color="blue")))
        fig.update_layout(
            title="throw height",
            xaxis=dict(title="frame"),
            yaxis=dict(title="height(m)"),
            width=700,
            height=350,
            margin=dict(t=50, l=1)
        )
    elif n == 4:
        data = data_A05[0:i+1]
        data_x = [item["frame"] for item in data]
        data_y = [item["speed"] for item in data]
        fig.add_trace(go.Scatter(x=data_x, y=data_y, line=dict(color="blue")))
        fig.update_layout(
            title="boxing speed",
            xaxis=dict(title="frame"),
            yaxis=dict(title="speed(m/s)"),
            width=700,
            height=350,
            margin=dict(t=50, l=1)
        )
    elif n == 5:
        data = data_A06[0:i+1]
        data_x = [item["frame"] for item in data]
        data_y = [item["speed"] for item in data]
        fig.add_trace(go.Scatter(x=data_x, y=data_y, line=dict(color="blue")))
        fig.update_layout(
            title="swim speed",
            xaxis=dict(title="frame"),
            yaxis=dict(title="speed(m/s)"),
            width=700,
            height=350,
            margin=dict(t=50, l=1)
        )
    return fig


# Application execution -------------------------------------------------------
if __name__ == '__main__':
    app.run_server(
        debug=True,
        host="0.0.0.0",
        use_reloader=True,
        port=int(port))
