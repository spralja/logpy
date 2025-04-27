from logpy.controller import ExcelController

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Simulate log file reading function (you should replace this with actual log reading logic)
def read_log():
    # This function should read the log file and return the academic and work durations
    # In this example, it's just a simulation with some dummy data
    
    current_time = time.strftime("%H:%M:%S", time.localtime())
    
    # Simulated values from a log file (replace with your actual log reading logic)

    LOG_PATH  = '/Users/spralja/Library/CloudStorage/OneDrive-Personal/log'

    START = datetime.fromisocalendar(2022, 37, 1).replace(tzinfo=timezone.utc)

    controller = ExcelController(Path(LOG_PATH))


    def get_weeks_entries(year, week):
        start_of_week = datetime.fromisocalendar(year, week, 1).replace(tzinfo=timezone.utc)
        end_of_week = start_of_week + timedelta(days=7)

        weeks_entries = controller.get_intersection(start_of_week, end_of_week)

        return weeks_entries

    weeks_entries = get_weeks_entries(2025, 17)

    academic_total_duration = timedelta(0)
    work_total_duration = timedelta(0)
    dtu_act_total_duration = timedelta(0)

    for entry in weeks_entries:
        if entry.category == 'Academic':
            academic_total_duration += entry.duration
        
        if entry.category == 'Work':
            work_total_duration += entry.duration

        if entry.description == 'DTU ACT':
            dtu_act_total_duration += entry.duration
    
    
    academic_total_duration = academic_total_duration.total_seconds() / 3600
    work_total_duration = work_total_duration.total_seconds() / 3600
    dtu_act_total_duration = dtu_act_total_duration.total_seconds() / 3600


    academic_total_duration = academic_total_duration  # Placeholder, replace with log reading
    work_total_duration = work_total_duration      # Placeholder, replace with log reading
    
    print(f"Log checked at {current_time} - Academic: {academic_total_duration} hrs, Work: {work_total_duration} hrs")
    return round(academic_total_duration, 2), round(work_total_duration, 2), round(dtu_act_total_duration, 2)

# Create a Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Weekly Productivity: Work and Academic"),
    
    # Pie chart output
    dcc.Graph(id='productivity-pie-chart'),

    # Interval component to trigger the callback every 5 minutes (300000 ms)
    dcc.Interval(
        id='interval-component',
        interval=60000,  # 300,000 milliseconds = 5 minutes
        n_intervals=0  # Start at the first interval
    )
])

# Callback to update the pie chart dynamically based on log file
@app.callback(
    Output('productivity-pie-chart', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_pie_chart(n):
    # Call the log reading function to get updated values
    academic_hours, work_hours, dtu_act_hours = read_log()
    
    # Max possible hours in a week
    max_hours = 37.5

    # Data for the pie chart
    labels = ['Academic', 'Work', 'DTU ACT', 'Remaining']
    durations = [academic_hours, work_hours,dtu_act_hours ,max_hours - (academic_hours + work_hours+dtu_act_hours)]
    durations = [d if d > 0 else 0 for d in durations]  # Handle negative values

    # Create the pie chart using Plotly
    fig = go.Figure(
        data=[go.Pie(labels=labels, values=durations, hole=0.4, 
                     textinfo='label+value', 
                     hoverinfo='label+value')]
    )
    
    fig.update_layout(title_text="Weekly Productivity Distribution", title_x=0.5)
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
    




    def P1(x, w, sp, R1):

        
        print(sp, R1)