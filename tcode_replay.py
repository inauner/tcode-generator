import serial #pip install pySerial
import re
import time
import sys

COM="COM4"

def tcode_replay(filename):
    with serial.Serial(COM,115200,timeout=1,parity=serial.PARITY_EVEN,rtscts=1) as ser:
        f = open(filename,"r")
        
        for line in f.readlines():
            line = line.rstrip()
            tuples = re.findall(r'([Ii])(\d+)', line)
            findmax = []
            for tuple in tuples:
                findmax.append(int(tuple[1]))
            interval = max(findmax)
            line = line + "\n"
            line = line.encode()
            print(line)
            ser.write(line)
            time.sleep(float(interval)/1000)
        
        
if __name__ == '__main__':
    if len(sys.argv)>1:
        tcode_replay(sys.argv[1])
    else: 
        print("specify file in same dir as arg")