import sys
sys.path.append("..")
import QuickMarch as qm 
import os

#Create Band    
Size = [8,4]
Band = qm.BandCls(Size,Angle = 90)

#----------Commands-------------------
Time = qm.QuickMarch(Band,0,2)
Time = qm.Bend(Band,Time,90)
Time = qm.Bend(Band,Time,-90,SameStart = True)
Time = qm.QuickMarch(Band,Time,100)

#----------Plot----------------------
bpm = 120
dt = 0.2
steps = 250
folder = 'Out/'

qm.makeOutput(Band,folder,steps,dt)
framerate = 1.0 / (60.0 / bpm * dt)
command = 'ffmpeg -r  ' + str(framerate) + ' -f image2 -i ' + folder + '%d.png -vcodec libx264rgb -preset slow -qp 0 ' + folder + 'output.mkv'
os.system(command)
