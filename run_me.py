from bokeh.plotting import figure, show, output_file
from motion_detector import df
from bokeh.models import HoverTool, ColumnDataSource

df["Start_time"] = df['Start'].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_time"] = df['End'].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)

f = figure(width=1400, height=500, title='Motion Graph', x_axis_type='datetime')
f.yaxis.minor_tick_line_color = None
# f.ygrid[0].ticker.desired_num_ticks = 1

hover = HoverTool(tooltips=[("Start","@Start_time"),("End","@End_time")])
f.add_tools(hover)

quad =  f.quad(left="Start", right="End", bottom=0, top=1, color='green', source=cds)

output_file('graph.html')
show(f)