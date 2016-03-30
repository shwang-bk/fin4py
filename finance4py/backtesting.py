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

from pandas import DataFrame
from pandas import Series
import numpy as np

class BandTest:
    def __init__(self, stock):
        self.stock = stock
        self.df = stock.df
        self.i_table = DataFrame(index = self.df.index)
        
    def addStrategy(self, name, strategy):
        signals = [(1 if strategy(i, self.df.iloc[i], self.stock) else 0) for i in range(self.df['Adj Close'].count())]
        signal = Series(signals, self.df.index)

        close = self.df['Adj Close']
        unit_income = np.log(close / close.shift(1)) * signal.shift(1)
        self.i_table[name] = np.exp(unit_income.cumsum())
        
    def plot(self):
        self.i_table.plot()