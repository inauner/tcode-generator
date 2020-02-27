'''
Proof of Concept code - needs a bit of work to be functional
You must enable Stereo Mix input device in windows recording devices.  https://www.howtogeek.com/howto/39532/how-to-enable-stereo-mix-in-windows-7-to-record-audio/
This program will take the first "stereo mix" input device found. Run list_devices() if you want to enumerate them all and manually enter the device number.
'''
import pyaudio # skip the yak shave and grab the pre-compiled windows binary here: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio or pip install pipwin ; pipwin install pyaudio
import serial  # pip install pyserial
import audioop
import sys
import math
import random
import statistics as stats

def list_devices():
    # List all audio input devices, only needed if auto detect doesn't work
    p = pyaudio.PyAudio()
    i = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
                print(str(i)+'. '+dev['name'])
        i += 1

def randomTcode():
        #vertical stroke distance, full tcode stroke is 0-99
        vertDist = random.randint(0,50)
        #time the vertical stroke takes to reach its destination
        vertDur = random.randint(100,900)
        #horizontal stroke distance, full tcode stroke is 0-99
        horDist = random.randint(0,99)
        #time the horizontal stroke takes to reach its destination
        horDur = random.randint(100,900)
        #make sure vertical stroke distance is at least 25 between commands
        return(vertDist,vertDur,horDist,horDur)

def audioTcode():
    chunk    = 100 # need to go fast to catch highs and lows
    scale    = 5   # Change if too dim/bright
    exponent = 1   # Change if too little/too much difference between loud and quiet sounds
    p = pyaudio.PyAudio()
    i = 0
    j = []
    k = 0
    dur=0
    maxV=0
    medV=0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            if 'Stereo Mix' in dev['name']:
                device = i
                break
        i += 1
    
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = dev['maxInputChannels'],
                    rate = 44100,
                    input = True,
                    frames_per_buffer = chunk,
                    input_device_index = device)
    
    print("Starting, use Ctrl+C to stop")
    try:
        last_vertDist = 0
        ser = serial.Serial('COM4',115200,timeout=1,parity=serial.PARITY_EVEN,rtscts=1)
        while True:
            data  = stream.read(chunk)
            rms   = audioop.rms(data, 2)
            # print(rms)
            level = int((min(rms / (2.0 ** 16) * scale, 1.0)**exponent)*255) #some fancy math *shrug*
            if level>99:
                level = 99
            if k == 500:
                i = b'L099I100&L199I100\n' 
                print(i)
                ser.write(i)
            if k <= 1000:
                j.append(level)
            else:
                maxV = 99-max(j)
                medV = 99-int(stats.median(j))
                dur = 100
                print(99-maxV,medV,99-min(j)) #cv determines duration
                k = 0
                j = []
                vertDist = 99-maxV #random.randint(0,50)
                vertDur = dur #random.randint(100,900)
                horDist = 99-maxV #random.randint(0,99)
                horDur = dur #random.randint(100,900)
                # while abs(vertDist-last_vertDist)<25:
                    # vertDist = random.randint(0,50)
                
                i = b'L0%dI%d&L1%dI%d\n' % (vertDist, vertDur, horDist, horDur)
                print(i)
                ser.write(i)
                last_vertDist = vertDist
            k += 1
            #time.sleep(dur/1000)

    except KeyboardInterrupt:
        pass
    finally:
        print("\nStopping")
        stream.close()
        p.terminate()
        ser.close()

if __name__ == '__main__':
    # list_devices()
    audioTcode()
	
	
	
	
	

