import pandas as pd
from pandas import Series
from pandas_datareader import data as pda
import numpy as np

class Stock:
    def __init__(self, stock_id, start_date = None, end_date = None):
        self.df = None
        
        try:
            self.df = pda.get_data_yahoo(stock_id, start_date, end_date)
        except:
            pass
        
        if self.df is None:
            try:
                self.df = pda.get_data_yahoo(stock_id + u'.TW', start_date, end_date)
            except:
                pass
            
        if self.df is None:
            try:
                self.df = pda.get_data_yahoo(stock_id + u'.TWO', start_date, end_date)
            except:
                print("KEY_ERROR: Wrong stock id.")
                raise
                
    def history(self):
        return self.df
    
    def MA(self, window = 5):
        return self.df['Adj Close'].rolling(window, center=False).mean()

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