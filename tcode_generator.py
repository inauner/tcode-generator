import serial #pip install pySerial
import time
import random
import sys
    
#arduino COM port
COM = 'COM4'
#stroke range. must be between 1 and 9999, but there's a float bug with values under 1000
min_range=1000
max_range=9999
#time between strokes. must be greater than or equal to 0
min_time=400
max_time=1100
    
    
def OSR2():
    #no need to change below variables. used for position state
    last_vertDist=0
    last_grindDist=500
    with serial.Serial(COM,115200,timeout=1,parity=serial.PARITY_EVEN,rtscts=1) as ser:
        while True:
            try:
                vertDist = float(random.randint(min_range,max_range))/10000 #need to make it a float for min. vert stroke distance
                vertDur = random.randint(min_time,max_time) #length of time in ms for a stroke to complete
                grindDur = random.randint(min_time,max_time)
                while grindDur > vertDur:
                    grindDur = random.randint(min_time,max_time)
                #make sure vertical stroke distance is at least x distance between commands
                while abs(vertDist-last_vertDist)<.4:
                    # print(vertDist,last_vertDist)
                    vertDist = float(random.randint(min_range,max_range))/10000
                vertDist = vertDist * 10000
                #randomize a grinding motion
                ranRotate = random.randint(1,2)
                if ranRotate == 1:
                    #make sure grind stroke alternates above / below .5 
                    if last_grindDist >=500:
                        grindDist = random.randint(0,2000)
                    else: 
                        grindDist = random.randint(800,9999)
                    last_grindDist = grindDist
                    i = b'L0%dI%d&R1%dI%d\n' % (vertDist, vertDur, grindDist, grindDur)
                else:
                    i = b'L0%dI%d&R1500I%d\n' % (vertDist, vertDur, vertDur)
                print(i)
                ser.write(i)
                #wait for motion to finish before sending next command
                delay = float(vertDur)/1000
                last_vertDist = float(vertDist)/10000
                time.sleep(delay)
            #send back to default position on exit
            except KeyboardInterrupt:
                i = b'L05R15\n'
                ser.write(i)  
                sys.exit(0)


if __name__ == '__main__':
    OSR2()


