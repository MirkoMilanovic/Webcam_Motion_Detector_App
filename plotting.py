"""
MAKING A PLOT:
First we need to think of the structure of our script. We need to think about:
- which plot to use? ...We will use quadrant
- what are the input parameters? ...We have them in a dataframe with datetimes (which we save to csv)

We decide to do plotting in a separate script, so we import specific values from the other script (df), so
the main program would be "plotting.py" which will start the "motion_detector4.py" and get a df from it.
"""
from motion_detector4 import df
from bokeh.plotting import figure, show, output_file

p = figure(x_axis_type='datetime', height=100, width=500, sizing_mode="scale_width", title="Motion Graph")

q = p.quad(left=df["Start"], right=df["End"], bottom=0, top=1, color="green")

output_file("Graph.html")
show(p)

