import fileinput

def find_channel(line):
    mhz = "MHz"
    channel = line.find(mhz.upper())
    if(channel >= 0):
        return line[channel-5:channel-1]
    return ""

def get_rss(line):
    db = "dB"
    rss_exists = line.find(db.upper())
    if(rss_exists >= 0):
        return line[rss_exists-3:rss_exists+len(db)]
    return ""

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
    time = data[1]
    
    rss = get_rss(line)
    mac_source = get_mac_source(line)
    mac_dest = get_mac_destination(line)
    
    return(date + " " + time + " " + rss + " " + mac_source + " " + mac_dest)

def main():
    f = open('/mnt/usb/record','a') #record position

    try:
        while(True):
            for line in fileinput.input():
                l = line.upper()
		print(print_data(l))
                f.write(print_data(l)+'\n')

    except KeyboardInterrupt:
        print("Program stopped by user")

    f.close()

main();
