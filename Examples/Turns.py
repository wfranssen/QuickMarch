import sys
sys.path.append("..")
import QuickMarch as qm 
import os

#This example shows some advanced tweeks that are needed when making use of turns (i.e.
#rotate all players in place).

#Create Band    
Size = [8,5]
Band = qm.BandCls(Size,Angle = 90)

#----------Commands-------------------
qm.QuickMarch(Band,16)
qm.EnglishCounter(Band)
#After the counter, all player path end at the same position: the end of the counter
#If we want to do a turn inplace, we must correct for this
#The "QuickMarchReturn" command issue move forward for all players, which ends at the time
#the last row exited the counter
qm.QuickMarchReturn(Band)
qm.Turn(Band,-90)
qm.QuickMarch(Band,10)
qm.Turn(Band,90)
qm.QuickMarch(Band,4)
qm.Bend(Band,90)
qm.QuickMarch(Band,100)
#----------Plot----------------------
bpm = 120
dt = 0.2
steps = 420
folder = 'Out/'

qm.makeOutput(Band,folder,steps,dt)

#--------Make movie------------------
framerate = 1.0 / (60.0 / bpm * dt)
command = 'ffmpeg -r  ' + str(framerate) + ' -f image2 -i ' + folder + '%d.png -vcodec libx264rgb -preset slow -qp 0 ' + folder + 'output.mkv'
os.system(command)
