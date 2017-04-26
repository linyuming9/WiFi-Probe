# -*- coding: utf-8 -*-

import fileinput
import zipfile
import time
import os

def get_rss(line):
    db = "dB"
    rss_exists = line.find(db.upper())
    if(rss_exists >= 0):
        return line[rss_exists-3:rss_exists+len(db)]
    return "-99DB"

def get_mac_source(line):
    mac_length = 20
    mac_source = line.find("SA:")
    if(mac_source >= 0):
        return line[mac_source:mac_source+mac_length]
    return ""

def get_mac_destination(line):
    mac_length = 20
    mac_source = line.find("DA:")
    if(mac_source >= 0):
        return line[mac_source:mac_source+mac_length]
    return ""

def print_data(line):
    data = line.split(" ")
    date = data[0]
    time = data[1][0:8]
    
    rss = get_rss(line)
    mac_source = get_mac_source(line)
    mac_dest = get_mac_destination(line)
    
    return(date + " " + time + "," + mac_source + "," + mac_dest + "," + rss)

def zip_file(srcFile,dstname):
    cnt = 0
    while os.path.exists(dstname+'.zip'):
        dstname = dstname.split('v')[0] + 'v%s'%cnt
        cnt += 1
    dstname = dstname + '.zip'
    zipFile = zipfile.ZipFile(dstname,'a',zipfile.ZIP_DEFLATED)
    zipFile.write(srcFile)
    zipFile.close()
    
    os.remove(srcFile)
    
def main():
    pre = ""
    path = "/mnt/usb/"
    o = open("/mnt/usb/openinfo.txt","a",0)
    o.write(time.strftime("%F-%H-%M-%S") +' boot\n')
    
    for file in os.listdir(path):
        if (file[-4:] == '.txt') and (file[:-4] != 'openinfo'):
            zip_file(filename, filename[:-4])
            o.write(time.strftime("%F-%H-%M-%S") + ' zip ' + filename + '\n')
            
    filename = "/mnt/usb/record_"+ time.strftime("%F-%H-%M-%S")+ '.txt'
    f = open(filename,"a",0)
    o.write(time.strftime("%F-%H-%M-%S") +' record ' + filename + '\n')
    
    cnt = 0
    while(True):
        for line in fileinput.input():
            cnt += 1
            if cnt == 3000000:
                f.close()
                zip_file(filename, filename[:-4])
                o.write(time.strftime("%F-%H-%M-%S") + ' zip ' + filename + '\n')
                
                filename = "/mnt/usb/record_"+ time.strftime("%F-%H-%M-%S")+ '.txt'
                f = open(filename,"a",0)
                o.write(time.strftime("%F-%H-%M-%S") +' record ' + filename + '\n')
                cnt = 0
                
            l = line.upper()
            rec = print_data(l)
            if rec[0:-5] != pre:
                f.write(rec + '\n')
            pre = rec[0:-5]
    f.close()
    o.close()
    
if __name__ =='__main__' :
    main();
