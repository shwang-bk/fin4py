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
from finance4py.backtesting import BandTest
from pylab import *

if __name__ == '__main__':

	# 建立股票資訊連結以及將資訊丟入回測程式
	s = Stock('2330', '10/31/2015', '03/05/2016')
	bt = BandTest(s)

	# 範例策略一
	# 在歷史股價內新增K, D兩個值的欄位
	s['K'], s['D'] = s.KD()

	# 撰寫個人策略 => def 名稱自取(今日, 今日資訊, 股票資訊)
	def golden_cross(today, today_data, stock):
		# 回傳資訊為 True = 持有狀態, False = 非持有狀態
		return today_data['K'] > today_data['D']

	# 將策略新增至回測程式中並取名
	bt.addStrategy('KD黃金交叉', golden_cross)

	# 範例策略二
	s['MA5'] = s.MA()
	s['MA20'] = s.MA(20)

	def average_cross(today, today_data, stock):
		return today_data['MA5'] > today_data['MA20']

	bt.addStrategy('均線黃金交叉', average_cross)

	# 範例策略三
	s['DIF'], s['DEM'],  s['OSC']= s.MACD()

	def macd_cross(today, today_data, stock):
		# 可調整today並透過stock取得其他日的資訊
		yesterday = today - 1
		yesterday_data = stock.getData(yesterday)

		return (today_data['DIF'] > today_data['DEM']) & \
			(yesterday_data['DIF'] > yesterday_data['DEM'])

	bt.addStrategy('MACD連續兩日黃金交叉', macd_cross)

	# 繪製回測結果 (縱軸為資產倍率)
	bt.plot()

	show()