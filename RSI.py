from datetime import datetime
import backtrader as bt


class RelativeStrengthIndexStrategy(bt.SignalStrategy):
    def __init__(self):
        self.index = bt.ind.RelativeStrengthIndex()

    def next(self):
        if self.index < 40 and self.datas[0].close[0] > self.datas[-1].close[-1]:
            self.buy(size=0.5)

        elif self.index > 70 and self.datas[0].close[0] < self.datas[-1].close[-1]:
            self.close(size=0.5)

        if self.datas[0].datetime.date(0) == datetime(2020, 1, 29).date():
            self.close()


cerebro = bt.Cerebro(stdstats=False)
cerebro.addobserver(bt.observers.BuySell)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('Starting Portfolio Cash: %.2f' % cerebro.broker.get_cash())
cerebro.addstrategy(RelativeStrengthIndexStrategy)
data0 = bt.feeds.YahooFinanceData(dataname='^NSEI', fromdate=datetime(2016, 1, 1),
                                  todate=datetime(2020, 1, 30))

cerebro.adddata(data0)
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('Final Portfolio Cash: %.2f' % cerebro.broker.get_cash())
cerebro.plot()
