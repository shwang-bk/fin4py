# -*- coding: utf-8 -*-
'''
 * finance4py
 * Based on Python Data Analysis Library.
 * 2016/03/22 by Sheg-Huai Wang <m10215059@csie.ntust.edu.tw>


 * Copyright (c) 2016, finance4py team   
 * All rights reserved.   

 * Redistribution and use in source and binary forms, with or without modification, 
   are permitted provided that the following conditions are met:   

 1. Redistributions of source code must retain the above copyright notice, 
    this list of conditions and the following disclaimer.   
 2. Redistributions in binary form must reproduce the above copyright notice, 
    this list of conditions and the following disclaimer in the documentation and/or 
    other materials provided with the distribution.   
 3. Neither the name of the copyright holder nor the names of its contributors may be used to 
    endorse or promote products derived from this software without specific prior written permission.   

 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS 
   OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
   AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
   DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER 
   IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF 
   THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

from finance4py import Stock
import matplotlib.pyplot as plt

if __name__ == '__main__':
	# 建立股票資訊連結(股票代碼，起始時間，結束時間)
	# s = Stock('2330')
	# s = Stock('2330', '10/31/2015')
	s = Stock('2330', '10/31/2015', '03/05/2016')

	# 取得歷史股價
	print('歷史收盤價')
	print(s['Adj Close'])

	# 取得均線值(預設週期為5日)
	# ma = s.MA(5)
	ma = s.MA()
	s['MA5'] = ma

	# 取得KD值(預設週期為9日)
	# k, d = s.KD(9)
	k, d = s.KD()
	s['K'] = k
	s['D'] = d

	# 取得MACD值(預設短週期為12日，長週期為26日，DIF平滑區間為9日)
	# 詳情可至維基百科查詢 https://zh.wikipedia.org/wiki/MACD
	# dif, dem, osc = s.MACD(12, 26, 9)
	dif, dem, osc = s.MACD()
	s['DIF'] = dif
	s['DEM'] = dem
	s['OSC'] = osc
	
	# 取得乖離率(預設週期為10日)
	# bias = s.BIAS(10)
	bias = s.BIAS()
	s['BIAS'] = bias

	# 取得布林通道值(預設週期為20日, 通道倍率為2倍)
	# top_line, bottom_line, band_width = s.BBand(20, 2)
	top_line, bottom_line, band_width = s.BBand()
	s['BTOP'] = top_line
	s['BBOTTOM'] = bottom_line
	s['BWIDTH'] = band_width

	print('歷史股價及技術線圖表')
	print(s)

	# 繪製技術線型
	plt.figure(figsize=(8,4))

	s['Adj Close'].plot()
	# ma.plot()
	# k.plot()
	# d.plot()
	# dif.plot()
	# dem.plot()
	# osc.plot.bar()
	# bias.plot()
	top_line.plot()
	bottom_line.plot()
	# band_width.plot()

	plt.show()

