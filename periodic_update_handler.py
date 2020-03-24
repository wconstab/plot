import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.application.handlers.handler import Handler
from bokeh.application.application import Application
from bokeh.server.server import Server



class PeriodicUpdateHandler(Handler):
    def __init__(self):
        super(PeriodicUpdateHandler, self).__init__()
        self.df = pd.DataFrame(columns=('x','y'))
        self.n = 50
        self.period_ms = 500

    def modify_document(self, doc):
        source = ColumnDataSource(self.df)
        p = figure()
        p.scatter('x','y', source=source, alpha=0.5)

        def callback():
            sample = np.random.multivariate_normal([0,0], [[1,0],[0,1]], self.n)
            df_new = pd.DataFrame(sample, columns=('x','y'))
            source.stream(df_new, 10*self.n)

        doc.add_root(p)
        doc.add_periodic_callback(callback, self.period_ms)

bkapp = Application(PeriodicUpdateHandler())
server = Server({'/': bkapp})
server.start()

if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')

    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()