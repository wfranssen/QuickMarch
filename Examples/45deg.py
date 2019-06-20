import sys
sys.path.append("..")
import QuickMarch as qm 

#Example to show a relatively easy redefinition of a turn function.
#We turn the odd and even rows by a different angle, march forward,
#rotate the full band 180 degrees, move forward again, and undo the
#odd/even rotation.

import os
def TurnOddEven(Band, Angles, TotalBeats = 2):
    """
    Turn Band in place, with angle depending on the row odd/even

    Input:
    Band: BandCls object
    Angle: [odd, even] angles
    TotalBeats (optional = 2): number of beats of the movement
    """
    for Player in Band.BandList:
        if Player.Row%2 == 0: #if even row
            Angle = Angles[0]
        else:
            Angle= Angles[1]
        qm.BendBase(Player,1e-6,Band.LastCTime,Angle,TotalBeats)
    Band.LastCTime += TotalBeats

#Create Band    
Size = [8,5]
Band = qm.BandCls(Size,Angle = 90)

#----------Commands-------------------
qm.QuickMarch(Band,4)
TurnOddEven(Band, [45, -45])
qm.QuickMarch(Band,10)
qm.Turn(Band,180)
qm.QuickMarch(Band,10)
TurnOddEven(Band, [135,-135])
qm.QuickMarch(Band,100)

#----------Plot----------------------
bpm = 120
dt = 0.2
steps = 170
folder = 'Out/'

qm.makeOutput(Band,folder,steps,dt)

#--------Make movie------------------
framerate = 1.0 / (60.0 / bpm * dt)
command = 'ffmpeg -r  ' + str(framerate) + ' -f image2 -i ' + folder + '%d.png -vcodec libx264rgb -preset slow -qp 0 ' + folder + 'output.mkv'
os.system(command)
