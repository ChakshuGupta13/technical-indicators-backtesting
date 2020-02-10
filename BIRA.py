from datetime import datetime
import backtrader as bt

ADX = 25
QTY = 5


class IchimokuCrossStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.correct_ctr_sell = 0
        self.buy_ctr = 0
        self.correct_ctr_buy = 0
        self.sell_ctr = 0

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
        self.ichi = self.ich.l.chikou_span[0]
        if self.dmiplus > self.dmimin and self.adx[0] > 25 or self.datas[0].open < self.ichi and self.senkou_span_a > self.senkou_span_b :
            self.buy_ctr += 1
            self.buy(size=QTY)
            self.decision = "BUY"
            try:
                if self.datas[0].open[1] >= self.datas[0].open[0]:
                    self.correct_ctr_buy += 1
            except:
                pass
        elif self.datas[0].open > self.ichi and self.senkou_span_a < self.senkou_span_b or self.dmiplus < self.dmimin and self.adx[0] > 25 :
            self.sell_ctr += 1
            self.decision = "SELL"
            try:
                if self.datas[0].open[0] >= self.datas[0].open[1]:
                    self.correct_ctr_sell += 1
            except:
                pass
            self.sell(size=QTY)

        if self.datas[0].datetime.date(0) == datetime(2019, 1, 1).date():
            self.close()
        print(self.buy_ctr, self.correct_ctr_buy,
              self.sell_ctr, self.correct_ctr_sell)
        try:
            print("Accuracy %.2f" % (100*(self.correct_ctr_sell +
                                          self.correct_ctr_buy) / (self.buy_ctr + self.sell_ctr)))
        except:
            pass


cerebro = bt.Cerebro(stdstats=False)
cerebro.addobserver(bt.observers.BuySell)
cerebro.broker.set_cash(200000)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('Starting Portfolio Cash: %.2f' % cerebro.broker.get_cash())
cerebro.addstrategy(IchimokuCrossStrategy)
data0 = bt.feeds.YahooFinanceData(dataname='MSFT', fromdate=datetime(2016, 8, 1),
                                  todate=datetime(2020, 1, 25))

cerebro.adddata(data0)

cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('Final Portfolio Cash: %.2f' % cerebro.broker.get_cash())

cerebro.plot()
