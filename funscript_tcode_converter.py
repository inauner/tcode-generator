import json
import sys
import os

def convert(input,output):
    data = json.load(open(input, 'r'))
    actions = (data)['actions']
    f = open(output,'w')
    last_at=0

    for action in actions:
        pos = float(action['pos'])/100
        if pos == 1.0:
            pos = 0.999
        pos = pos * 1000
        at = action['at']
        i = "L0%dI%d" %(pos,at-last_at)
        f.write(i+'\n')
        last_at = at
        
    
if __name__ == '__main__':
    if len(sys.argv)==3:
        convert(sys.argv[1],sys.argv[2])
    elif len(sys.argv)==2:
        output = os.path.splitext(sys.argv[1])[0]+".tcode"
        convert(sys.argv[1],output)
    else: 
        print("drag funscript onto this script")
        
