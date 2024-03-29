import sys
import os
import math
sys.path.append("..")
import QuickMarch as qm 

#This example shows how to make your own commands using the base commands
#in the library. As we require unique commands for every column in this case, 
#we cannot make this with the higher level commands.

def Star(Band,MarchTime):
    """
    Defines a star like move. Only defined for a 4 column band (this could be generalized).

    Input:
    MarchTime: time that should be moved in a straight line after the split
    """
    AngleList = [-90,-35,35,90] #List of angles to bend when making the star
    BackAngleList = [-180,-180,180,180] #List of angles for the return

    Radius = 0.2 * Band.Sep[1] #Return bend should be small, 0.2 times the column sep in this case

    for Player in Band.BandList:
        BendTime = (Radius * math.pi) / Player.Stride
        Column = Player.Column
        Angle = AngleList[Column]
        BackAngle = BackAngleList[Column]
        if Player.Row > 0 and not Band.StartEqual: #Let rows behind the first move straight to the start of the star
            qm.QuickMarchBase(Player,Band.LastCTime,Player.Row * Band.Sep[0] / Player.Stride)
        
        #Turn1 (radius very small, but must be non-zero)
        tmpTime = qm.BendBase(Player,1e-6,Band.LastCTime,Angle,TotalBeats = 0)
        #Straight1
        tmpTime = qm.QuickMarchBase(Player,tmpTime,MarchTime)
        #Bend
        tmpTime = qm.BendBase(Player,0.2 * Band.Sep[1],tmpTime,BackAngle,TotalBeats = BendTime)
        #Straight2
        tmpTime = qm.QuickMarchBase(Player,tmpTime,MarchTime)
        #Turn2 (radius very small, but must be non-zero)
        tmpTime = qm.BendBase(Player,1e-6,tmpTime,-Angle,TotalBeats = 0)
    Band.StartEqual = True #All players have now been defined up to the same position
    Band.LastCTime = tmpTime #Set the time of the last position of the band


#----------Create Band---------------
Size = [8,4]
Band = qm.BandCls(Size,Angle = 90)

#----------Commands------------------
qm.QuickMarch(Band,2)
Star(Band,16)
qm.QuickMarch(Band,100)

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
