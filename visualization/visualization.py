# coding: utf-8

import subprocess
from threading import Thread
import time
import copy

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
#get_ipython().magic('matplotlib notebook')

# Define a class to save the rssi
class rssi():
    
    def __init__(self, new_rss):
        self.rss = new_rss
        self.cnt = 1
    
    def update(self, new_rss):
        self.rss = (self.rss * self.cnt + new_rss) / (self.cnt + 1)
        self.cnt += 1
        return self
    
    def decay(self):
        self.cnt = 0
        #self.rss -= 0.5
        return self

# Convert rssi object to float value
def convert(rssi):
    try:
        return rssi.rss
    except:
        return rssi

# Read out the packet information
def read_buff(line):
    
    time = line.split(" ")[0] + ' ' + line.split(" ")[1][0:8]
    try:
        time = pd.to_datetime(time)
    except:
        time = None

    source = line.find("SA:")
    if source >= 0:
        source = line[source+3:source+20]
    else:
        source = None
    
    rss = line.find("dB")
    if rss >= 0:
        rss = float(line[rss-3:rss])
    else:
        rss = None
        
    return time, source, rss

# Update the rssi record
def update(record, buff):
    
    if not record.empty:
        time_prev = record.columns[-1]
    else:
        time_prev = None
    
    time, source, rss = read_buff(buff)
    
    if time and rss:
        if source not in record.index:
            ax.scatter(time, rss, c='k', marker='x', alpha=0.2)
            record.loc[source, time] = rssi(rss)
            
        elif time_prev == None or time > time_prev:
            ax.scatter(time, rss, c='k', marker='x', alpha=0.2)
            record.loc[source, time] = rssi(rss)
            
        elif time == time_prev:
            ax.scatter(time, rss, c='k', marker='x', alpha=0.2)
            record.loc[source, time].update(rss)
    
    record = record.fillna(method='ffill', axis=1)
    return record

# Flush the figure
def flush(data):

    #data = data.rolling(5).mean().dropna()
    data = data[:-1]

    if data.empty:
        return None
    data = data.sort_index()
    
    if data.shape[0] > tw:
        for label in data.columns:
            l[label].set_data(data.iloc[-tw:][label].index, data.iloc[-tw:][label].values) 
        ax.set_xlim([data[-tw:].index[-1] - pd.Timedelta('1s') * tw, data[-tw:].index[-1] + pd.Timedelta('1s')])

    else:
        for label in data.columns:
            l[label].set_data(data.loc[:, label].index, data.loc[:, label].values)
        ax.set_xlim([data.index[-1] - pd.Timedelta('1s') * tw, data.index[-1] + pd.Timedelta('1s')])
        
    fig.canvas.draw()
    fig.canvas.flush_events()





# Set up dataframe and figure 
tw = 30
buffer = []
record = pd.DataFrame([])

plt.ion()
plt.style.use('seaborn')

fig = plt.figure(figsize=(8,4))
ax = fig.add_subplot(111)

# Create lines for different mobile device
with open('D:\\OneDrive\\Software\\PUTTY\\tcpdump.txt') as f:
    src = f.read().split('src ')[1].split(' or ')
l = pd.Series([])
c = 'rbgy'
for i in range(len(src)):
    l[src[i]], = ax.plot([],[],label=src[i], c=c[i])

ax.set_ylim([-90, -20])
ax.set_xlabel('System Time')
ax.set_ylabel('Signal Strength (dB)')
ax.legend()

fig.canvas.draw()
fig.canvas.flush_events()





# cmd command to start the tcpdump monitor
cmd = ['./PLINK.EXE',
       'root@192.168.8.1',
       '-pw',
       'sujingmeng',
       '-m',
       './tcpdump.sh']

# Built up a pipe to record the ssh return
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# Set up a thread to read out the stdout buffer
def reader(f,buffer):

    while True:
        line = f.readline().decode('utf-8')
        if line and len(buffer) < 10:
            buffer.append(line)
            
t = Thread(target=reader, args=(p.stdout, buffer))
t.daemon = True
t.start()

while True:
    if buffer:
        print(buffer[0])
        record = update(record, buffer.pop(0))
        data = record.apply(lambda x: x.apply(convert)).T
        flush(data)
        
    else:
        if not record.empty:
            record[record.columns[-1] + pd.Timedelta('1s')] = record.iloc[:, -1].apply(lambda x:copy.deepcopy(x))
            record.iloc[:, -1] = record.iloc[:, -1].apply(lambda x:x.decay())
            
        data = record.apply(lambda x: x.apply(convert)).T
        
        flush(data)
        time.sleep(1)