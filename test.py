#!/usr/bin/env/ python3

import get_stocks as gs
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
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
    return date, openp, highp, lowp, closep, volume, adjclosep

def plot_data(symbol, date, openp, highp, lowp, closep, volume, adjclosep):
    style.use('ggplot')
    ax1 = plt.subplot2grid((1,1), (0,0), rowspan=1, colspan=1)
    plt.plot(date,adjclosep, label='Adjusted closing price')
    plt.ylabel('Adjusted Closing Price')
    plt.title(symbol)
    #plt.legend()
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    plt.subplots_adjust(left=0.09,bottom=0.15,right=0.94,top=0.92,wspace=0.2, hspace=0)
    plt.show()

if __name__=='__main__':
    symbol=gs.get_going()
    file_name=symbol+'.csv'
    date, openp, highp, lowp, closep, volume, adjclosep=read_csv(file_name)
    plot_data(symbol, date, openp, highp, lowp, closep, volume, adjclosep)
