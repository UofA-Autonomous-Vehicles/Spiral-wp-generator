import math
import LatLon

def Sprial_Waypoint_Generator_xy(home , DistanceBetweenTurn, NumPoints, radius):
    a = (DistanceBetweenTurn/2) / math.pi
    NumTurns = math.degrees(radius/a)/360
    degPerPoint = (NumTurns*360)/NumPoints
    points = []
    tail = []
    close = False
    #write spiral
    for i in range(0, NumPoints):
        theta = i * degPerPoint
        r = a * math.radians(theta)
        point = home.offset(theta, r/1000.0)
        points.append(point)
    #write finishing loop until dist is less than spiral dist to closeist point
    i = NumPoints
    r = a*math.radians(i * degPerPoint)
    while (close is False):
        if ((i-NumPoints)*degPerPoint)>360:
            close = True
        i += 1
        tail.append(home.offset((i * degPerPoint),(r/1000)))
        #devide by 3000 in order to get within one third the sepration distance
        if tail[-1].distance(points[-int(round(180/degPerPoint))]) <= (DistanceBetweenTurn/3000.):
            close = True
    return points+tail
    
class MP_file_write(object):
    def __init__(self,filename='out.txt'):
        self.outfile = open(filename, 'w')
        #write version string
        self.outfile.write("QGC WPL 110\n")
        self.index = 0
        
    #Feild names from http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format
    def WriteLine(self,
    CURRENT_WP = 0,
    COORD_FRAME = 3, #Cord info from http://planner.ardupilot.com/wiki/common-mavlink-mission-command-messages-mav_cmd/#copter-4
    COMMAND = 16,   #Commands 16 = waypoint, 82 = Spline WP, 21 = Land, 22 = Takeoff
    PARAM1=0,#                Delay          Delay           N/A        
    PARAM2=0,#                N/A            N/A             N/A        
    PARAM3=0,#                N/A            N/A             N/A        
    PARAM4=0,#                N/A            N/A             N/A        
    PARAM5=0,#                Lat            Lat             Lat        
    PARAM6=0,#                Lon            Lon             Lon        
    PARAM7=0,#                Alt (m)        Alt (m)         N/A        Alt(m)
    AUTOCONTINUE=1,#Automatically move to next command?
    ):
        self.index += 1
        INDEX = self.index
        self.outfile.write(str(INDEX)+"\t"+
            str(CURRENT_WP)+"\t"+
            str(COORD_FRAME)+"\t"+
            str(COMMAND)+"\t"+
            str(PARAM1)+"\t"+
            str(PARAM2)+"\t"+
            str(PARAM3)+"\t"+
            str(PARAM4)+"\t"+
            str(PARAM5)+"\t"+
            str(PARAM6)+"\t"+
            str(PARAM7)+"\t"+
            str(AUTOCONTINUE)+"\n")
            
    def addWP(self,lat_lon,alt=10):
        self.WriteLine(PARAM5=(lat_lon.to_string("%D")[0]),PARAM6=(lat_lon.to_string("%D")[1]),PARAM7=alt)
    def addSpline(self,lat_lon,alt=10):
        self.WriteLine(COMMAND=82,PARAM5=(lat_lon.to_string("%D")[0]),PARAM6=(lat_lon.to_string("%D")[1]),PARAM7=alt)
        
    

if __name__ == "__main__":
    home = LatLon.LatLon(LatLon.Latitude(32.2362917), LatLon.Longitude(-110.9501144))
    points = Sprial_Waypoint_Generator_xy(home,25,200,100)
    mp_file = MP_file_write()
    for i, point in enumerate(points):
        mp_file.addSpline(point)
        print i," ",point.to_string("%D")
        #print math.degrees(latlon[0]),math.degrees(latlon[1])