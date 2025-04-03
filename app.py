from dash import Dash, dcc, html, Output, Input, State, ctx
import dash
import plotly.graph_objects as go
import json
import dash_extensions.javascript as dj
import requests
import random
import os

# File path configuration -----------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Project root directory

# Define data file paths
DATA_FILES = [os.path.join(
    BASE_DIR, "data", f"bone_{i}.json") for i in range(7)]
ATHLETE_DATA_PATH = os.path.join(
    BASE_DIR, "data", "athlete.json")  # Athlete metadata
VIDEO_PATH = os.path.join(BASE_DIR, "data", "output.mp4")  # Sample video

# Data loading ----------------------------------------------------------------
# Load skeletal data
bone_data = []
for path in DATA_FILES:
    with open(path, 'r') as f:
        bone_data.append(f.read())

# Load athlete information
with open(ATHLETE_DATA_PATH, 'r') as f:
    athlete_data = json.load(f)

# Application initialization --------------------------------------------------
app = Dash(__name__)  # Create Dash app instance
server = app.server  # Get Flask server instance for deployment
port = os.getenv("PORT", 8050)  # Get port from environment variable or default

# 3D visualization preprocessing ----------------------------------------------
TIME_STEPS = 120  # Total animation frames
figs = []  # Store 3D figures for all athletes

# Bone connection orders for skeleton visualization
BONE_CONNECTIONS = [
    [0, 1],          # Upper torso
    [4, 3, 2, 5, 6, 7],  # Right arm
    [2, 8, 11, 5],   # Spine
    [8, 9, 10],      # Left leg
    [11, 12, 13]     # Right leg
]


def process_coordinates(coordinates, connections):
    """Process coordinate data to generate line connections between joints
    Args:
        coordinates: Raw joint position data
        connections: Defined bone connection orders
    Returns:
        Tuple of (x_lines, y_lines, z_lines) for 3D plotting
    """
    x_lines, y_lines, z_lines = [], [], []
    for t in range(TIME_STEPS):
        # Generate coordinate sequences with None separators between bones
        x_t = sum(([coordinates[t]['x'][i] if coordinates[t]['x'][i] != 0.0 else None
                  for i in conn] + [None] for conn in connections), [])[:-1]

        y_t = sum(([coordinates[t]['y'][i] if coordinates[t]['x'][i] != 0.0 else None
                  for i in conn] + [None] for conn in connections), [])[:-1]

        z_t = sum(([coordinates[t]['z'][i] if coordinates[t]['x'][i] != 0.0 else None
                  for i in conn] + [None] for conn in connections), [])[:-1]

        x_lines.append(x_t)
        y_lines.append(y_t)
        z_lines.append(z_t)
    return x_lines, y_lines, z_lines


# Create 3D figures for each athlete
for athlete_idx in range(7):
    coordinates = json.loads(bone_data[athlete_idx])
    x_lines, y_lines, z_lines = process_coordinates(
        coordinates, BONE_CONNECTIONS)

    # Create animation frames
    frames = [
        go.Frame(
            data=[go.Scatter3d(
                x=x_lines[t], y=y_lines[t], z=z_lines[t],
                mode='lines+markers',
                line=dict(color='red', width=3),
                marker=dict(size=4, color='green')
            )],
            name=f"frame_{t}"
        ) for t in range(TIME_STEPS)
    ]

    # Initialize figure
    fig = go.Figure(
        data=[go.Scatter3d(
            x=x_lines[0], y=y_lines[0], z=z_lines[0],
            mode='lines+markers',
            line=dict(color='red', width=3),
            marker=dict(size=4, color='green')
        )],
        layout=go.Layout(
            title="Skeletal Motion Visualization",
            scene=dict(
                xaxis=dict(title='X Axis'),
                yaxis=dict(title='Y Axis'),
                zaxis=dict(title='Z Axis'),
                camera=dict(eye=dict(x=1, y=-2, z=0.3))  # Initial view angle
            )
        ),
        frames=frames
    )
    figs.append(fig)

# Dashboard layout ------------------------------------------------------------
app.layout = html.Div(
    className="main-container",
    children=[
        # Visualization and video section
        html.Div(
            className="visualization-section",
            children=[
                html.Div(
                    id='athlete-info-panel',
                    children="Select an athlete to view details",
                    style={'marginTop': '20px', 'fontSize': '18px'}
                ),
                html.Div(
                    className="graph-container",
                    children=[
                        dcc.Graph(
                            id='3d-visualization',
                            figure=figs[0],
                            config={'responsive': True}
                        ),
                        dcc.RadioItems(
                            id='athlete-selector',
                            options=[
                                {'label': f'A0{i+1}', 'value': i}
                                for i in range(7)
                            ],
                            value=0,
                            inline=True,
                            labelStyle={'margin-right': '15px'}
                        )
                    ]
                ),
                html.Video(
                    id="motion-video",
                    controls=True,
                    src=VIDEO_PATH,
                    autoPlay=False,
                    loop=True,
                    muted=True,
                    style={"width": "600px", "borderRadius": "8px"}
                )
            ]
        ),

        # Control panel
        html.Div(
            className="control-section",
            children=[
                # Timeline controls
                html.Div(
                    className="timeline-controls",
                    children=[
                        dcc.Slider(
                            id='frame-slider',
                            min=0,
                            max=TIME_STEPS-1,
                            step=1,
                            value=0,
                            marks={i: str(i) for i in range(0, 121, 30)},
                            tooltip={"placement": "bottom"}
                        ),
                        dcc.Interval(
                            id='animation-timer',
                            interval=35,  # ~28.5fps (1000/35)
                            n_intervals=0,
                            disabled=False
                        )
                    ]
                ),

                # Playback controls
                html.Div(
                    className="playback-controls",
                    children=[
                        html.Button(
                            "▶️",
                            id="play-pause-btn",
                            n_clicks=0,
                            className="control-btn"
                        ),
                        dcc.Dropdown(
                            id="speed-control",
                            options=[
                                {"label": "0.25X", "value": 0.25},
                                {"label": "0.5X", "value": 0.5},
                                {"label": "1.0X", "value": 1.0},
                                {"label": "1.5X", "value": 1.5}
                            ],
                            value=1.0,
                            clearable=False,
                            className="speed-selector"
                        ),
                        html.Button(
                            "Sync",
                            id="sync-btn",
                            className="control-btn",
                            title="Synchronize video with animation"
                        ),
                        # Video frame data storage
                        dcc.Store(id="video-frame-store")
                    ]
                )
            ]
        )
    ]
)

# Callback functions ----------------------------------------------------------


@app.callback(
    Output('frame-slider', 'value'),
    [Input('animation-timer', 'n_intervals'),
     Input('sync-btn', 'n_clicks'),
     State('frame-slider', 'value'),
     State('video-frame-store', 'data')]
)
def update_slider(n_intervals, sync_clicks, current_frame, video_frame):
    """Update slider position based on animation or video sync
    Args:
        n_intervals: Timer trigger count
        sync_clicks: Sync button clicks
        current_frame: Current slider value
        video_frame: Video frame data from store
    Returns:
        Updated frame index
    """
    ctx = dash.callback_context
    if not ctx.triggered:
        return 0

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'sync-btn':
        return video_frame or 0
    elif trigger_id == 'animation-timer':
        return (current_frame + 1) % TIME_STEPS
    return current_frame


@app.callback(
    Output('athlete-info-panel', 'children'),
    [Input('athlete-selector', 'value'),
     Input('frame-slider', 'value')]
)
def update_athlete_info(athlete_id, frame):
    """Display athlete information and performance data
    Args:
        athlete_id: Selected athlete ID
        frame: Current animation frame
    Returns:
        Formatted athlete information HTML components
    """
    athlete_key = f"A0{athlete_id + 1}"
    info = athlete_data.get(athlete_key, "Information unavailable")

    # Simulated performance data (replace with actual API call)
    speed = random.uniform(8.5, 12.5)  # Demo random speed

    return html.Div([
        html.H3(f"Athlete {athlete_key} Profile"),
        html.P(info),
        html.P(f"Current speed: {speed:.2f} m/s (Frame {frame})")
    ])


@app.callback(
    Output('animation-timer', 'interval'),
    Input('speed-control', 'value')
)
def adjust_playback_speed(speed):
    """Adjust animation playback speed
    Args:
        speed: Selected speed multiplier
    Returns:
        Updated interval duration in milliseconds
    """
    speed_mapping = {
        0.25: 140,   # 140ms = ~7fps
        0.5: 70,     # 70ms = ~14fps
        1.0: 35,     # 35ms = ~28.5fps
        1.5: 23      # 23ms = ~43fps
    }
    return speed_mapping.get(speed, 35)


@app.callback(
    Output('3d-visualization', 'figure'),
    [Input('frame-slider', 'value'),
     Input('athlete-selector', 'value')]
)
def update_3d_visualization(frame, athlete_id):
    """Update 3D visualization to specified frame
    Args:
        frame: Target frame index
        athlete_id: Selected athlete ID
    Returns:
        Updated Plotly figure object
    """
    fig = figs[athlete_id]
    fig.update_traces(
        x=fig.frames[frame].data[0].x,
        y=fig.frames[frame].data[0].y,
        z=fig.frames[frame].data[0].z,
        marker=dict(color='blue' if athlete_id % 2 else 'red')
    )
    return fig


@app.callback(
    Output('animation-timer', 'disabled'),
    Output('play-pause-btn', 'children'),
    Input('play-pause-btn', 'n_clicks')
)
def toggle_playback_state(n_clicks):
    """Toggle animation play/pause state
    Args:
        n_clicks: Button click count
    Returns:
        Tuple: (timer_disabled_state, button_label)
    """
    is_paused = n_clicks % 2 == 0
    return (not is_paused, "⏸️") if is_paused else (is_paused, "▶️")


# Client-side callback (JavaScript integration) -------------------------------
app.clientside_callback(
    """
    function syncVideoWithSlider(video_id) {
        const videoElement = document.getElementById(video_id);
        if (!videoElement) return null;

        const FRAMES_PER_SECOND = 33.3;  // Video frame rate
        return new Promise(resolve => {
            videoElement.addEventListener('timeupdate', () => {
                const currentFrame = Math.min(
                    Math.floor(videoElement.currentTime * FRAMES_PER_SECOND),
                    TIME_STEPS - 1
                );
                resolve(currentFrame);
            });
        });
    }
    """,
    Output('video-frame-store', 'data'),
    Input('motion-video', 'id')
)

# Application execution -------------------------------------------------------
if __name__ == '__main__':
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=int(port))
