import math
import LatLon

def Sprial_Waypoint_Generator_xy(home , DistanceBetweenTurn, NumPoints):
    a = DistanceBetweenTurn / math.pi
    #r = a * theta									# formula of  spiral
    points = []
    for i in range(0, NumPoints):
        theta = i * (2 * math.pi / NumPoints)
        r = a * theta
        point = home.offset(math.degrees(theta), r/1000)
        #x = r * math.cos(theta)						# polar to xy
        #y = r * math.sin(theta)						# polar to xy
        points.append(point)
    return points

def Delm_to_latlon(delx,dely,clat,clon):
    latx,lonx,num,zone = utm.from_latlon(clat, clon)
    latx = latx+delx
    lonx = lonx+dely
    flat,flon = utm.to_latlon(latx,lonx,num,zone)
    return [flat,flon]
    

if __name__ == "__main__":
    home = LatLon.LatLon(LatLon.Latitude(32.2362917), LatLon.Longitude(-110.9501144))
    points = Sprial_Waypoint_Generator_xy(home,50,100)
    
    mission = open('out.txt', 'w')
    mission.write("QGC WPL 110\n0\t1\t0\t0\t0\t0\t0\t0\t0\t0\t0\t1\n")
    for i, point in enumerate(points):
        mission.write(str(i+1)+"1\t0\t3\t16\t0.000000\t0.000000\t0.000000\t0.000000\t")
        mission.write(str(point.to_string("%D")[0])+"\t"+str(point.to_string("%D")[1]))
        mission.write("\t100.000000\t1\n")
        print point.to_string("%D")
        #print math.degrees(latlon[0]),math.degrees(latlon[1])