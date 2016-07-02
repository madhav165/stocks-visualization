#!/usr/bin/env/ python3

import get_stocks as gs
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy as np

def bytesupdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter (b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

def read_csv(file_name):
   print ('Reading %s' % file_name)
   date, openp, highp, lowp, closep, volume, adjclosep = np.loadtxt(file_name, 
                                                                    delimiter=',', 
                                                                    unpack=True,
                                                                    converters={0:bytesupdate2num('%Y-%m-%d')},
                                                                    skiprows=1
                                                                   )

if __name__=='__main__':
    symbol=gs.get_going()
    file_name=symbol+'.csv'
    read_csv(file_name)
