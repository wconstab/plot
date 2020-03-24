from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.server.server import Server
from bokeh.themes import Theme
from bokeh.application.handlers.handler import Handler
from bokeh.application.application import Application

class MyHandler(Handler):
    def __init__(self):
        super(MyHandler, self).__init__()
        self.safe_to_fork = True
        self.df = sea_surface_temperature.copy()
        self.source = ColumnDataSource(data=self.df)

    def modify_document(self, doc):
        self.safe_to_fork = False

        plot = figure(x_axis_type='datetime', y_range=(0, 25), y_axis_label='Temperature (Celsius)',
                    title="Sea Surface Temperature at 43.18, -70.43")
        plot.line('time', 'temperature', source=self.source)

        def callback(attr, old, new):
            if new == 0:
                data = self.df
            else:
                data = self.df.rolling('{0}D'.format(new)).mean()
            self.source.data = ColumnDataSource.from_df(data)

        slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
        slider.on_change('value', callback)

        doc.add_root(column(slider, plot))


# Setting num_procs here means we can't touch the IOLoop before now, we must
# let Server handle that. If you need to explicitly handle IOLoops then you
# will need to use the lower level BaseServer class.
handler = MyHandler()
server = Server({'/': Application(handler)}, num_procs=1)
server.start()

if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')

    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()