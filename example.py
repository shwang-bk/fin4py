# -*- coding: utf-8 -*-

from TechnicalAnalysis import Stock
import matplotlib.pyplot as plt

if __name__ == '__main__':
	# 建立股票資訊連結(股票代碼，起始時間，結束時間)
	# s = Stock('2330')
	# s = Stock('2330', '10/31/2015')
	s = Stock('2330', '10/31/2015', '03/05/2016')

	# 取得歷史股價
	history = s.history()
	print("歷史收盤價")
	print(history['Adj Close'])

	# 取得均線值(預設週期為5日)
	# ma = s.MA(5)
	ma = s.MA()
	history['MA5'] = ma

	# 取得KD值(預設週期為9日)
	# k, d = s.KD(9)
	k, d = s.KD()
	history['K'] = k
	history['D'] = d

	# 取得MACD值(預設短週期為12日，長週期為26日，DIF平滑區間為9日)
	# 詳情可至維基百科查詢 https://zh.wikipedia.org/wiki/MACD
	# dif, dem, osc = s.MACD(12, 26, 9)
	dif, dem, osc = s.MACD()
	history['DIF'] = dif
	history['DEM'] = dem
	history['OSC'] = osc
	
	# 取得乖離率(預設週期為10日)
	# bias = s.BIAS(10)
	bias = s.BIAS()
	history['BIAS'] = bias

	print("歷史股價及技術線圖表")
	print(history)

	# 繪製技術線型
	plt.figure(figsize=(8,4))

	# ma.plot()
	k.plot()
	d.plot()
	# dif.plot()
	# dem.plot()
	# osc.plot.bar()
	# bias.plot()

	plt.show()

