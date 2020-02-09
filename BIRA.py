from datetime import datetime
import backtrader as bt

ADX = 25
QTY = 5


class BiraStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def _init_(self):
        self.adx = bt.ind.ADX()
        self.dmiplus, self.dmimin = bt.ind.PlusDI(), bt.ind.MinusDI()
        self.dmi = bt.ind.DMI()
        self.crossoverdmi = bt.ind.CrossOver(self.dmimin, self.dmiplus)
        self.ich = bt.ind.Ichimoku()
        self.rsi = bt.ind.RelativeStrengthIndex()
        self.crossover = bt.ind.CrossOver(self.data0, self.ich.l.tenkan_sen)


    def next(self):
        print(self.datas[0].datetime.date(0))

        self.tenkan_sen = self.ich.l.tenkan_sen[0]
        self.kijun_sen = self.ich.l.kijun_sen[0]
        self.senkou_span_a = self.ich.l.senkou_span_a[0]
        self.senkou_span_b = self.ich.l.senkou_span_b[0]
        self.ichi=self.ich.l.chikou_span[0]
        print(self.tenkan_sen,self.kijun_sen,self.senkou_span_a,self.senkou_span_b)
        print(self.senkou_span_a, self.datas[0].close[0])
        print(self.getsizer())


        if self.dmiplus > self.dmimin and self.adx[0]>25:
            self.buy(size=QTY)
        elif self.datas[0].open > self.ichi or self.rsi>70:
            self.close(size=3*QTY)

        if self.datas[0].datetime.date(0) == datetime(2019, 1, 1).date():
            self.close()



cerebro = bt.Cerebro(stdstats=False)
cerebro.addobserver(bt.observers.BuySell)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('Starting Portfolio Cash: %.2f' % cerebro.broker.get_cash())

cerebro.addstrategy(BiraStrategy)
cerebro.adddata(bt.feeds.YahooFinanceData(dataname='^NSEI', fromdate=datetime(2013, 1, 1), todate=datetime(2019, 1, 2)))
cerebro.broker.set_cash(200000)
cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('Final Portfolio Cash: %.2f' % cerebro.broker.get_cash())

cerebro.plot()