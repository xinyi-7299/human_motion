from dash import Dash, dcc, html, Output, Input, State, ctx
import dash
import plotly.graph_objects as go
import json
import dash_extensions.javascript as dj
import requests
import random
import os


# api_url = "http://127.0.0.1:8000/api/quertspeed"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
data_path_0 = os.path.join(BASE_DIR, "data", "bone_0.json")
data_path_1 = os.path.join(BASE_DIR, "data", "bone_1.json")
data_path_2 = os.path.join(BASE_DIR, "data", "bone_2.json")
data_path_3 = os.path.join(BASE_DIR, "data", "bone_3.json")
data_path_4 = os.path.join(BASE_DIR, "data", "bone_4.json")
data_path_5 = os.path.join(BASE_DIR, "data", "bone_5.json")
# data_path_6 = os.path.join(BASE_DIR, "`data", "bone_6.json")
data_athlete = os.path.join(BASE_DIR, "data", "athlete.json")

assets_path = os.path.join(BASE_DIR, "data", "output.mp4")


print("This is the base directory ========>")
print(BASE_DIR)
print("This is the data path1 ========>")

print(data_path_0)
# Load JSON data from files
with open(data_path_0, 'r') as file:
    data_p0 = file.read()
with open(data_path_1, 'r') as file:
    data_p1 = file.read()
with open(data_path_2, 'r') as file:
    data_p2 = file.read()
with open(data_path_3, 'r') as file:
    data_p3 = file.read()
with open(data_path_4, 'r') as file:
    data_p4 = file.read()
with open(data_path_5, 'r') as file:
    data_p5 = file.read()
# with open(data_path_6, 'r') as file:
#     data_p6 = file.read()

with open(data_athlete, 'r') as file:
    athlete_data = json.load(file)

# with open('../data/girl_3.json', 'r') as file:
#     data_p3 = file.read(file)


data_list = [data_p0, data_p1, data_p2, data_p3, data_p4, data_p5]
app = Dash()

server = app.server

port = os.getenv("PORT", 8050)

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
            title="skeleton",
            scene=dict(
                xaxis=dict(title='X Axis',),
                yaxis=dict(title='Y Axis',),
                zaxis=dict(title='Z Axis',),
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
              className="graph-video",
              children=[
                  html.Div(id='text', children="Please select an athlete to view their information.",
                           style={'marginTop': '20px', 'fontSize': '18px'}),
                  html.Div(
                      className="graph",
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
                                  {'label': 'A02', 'value': 2},
                                  {'label': 'A03', 'value': 4},
                                  {'label': 'A04', 'value': 1},
                                  {'label': 'A05', 'value': 5},
                                  {'label': 'A06', 'value': 6},
                              ],
                              value=0,
                              inline=True
                          )
                      ]
                  ),
                  html.Div(
                      className="video",
                      children=html.Video(
                          id="video-player",
                          controls=True,
                          src=assets_path,
                          autoPlay=False,
                          loop=True,
                          muted=True,
                          style={"width": "600px"}
                      )
                  )
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
                            max=60,
                            step=1,
                            value=0,
                        ),
                        # Control the automatically transfer video frame to slider
                        dcc.Interval(
                            id='interval',
                            interval=35,
                            n_intervals=0,
                            disabled=False
                        ),
                        dcc.Interval(
                            id='interval_1',
                            interval=100,
                            n_intervals=0,
                            disabled=False
                        )
                    ]),
                html.Div(
                    className="control-button",
                    children=[
                        html.Button("▶️", id="play-button",
                                    n_clicks=0, style={"width": "50px"}),
                        dcc.Dropdown(
                            className="control-button",
                            id="dropdown",
                            options=[
                                {"label": "0.25X", "value": 0.25},
                                {"label": "0.5X", "value": 0.5},
                                {"label": "1.0X", "value": 1.0},
                                {"label": "1.5X", "value": 1.5}
                            ],
                            value=1.0,
                            clearable=False,
                            style={"width": "90px"}

                        ),
                        html.Button("sync", id="update-value",
                                    style={"width": "50px"}),
                        dcc.Store(id="video-value")
                    ]


                )
            ])

    ])


@app.callback(
    Output('time-slider', 'value'),
    [Input("interval", "n_intervals"),
     Input("update-value", "n_clicks"),
     State('time-slider', 'value'),
     State('video-value', 'data')]
)
def updateValue(n_intervals, n_clicks, value, data):
    triggered_id = ctx.triggered_id
    if triggered_id == "update-value":
        return data if data is not None else 0
    elif triggered_id == "interval":
        return (value + 1) % 120 if value is not None else 0
    return 0


@app.callback(
    Output('text', 'children'),
    [Input('checklist', 'value'),
     State('time-slider', 'value')]
)
def update_text(value, slider_value):

    num = int(value)+1
    athlete = athlete_data[f"A0{num}"]

    # res = requests.post(api_url, json={"ID": f"A0{num}"})
    # res_json = res.json()

    # if slider_value is None:
    #     slider_value = 0  # 或者设置一个默认值
    # elif slider_value <= 30:
    #     speed = res_json["SpeedData"][0]["speed"]
    # elif slider_value <= 60 and slider_value > 30:
    #     speed = res_json["SpeedData"][1]["speed"]

    return html.Div([
        f"{athlete}"
    ])


@app.callback(
    Output('interval', 'interval'),
    Input('dropdown', 'value'),
)
def update_speed(value):
    speed = 30
    if value == 0.25:
        speed = 120
    if value == 0.5:
        speed = 60
    if value == 1.5:
        speed = 20
    return speed


@app.callback(
    Output('3d-sport-graph', 'figure'),
    [Input('time-slider', 'value'),
     Input('checklist', 'value')]
)
def update_figure(value, n):

    a = int(n)
    fig = figs[a]
    if a == 0:
        fig.update_traces(x=fig.frames[value].data[0].x,
                          y=fig.frames[value].data[0].y,
                          z=fig.frames[value].data[0].z,
                          line=dict(color='blue', width=3),
                          marker=dict(
            color=fig.frames[value].data[0].marker.color, size=frames[value].data[0].marker.size))
    else:
        fig.update_traces(x=fig.frames[value].data[0].x,
                          y=fig.frames[value].data[0].y,
                          z=fig.frames[value].data[0].z,
                          line=dict(color='blue', width=3),
                          marker=dict(
            color=fig.frames[value].data[0].marker.color, size=frames[value].data[0].marker.size))
    return fig


@app.callback(
    Output('interval', 'disabled'),
    Output('play-button', 'children'),
    Input('play-button', 'n_clicks'),
    prevent_initial_call=False
)
def toggle_play_pause(n_clicks):
    if n_clicks % 2 == 1:
        return False, "⏸️"
    else:
        return True, "▶️"


app.clientside_callback(
    """
    function updatePlay(video_id, n_clicks) {
        const video = document.getElementById(video_id)
        if (n_clicks % 2 === 1){
            video.play()
        }
        else {
            video.pause()
        }
    }
    """,
    Input("video-player", "id"),
    Input("play-button", "n_clicks")
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
                    console.log(currentFrame);  // Log the current frame value
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


if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=int(port))
