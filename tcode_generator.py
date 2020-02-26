import serial #pip install pySerial
import time
import random
import sys
import platform


#arduino COM port
COM = 'COM4'

# A function that tries to list serial ports on most common platforms
def list_serial_ports():
    system_name = platform.system()
    if system_name == "Windows":
        # Scan for available ports.
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append(i)
                s.close()
            except serial.SerialException:
                pass
        return available
    elif system_name == "Darwin":
        # Mac
        return glob.glob('/dev/tty*') + glob.glob('/dev/cu*')
    else:
        # Assume Linux or something else
        return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*')
        

def OSRneutral():
    with serial.Serial(COM,115200,timeout=1,parity=serial.PARITY_EVEN,rtscts=1) as ser:
        i = b'L05R15\n'
        ser.write(i)

def OSRgrind():
    # with serial.Serial(COM,115200,timeout=1,parity=serial.PARITY_EVEN,rtscts=1) as ser:
    for n in range(5):
        i = b'R1999I500\n'
        time.sleep(.5)
        ser.write(i)
        i = b'R1000I500\n'
        time.sleep(.5)
        ser.write(i)
        return(i)

def OSR2():
    min_range=100
    max_range=699
    min_time=400
    max_time=1100
    last_vertDist=0
    last_grindDist=500
    with serial.Serial(COM,115200,timeout=1,parity=serial.PARITY_EVEN,rtscts=1) as ser:
        while True:
            vertDist = float(random.randint(min_range,max_range))/1000 #need to make it a float for min. vert stroke distance
            vertDur = random.randint(min_time,max_time) #length of time in ms for a stroke to complete
            grindDur = random.randint(1,999)
            #make sure vertical stroke distance is at least 250 between commands
            
            while abs(vertDist-last_vertDist)<.4:
                vertDist = float(random.randint(min_range,max_range))/1000
                # print(vertDist,last_vertDist,abs(vertDist-last_vertDist))
                
            vertDist = vertDist * 1000
            #randomize a grinding motion
            ranRotate = random.randint(1,10)
            if ranRotate == 1:
                #make sure grind stroke alternates above / below .5 
                if last_grindDist >=500:
                    grindDist = random.randint(1,200)
                else: 
                    grindDist = random.randint(800,999)
                last_grindDist = grindDist
                i = b'L0%dI%dR1%dI%d\n' % (vertDist, vertDur, grindDist, grindDur)
            else:
                i = b'L0%dI%d\n' % (vertDist, vertDur)
            print(i)
            ser.write(i)
            #wait for motion to finish before sending next command
            delay = float(vertDur)/1000
            last_vertDist = float(vertDist)/1000

            time.sleep(delay)
            




if __name__ == '__main__':
    if len(sys.argv)>1:
        if sys.argv[1] == str(2):
            OSR2()
        elif sys.argv[1] == str(3):
            OSR3()
        elif sys.argv[1] == str('grind'):
            OSRgrind()
        elif sys.argv[1] == str(0):
            OSRneutral()
        else:
            OSR = input("2 for OSR2, 3 for OSR3")
            if OSR == 3:
                OSR3()
            else:
                OSR2()
    else:
        OSR = input("2 for OSR2, 3 for OSR3")
        if OSR == 3:
            OSR3()
        else:
            OSR2()



'''
NOTES
L0999I300&R1500I300
SLOW: I9000, S0
FAST: I0, S9000
'''