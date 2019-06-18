import matplotlib.pyplot as plt
import os
import math

# Copyright 2019 Wouter Franssen

# This file is part of QuickMarch.
#
# QuickMarch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# QuickMarch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with QuickMarch. If not, see <http://www.gnu.org/licenses/>.

def sind(angle):
    """
    Returns the sine of the value that is supplied in degrees
    """
    return math.sin(angle/180 * math.pi)
    
def cosd(angle):
    """
    Returns the cosine of the value that is supplied in degrees
    """
    return math.cos(angle/180 * math.pi) 

def rotMatrix(angle):
    """
    Returns a 2x2 rotation matrix for the supplied "angle"
    """
    return [[cosd(angle),-sind(angle)],[sind(angle),cosd(angle)]]

def dot(a,b):
    """
    Performs a dot product between a 2x2 matrix and a length 2 vector
    a: list of lists (2x2)
    b: list (length 2)
    """
    elem1 = a[0][0] * b[0] + a[0][1] * b[1]
    elem2 = a[1][0] * b[0] + a[1][1] * b[1]
    return [elem1, elem2]

def vecSum(a,b):
    """
    Sums two length two vectors (i.e. lists)
    """
    return [a[0] + b[0], a[1] + b[1]]

 
class PlayerCls:
    """
    The player class. This holds the row and column position of a player, 
    as well as the step size (i.e. stride). Additional input is the start position
    ([x,y]) and start angle.
    """
    def __init__(self,startPos,startAngle, Stride, Row, Column):
        self.Pos = startPos
        self.Distance = 0
        self.Angle = startAngle
        self.Stride = Stride
        self.Row = Row
        self.Column = Column
        self.Path = [[None,None,0,self.Pos,self.Angle]]
        self.CumDist = [0] #The cumulative distance (i.e. the distance at the end of each path)
        self.Commands = [] #Holds the commands. Each command is a list with [time, stridelength]
        #Symbol definition in polar coordinates [r,angle]
        self.Symbol = [[0, 0], [0.3, 135], [0.4, 0], [0.3,-135]]
        self.Colour = 'b' #Symbol colour

class BandCls:
    def __init__(self,Size,Sep = [1.6,1.6],Stride = 0.8,Pos = [0,0],Angle = 0):
        """
        Band class object. Holds all the individual players, as well as the current
        time.

        Inputs:
        Size: size of the band, in [Rows,Colums]
        Sep (optional = [1.6,1.6]): distance between rows and columns [Row,Column]
        Stride (optional = 0.8): stride length
        Pos (optional [0,0]): start position of row 1, centre position [x,y]
        Angle (optional = 0): start angle of all players


        Routines:
        advanceTime: Advance the time of the band, calculating all new positions
        and angles of all players.

        Plot: Makes a plot of the band, and saves to a file.
        """
        self.Rows = Size[0]
        self.Columns = Size[1]
        self.BandList = []
        self.Sep = Sep 
        self.Pos = Pos
        self.Angle = Angle
        self.Time = 0 #Time in beats since start
        self.LastCTime = 0 #Time of last command/path definition
        
        for Row in range(self.Rows):
            for Column in range(self.Columns):
                Cpos = (Column + 1 - (self.Columns + 1) / 2) * self.Sep[1]
                Rpos =  Row * self.Sep[0]
                x = sind(Angle) * Cpos - cosd(Angle) * Rpos
                y = - cosd(Angle) * Cpos - sind(Angle) * Rpos
                self.BandList.append(PlayerCls([x,y],self.Angle,Stride,Row,Column))
                
    def advanceTime(self,Beats):
        """
        Advance the time of the band. This updates all player positions and orientations

        Input:
        Beats: the number of beats that the time should be advanced
        """

        OldTime = self.Time
        NewTime = OldTime + Beats
        for Player in self.BandList:
            Dist = Player.Distance
            CurrentTime = self.Time

            ActiveCommands = [x[0] for x in Player.Commands if x[0] >= OldTime]
            CommandsIndex = [x for x in range(len(Player.Commands)) if Player.Commands[x][0]  >= OldTime]
                    
            while CurrentTime < NewTime: #Continue increasing dist until final time is reached
                if len(ActiveCommands) > 0 and NewTime >= ActiveCommands[0]:
                    Dist += (ActiveCommands[0] - CurrentTime ) * Player.Stride
                    Player.Stride = Player.Commands[CommandsIndex[0]][1]
                    CurrentTime += ActiveCommands[0] - CurrentTime
                    ActiveCommands.pop(0) #Remove used command
                    CommandsIndex.pop(0) #Remove used command
                else:
                    Dist += (NewTime - CurrentTime) * Player.Stride
                    CurrentTime = NewTime
            
            #Calc the new position
            ActivePaths = [a for a in Player.CumDist if a > Dist]
            if len(ActivePaths) > 0: #Stop if there is no path at this distance
                Path = ActivePaths[0]
                Index = Player.CumDist.index(Path)

                EffDist = Dist
                if Index > 0: #Get start offset of current path
                    EffDist -= Player.CumDist[Index - 1]
                Player.Pos = Player.Path[Index][0](EffDist)
                Player.Angle = Player.Path[Index][1](EffDist)
                Player.Distance = Dist
            
        self.Time = NewTime #Update the time to the new value
        
    def plot(self,Path,Fig = None,ax = None, limits = [[-20,20],[-60,65]], dpi = 150):
        """
        Make a plot of the current band

        Inputs: 
        Path: string, with output location path including file extension (i.e. .png)
        Fig (optional): figure handle
        ax (optional): axis handle
        limits (optional): plot limits as list of lists: [[xmin, xmax],[ymin, ymax]]
        dpi (optional = 150): resolution of output picture
        """
        if Fig == None:
            Fig = plt.figure()
            ax = Fig.add_subplot(111)
        else:
            ax.clear()
        for Player in self.BandList:
                #Rotate and translate symbol
                tmpSymbol = list(Player.Symbol)
                for pos, elem in enumerate(tmpSymbol):
                   r = elem[0]
                   shapeAngle = elem[1]
                   tmpSymbol[pos] = [r * cosd(Player.Angle + shapeAngle) + Player.Pos[0], r * sind(Player.Angle + shapeAngle) + Player.Pos[1]]
                Fig.gca().add_patch(plt.Polygon(tmpSymbol,Player.Colour))
        ax.axis('equal')
        ax.axis('off')
        ax.set_xlim(limits[0])
        ax.set_ylim(limits[1])
        Fig.canvas.draw()
        Fig.savefig(Path,dpi=dpi)
        return Fig, ax

def makeOutput(Band,Folder,Steps,dt,PlotLimits = [[-20,20],[-60,65]], dpi = 150):
    """
    Generate images of all required frames of the band animation

    Input:
    Band: BandCls object
    Folder: output folder, will be cleared/created if required
    Steps: number of animation frames
    dt: time in beats between each frame
    """
    if int(Steps) < 1:
        raise ValueError('"Steps" should be more than 0')

    if not os.path.exists(Folder):
        os.mkdir(Folder)

    #Clear folder
    filelist = [ f for f in os.listdir(Folder)]
    for f in filelist:
        os.remove(os.path.join(Folder, f))

    Fig,ax = Band.plot(Folder + '1.png', limits = PlotLimits, dpi=dpi)
    for step in range(int(Steps) - 1):
        Band.advanceTime(dt)
        Band.plot(Folder + str(step + 2) + '.png', Fig, ax, limits = PlotLimits, dpi=dpi)
    plt.close()


def CornerPosFunction(StartPos,StartAngle,Radius,Angle):
    """
    Position function for a corner. Returns a lambda function in which a distance
    from the start of the path can be supplied. It returns the position [x,y] of the player.

    Inputs:
    StartPos: [x,y] (start position of the player before the path)
    StartAngle: float (start angle of the player before the path)
    Radius: Radius of the corner that is to be made
    Angle: Angle of the corner that is to be made. Positive values are corners to the right.
    """
    start = [StartPos[0],StartPos[1]]
    sign = math.copysign(1,Angle)
    totdist = math.fabs(2*math.pi*Radius/360*Angle)

    return lambda Dist: vecSum(start, dot(rotMatrix(StartAngle) , [Radius * sind(sign*Angle*Dist/totdist), Radius * (sign*cosd(Angle*Dist/totdist) - sign)]))
    
def CornerAngleFunction(StartAngle,Radius,Angle):
    """
    Angle function for a corner. Returns a lambda function in which a distance
    from the start of the path can be supplied. It returns the angle of the player.

    Inputs:
    StartAngle: float (start angle of the player before the path)
    Radius: Radius of the corner that is to be made
    Angle: Angle of the corner that is to be made. Positive values are corners to the right.
    """
    sign = -math.copysign(1,Angle)
    totdist = math.fabs(2*math.pi*Radius/360*Angle)
    return lambda Dist: StartAngle - Angle * Dist / totdist

def StraightPosFunction(StartPos,StartAngle):
    """
    Position function for a straight path. Returns a lambda function in which a distance
    from the start of the path can be supplied. It returns the position [x,y] of the player.

    Inputs:
    StartPos: [x,y] (start position of the player before the path)
    StartAngle: float (start angle of the player before the path)
    """
    return lambda Dist: [StartPos[0] + cosd(StartAngle) * Dist, StartPos[1] + sind(StartAngle) * Dist]


def StraightAngleFunction(StartAngle):
    """
    Angle function for a straight path. Returns a lambda function in which a distance
    from the start of the path can be supplied. It returns the angle of the player.

    Inputs:
    StartAngle: float (start angle of the player before the path)
    """
    return lambda Dist: StartAngle


def QuickMarchBase(Player,Time,TotalBeats):
    """
    Base function for a straight path. It adds all required path and commands
    to the "Player" for a path of duration "TotalBeats". Stride length is not changed.
    """
    pathdist = TotalBeats * Player.Stride

    startpos = Player.Path[-1][3] #start pos of previous path
    startangle = Player.Path[-1][4] #start angle of previous path
    maxdistance = pathdist + Player.CumDist[-1]
            
    posdef =  StraightPosFunction(startpos,startangle) 
    angledef =  StraightAngleFunction(startangle)
    endpos = posdef(pathdist)
    endangle = angledef(pathdist)
    Player.Path.append([posdef,angledef,pathdist,endpos,endangle]) 
    Player.CumDist.append(maxdistance)
    return Time + TotalBeats
               
    
def BendBase(Player,Radius,Time,Angle,TotalBeats = 2):
    """
    Base function for a bend. It adds all required path and commands
    to the "Player" for a path of duration "TotalBeats". 
    Other input is:
    Radius: the radius of the bend that the player must make
    Time: the time the change in speed should start
    Angle: the angle of the bend (positive angles are bends to the right)
    """
    PathDist = math.fabs(Angle) / 180 * math.pi * Radius

    StartPos = Player.Path[-1][3] #Start Pos of previous path
    StartAngle = Player.Path[-1][4] #Start Angle of previous path
    MaxDistance = PathDist + Player.CumDist[-1]
        
    PosDef =  CornerPosFunction(StartPos,StartAngle,Radius,Angle) 
    AngleDef =  CornerAngleFunction(StartAngle,Radius,Angle)
    EndPos = PosDef(PathDist)
    EndAngle = AngleDef(PathDist)
    Player.Path.append([PosDef,AngleDef,PathDist,EndPos,EndAngle]) 
    Player.CumDist.append(MaxDistance)
   
    endTime = Time + TotalBeats
    if TotalBeats > 0: #If no time, no speed changes are needed
        Player.Commands.append([Time ,PathDist / TotalBeats])
        Player.Commands.append([endTime, Player.Stride]) #Reset stride
    return endTime


def QuickMarch(Band,TotalBeats):
    """
    Walk in a straight line for "TotalBeats" time.

    Input:
    Band: the BandCls object
    TotalBeats: float of the total number of beats the walk should last
    """
    for Player in Band.BandList:
        QuickMarchBase(Player,Band.LastCTime,TotalBeats)
    Band.LastCTime += TotalBeats

def Bend(Band,Angle,TotalBeats=16, SameStart = False):
    """
    Make a bend. Radii are based on the columns of the players. The
    innermost column has radius of 0, while the other columns remain
    their regular separation apart.

    Input:
    Band: the BandCls object
    Angle: the angle of the bend (positive for right, negative for left)
    TotalBeats (optional = 16): float of the total number of beats the walk should last
    SameStart (optional = False): bool, specifies if the path before this bend end
    at the same place or not.
    """
    for Player in Band.BandList:
        if Player.Row > 0 and not SameStart:
            QuickMarchBase(Player,Band.LastCTime,Player.Row * Band.Sep[0] / Player.Stride)
        if Angle < 0:
            Radius = Player.Column * Band.Sep[1] 
        else:
            Radius = (Band.Columns - Player.Column - 1) * Band.Sep[1]
        if Radius == 0.0:
            Radius = 1e-6
        BendBase(Player,Radius,Band.LastCTime,Angle,TotalBeats)
    Band.LastCTime += TotalBeats


def Turn(Band,Angle,TotalBeats = 2):
    """
    Turn Band in place

    Input:
    Band: BandCls object
    Time: time of the start of the turn
    Angle: rotation angle (positive for right, negative for left)
    TotalBeats (optional = 2): number of beats of the movement
    """
    for Player in Band.BandList:
        BendBase(Player,1e-6,Band.LastCTime,Angle,TotalBeats)
    Band.LastCTime += TotalBeats

def EnglishCounter(Band,SameStart = False):
    """
    Perform an english counter

    Input:
    Band: BandCls object
    Time: start time of the english counter
    SameStart (optional = False): bool, specifies if the path before this bend end
    at the same place or not.
    """
    Radius = 0.25 * Band.Sep[1]
    for Player in Band.BandList:
        BendTime = (Radius * math.pi) / Player.Stride
        if Player.Row > 0 and not SameStart:
            QuickMarchBase(Player, Band.LastCTime, Player.Row * Band.Sep[0] / Player.Stride)
        BendBase(Player,Radius, Band.LastCTime,180,BendTime)
        #Switch left-right
        Player.Column = Band.Columns - Player.Column - 1
    Band.LastCTime += BendTime


def AmericanCounter(Band, TotalBeats=16, SameStart = False):
    """
    Perform an american counter

    Input:
    Band: BandCls object
    Time: start time of the counter
    TotalBeats (optional = 16): number of beats of the movement
    SameStart (optional = False): bool, specifies if the path before this bend end
    at the same place or not.
    """
    Centre = math.ceil(Band.Columns/2) - 1
    for Player in Band.BandList:
        if Player.Row > 0 and not SameStart:
            QuickMarchBase(Player, Band.LastCTime, Player.Row * Band.Sep[0] / Player.Stride)
        Column = Player.Column
        if Column <= Centre:
            Angle = 180
            Radius = abs(Column - Centre) * 2 + 0.5
        else:
            Angle = -180
            Radius = abs(Column - Centre) * 2 - 0.5
        Radius *= Band.Sep[1] / 2

        BendBase(Player,Radius,Band.LastCTime,Angle,TotalBeats)
    Band.LastCTime += TotalBeats

