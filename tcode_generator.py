import serial #pip install pySerial
import time
import random
import sys

#arduino COM port
COM = 'COM4'

def OSR2():
    last_vertDist=1
    last_grindDist=500
    with serial.Serial(COM,115200,timeout=1,parity=serial.PARITY_EVEN,rtscts=1) as ser:
        while True:
            vertDist = random.randint(100,999)/1000 #need to make it a float for min. vert stroke distance
            vertDur = random.randint(400,1200) #length of time in ms for a stroke to complete
            grindDur = random.randint(1,999)
            #make sure vertical stroke distance is at least 250 between commands
            while abs(vertDist-last_vertDist/1000)<.7:
                vertDist = random.randint(100,999)/1000
            vertDist = vertDist * 1000
            #randomize a grinding motion
            ranRotate = random.randint(3,3)
            if ranRotate == 1:
                i = b'L0%dI%d&R1%dI%d\n' % (vertDist, vertDur, grindDist, grindDur)
            elif ranRotate == 2:
                #make sure grind stroke alternates above / below .5 
                if last_grindDist >=500:
                    grindDist = random.randint(1,400)
                else: 
                    grindDist = random.randint(600,999)
                last_grindDist = grindDist
                i = b'R1%dI%d\n' % (grindDist, grindDur)
            else:
                i = b'L0%dI%d\n' % (vertDist, vertDur)
            print(i)
            ser.write(i)
            #wait for motion to finish before sending next command
            delay = vertDur/1000
            last_vertDist = vertDist

            time.sleep(delay)
            
def OSR0():
    with serial.Serial(COM,115200,timeout=1,parity=serial.PARITY_EVEN,rtscts=1) as ser:
        while True:
            i = b'L0999I3000\n'
            time.sleep(3)
            ser.write(i)
            i = b'L0000I3000\n'
            time.sleep(3)
            ser.write(i)
            print(i)

if __name__ == '__main__':
    if len(sys.argv)>1:
        if sys.argv[1] == str(2):
            OSR2()
        elif sys.argv[1] == str(3):
            OSR3()
        elif sys.argv[1] == str(0):
            OSR0()
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