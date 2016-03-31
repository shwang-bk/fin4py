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
import datetime
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from pandas import Series
from pandas_datareader import data as pda
from matplotlib.dates import date2num
from matplotlib.dates import num2date
from matplotlib.finance import candlestick_ochl
from matplotlib.finance import volume_overlay3

class Stock:
    def __init__(self, stock_id, start_date = None, end_date = None):
        self.df = None
        
        try:
            self.df = pda.get_data_yahoo(stock_id + u'.TW', start_date, end_date)
        except:
            pass
        
        if self.df is None:
            try:
                self.df = pda.get_data_yahoo(stock_id + u'.TWO', start_date, end_date)
            except:
                pass
            
        if self.df is None:
            try:
                self.df = pda.get_data_yahoo(stock_id, start_date, end_date)
            except:
                print("KEY_ERROR: Wrong stock id.")
                raise

        self.df = self.df[self.df.Volume != 0]

    def __getitem__(self, key):
        return self.df[key]

    def __setitem__(self, key, value):
        self.df[key] = value

    def __repr__(self):
        return repr(self.df)
    
    def MA(self, window = 5):
        return self.df['Adj Close'].rolling(window, center=False).mean()

    def MA_Volume(self, window = 5):
        return self.df['Volume'].rolling(window, center=False).mean()

    def KD(self, window = 9):
        df_min = self.df['Low'].rolling(window, center=False).min()
        df_max = self.df['High'].rolling(window, center=False).max()
        df_RSV = (self.df['Adj Close'] - df_min) / (df_max - df_min) * 100

        K = []
        curr_K = 50
        for rsv in df_RSV:
            if pd.isnull(rsv):
                K.append(rsv)
                continue
            curr_K = rsv * (1.0/3) + curr_K  * (2.0/3)
            K.append(curr_K)

        df_K = Series(K, df_RSV.index)

        D = []
        curr_D = 50
        for k in df_K:
            if pd.isnull(k):
                D.append(k)
                continue
            curr_D = k * (1.0/3) + curr_D  * (2.0/3)
            D.append(curr_D)

        df_D = Series(D, df_RSV.index)

        return df_K, df_D

    def MACD(self, s_window = 12, l_window = 26, dif_window = 9):
        EMA_short = self.df['Adj Close'].ewm(span=s_window).mean()
        EMA_long = self.df['Adj Close'].ewm(span=l_window).mean()

        DIF = EMA_short - EMA_long
        DEM = DIF.ewm(span=dif_window).mean()

        OSC = DIF - DEM

        return DIF, DEM, OSC

    def BIAS(self, window = 10):
        ma = self.MA(window)
        return (self.df['Adj Close'] - ma) / ma * 100

    def BBand(self, window = 20, band = 2):
        ma = self.MA(window)
        stdiv = self.df['Adj Close'].rolling(window).std()
        
        top = ma + band * stdiv
        bottom = ma - band * stdiv
        width = band * 2 * stdiv / self.df['Adj Close']
        
        return top, bottom, width
    
    def getData(self, i):
        return self.df.iloc[i]

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        timestemps = self.df.index.date
        candlesticks = zip(date2num(timestemps), self.df['Open'], self.df['Adj Close'],
            self.df['High'], self.df['Low'], self.df['Volume'])
        candlestick_ochl(ax, candlesticks,width=1,colorup='r', colordown='g')

        pad = 0.25
        yl = ax.get_ylim()
        ax.set_ylim(yl[0]-(yl[1]-yl[0])*pad,yl[1])

        #ax2 = ax.twinx()
        #ax2.set_position(matplotlib.transforms.Bbox([[0.125,0.1],[0.9,0.32]]))

        #dates = [x[0] for x in candlesticks]
        #dates = np.asarray(dates)
        #volume = [x[5] for x in candlesticks]
        #volume = np.asarray(volume)

        #pos = self.df['Open']-self.df['Adj Close']<0
        #neg = self.df['Open']-self.df['Adj Close']>0
        #ax2.bar(dates[pos],volume[pos],color='green',width=1,align='center')
        #ax2.bar(dates[neg],volume[neg],color='red',width=1,align='center')

        #ax2.set_xlim(min(dates),max(dates))

        #yticks = ax2.get_yticks()
        #ax2.set_yticks(yticks[::3])

        #ax2.yaxis.set_label_position("right")
        #ax2.set_ylabel('Volume', size=20)

        xt = ax.get_xticks()
        new_xticks = [datetime.date.isoformat(num2date(d)) for d in xt]
        ax.set_xticklabels(new_xticks,rotation=45, horizontalalignment='right')
        plt.show()