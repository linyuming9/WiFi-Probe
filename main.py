import fileinput

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
    time = data[1][0:7]
    
    rss = get_rss(line)
    mac_source = get_mac_source(line)
    mac_dest = get_mac_destination(line)
    
    return(date + " " + time + "," + mac_source + "," + mac_dest + "," + rss)

def main():
    f = open('/mnt/usb/record','a') #record position

    try:
	pre_record = ""
        while(True):
            for line in fileinput.input():
                l = line.upper()

		record = print_data(l)
		if record[:-2] != pre_cord[:-2] :
			f.write(record+'\n')
		pre_record = record

    except KeyboardInterrupt:
        print("Program stopped by user")

    f.close()

main();
