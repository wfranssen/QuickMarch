import sys
sys.path.append("..")
import QuickMarch as qm 
import os

#Create Band    
Size = [8,5]
Band = qm.BandCls(Size,Angle = 90)

#----------Commands-------------------
qm.QuickMarch(Band,16)
qm.EnglishCounter(Band)
qm.QuickMarch(Band,16)
qm.Bend(Band,90,SameStart = True)
qm.QuickMarch(Band,16)
qm.AmericanCounter(Band,SameStart = True)
qm.QuickMarch(Band,100)
#----------Plot----------------------
bpm = 120
dt = 0.2
steps = 500
folder = 'Out/'

qm.makeOutput(Band,folder,steps,dt)

#--------Make movie------------------
framerate = 1.0 / (60.0 / bpm * dt)
command = 'ffmpeg -r  ' + str(framerate) + ' -f image2 -i ' + folder + '%d.png -vcodec libx264rgb -preset slow -qp 0 ' + folder + 'output.mkv'
os.system(command)
