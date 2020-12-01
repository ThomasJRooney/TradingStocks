# sample of how a backtrading strategy must be set up to be tested

# import modules
import backtrader

# instantiate class
class TurtleTrader(backtrader.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None
        self.lows = []

    def get_20dma(self):
        data = yf.download(self.symbol, '2020-01-01', '2020-02-09')
        data = data[-20:]
        return numpy.mean(data, axis = None)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED {}".format(order.executed.price))
            elif order.issell():
                self.log("SELL EXECUTED {}".format(order.executed.price))
            self.bar_executed = len(self)
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        print(len(self))
        print(self.order)
        print(self.position)

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.buy()
        else:
            if len(self) >= (self.bar_executed + 2):
                self.log("SELL CREATED {}".format(self.dataclose[0]))
                self.order = self.sell()