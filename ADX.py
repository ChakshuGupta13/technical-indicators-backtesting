from datetime import datetime
import backtrader as bt

ADX = 25
QTY = 1


class ADXDMICross(bt.Strategy):

    def __init__(self):
        self.adx = bt.ind.ADX()
        self.dmiplus, self.dmimin = bt.ind.PlusDI(), bt.ind.MinusDI()
        self.crossoverdmi = bt.ind.CrossOver(self.dmimin, self.dmiplus)

    def next(self):
        #     if self.crossoverdmi[0] == -1.0 and self.adx[0] > ADX:
        if self.dmiplus > self.dmimin and self.adx[0] > ADX:
            self.buy(size=QTY)
        #     if self.datas[0].datetime.date(0) == datetime(2020, 1, 23).date():
        if self.dmiplus < self.dmimin and self.adx[0] > ADX:
            self.close(size=QTY)

        if self.datas[0].datetime.date(0) == datetime(2020, 1, 23).date():
            self.close()


cerebro = bt.Cerebro(stdstats=False)
cerebro.addobserver(bt.observers.BuySell)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('Starting Portfolio Cash: %.2f' % cerebro.broker.get_cash())
cerebro.addstrategy(ADXDMICross)
data0 = bt.feeds.YahooFinanceData(dataname="GOOGL", fromdate=datetime(2016, 8, 1),
                                  todate=datetime(2020, 1, 30))
cerebro.adddata(data0)
cerebro.broker.set_cash(200000)
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('Final Portfolio Cash: %.2f' % cerebro.broker.get_cash())
cerebro.plot()
