"""
MAKING A PLOT MORE PLEASING
We did make a plot, but we have some unnecessary granulation on the y-axis, we need to get rid of that.
HOVER - We want to show the exact time when we point the mouse pointer is over the quadrant box (pop-up)
    we import the HoverTool from bokeh.models
    we make a hower pop-up window using a list of tuples, every tuple is a new row, you type the name
      of the value and "@___"(column in a DF), and you add that tool:
            hover = HoverTool(tooltips=[("Start", "@Start"), ("End", "@End")])
            p.add_tools(hover)
    in some cases the values of the df can't be took, so instead of an datafrae, we use ColumnDataSource:

            from bokeh.models import HoverTool, ColumnDataSource

            cds = ColumnDataSource(df)

            q = p.quad(left="Start", right="End", bottom=0, top=1, color="green", source=cds)

    the hover tool method is not able to fetch the datatypes, so we convert datatype to strings:
            df["Start_string"]=df["Start"].df.strftime("%Y-%m-%d %H:%M:%S")
            df["End_string"]=df["End"].df.strftime("%Y-%m-%d %H:%M:%S")
"""
from motion_detector4 import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df["Start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)

p = figure(x_axis_type='datetime', height=100, width=500, sizing_mode="scale_width", title="Motion Graph")
p.yaxis.minor_tick_line_color=None
p.yaxis.ticker.desired_num_ticks=1

hover = HoverTool(tooltips=[("Start", "@Start_string"), ("End", "@End_string")])
p.add_tools(hover)

q = p.quad(left="Start", right="End", bottom=0, top=1, color="green", source=cds)

output_file("Graph.html")
show(p)



