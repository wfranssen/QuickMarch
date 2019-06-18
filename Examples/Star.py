import sys
import os
import math
sys.path.append("..")
import QuickMarch as qm 

#This example shows how to make your own commands using the base commands
#in the library. As we require unique commands for every column in this case, 
#we cannot make this with the higher level commands.

def Star(Band,Time,MarchTime):
    AngleList = [-90,-35,35,90] #List of angles to bend when making the star
    BackAngleList = [-180,-180,180,180] #List of angles for the return

    Radius = 0.2 * Band.Sep[1] #Return bend should be small, 0.2 times the column sep in this case

    for Player in Band.BandList:
        BendTime = (Radius * math.pi) / Player.Stride
        Column = Player.Column
        Angle = AngleList[Column]
        BackAngle = BackAngleList[Column]
        if Player.Row > 0: #Let rows behind the first move straight to the start of the star
            qm.QuickMarchBase(Player,Time,Player.Row * Band.Sep[0] / Player.Stride)
        
        #Turn1 (radius very small, but must be non-zero)
        tmpTime = qm.BendBase(Player,1e-6,Time,Angle,TotalBeats = 0)

        #Straight1
        tmpTime = qm.QuickMarchBase(Player,tmpTime,MarchTime)

        #Bend
        tmpTime = qm.BendBase(Player,0.2 * Band.Sep[1],tmpTime,BackAngle,TotalBeats = BendTime)

        #Straight2
        tmpTime = qm.QuickMarchBase(Player,tmpTime,MarchTime)

        #Turn2 (radius very small, but must be non-zero)
        tmpTime = qm.BendBase(Player,1e-6,tmpTime,-Angle,TotalBeats = 0)
    return tmpTime


#----------Create Band---------------
Size = [8,4]
Band = qm.BandCls(Size,Angle = 90)

#----------Commands------------------
Time = qm.QuickMarch(Band,0,2)
Time = Star(Band,Time,16)
Time = qm.QuickMarch(Band,Time,100)

#----------Plot----------------------
bpm = 120
dt = 0.2
steps = 300
folder = 'Out/'

qm.makeOutput(Band,folder,steps,dt)

#--------Make movie------------------
framerate = 1.0 / (60.0 / bpm * dt)
command = 'ffmpeg -r  ' + str(framerate) + ' -f image2 -i ' + folder + '%d.png -vcodec libx264rgb -preset slow -qp 0 ' + folder + 'output.mkv'
os.system(command)
