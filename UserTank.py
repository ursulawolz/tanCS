from Tank import *

class UserTank:
    '''This class is a wrapper for the purpose of the API. It gives the user access to the Tank class in a controlled manner
    '''


    def __init__(self, tank):
        self.__tank = tank

    def wait(self, time):
    	'''The tank waits, doing nothing, for the specified time, in seconds'''
    	self.__tank.wait(time)

    #MOVEMENT

    def apply_thrusters(self, right = 1, left = 1):
        '''Applies forces to the tank in order to move it.
        @param right, left: Given from -1 to 1'''

        if abs(right) > 1:
            raise ValueError ("Thrusters must be applied with values between -1 and 1.")
        if abs(left) > 1:
            raise ValueError ("Thrusters must be applied with values between -1 and 1")

        self.__tank.applyThrusters(right, left)

    def apply_brakes(self, amt = 1):
        '''Applies braking force to all wheels 
        @param amt: between 0 and 1'''

        if (amt < 0 or amt > 1):
            raise ValueError("Brakes must be applied between 0 and 1")

        self.__tank.applyBrakes(amt)


    def move(self, distance = 20):
        '''Moves the tank the given distance. Forward is positive'''
        self.__tank.move(distance)

    def backward(self, dist = 20):
        '''Moves the specified number of units backward'''
        if dist <=0:
            raise ValueError("Distance must be positive for forward and backward")
        else:
            self.move(-1*distance)
    
    def forward(self, distance = 20):
        '''Moves the specified number of units forward'''
        if (dist <=0):
            raise ValueError("Distance must be positive for forward and backward")
        else:
            self.move(distance)

    #ROTATION

    def rotate(self, angle = 90):
        '''Rotates the tank the specified number of degrees. Counter-clockwise (left) is positive'''
        self.__tank.rotate(angle)


    def turn_to(self, newH = 0):
        '''Turn so that you have the given heading value'''

        self.rotate(newH - self._nodePath.getH())

    def left(self, angle = 90):
        '''Turns the specified number of degrees left'''

        if angle < 0:
            raise ValueError("For left and right, angle must be greater than 0.")

        self.rotate(angle)

    def right(self, angle = 90):
        '''Turns the specified number of degrees right'''
        if angle < 0:
            raise ValueError("For left and right, angle must be greater than 0.")

        self.rotate(-angle)

    def face(self, point = (0,0,0)):
        '''Turn so that you are facing a point. Uses rotate and faceRel
        Assumes absolute coordinate system for the point
        '''
        if type(point) == tuple or type(point) == list:
            point = Point3(point[0], point[1], 0)
        deltaPos = point - self.getPos()
        self.faceRel(deltaPos)

    def face_rel(self, point_rel = (10, 0, 0)):
        '''Turn so that you face a point_rel relative to the tank.
        @param point_rel: Relative x, y and z coordinates as a Point3, tuple, or list
        '''
        if type(pointRel) == tuple or type(pointRel) == list:
            point_rel = Point3(point_rel[0], point_rel[1], 0)
		        
        newH = math.atan2(pointRel[1], pointRel[0]) * 180/math.pi + 90
        self.turnTo(newH)


    #SCANNING

    def distance_scan(self):
    	'''
        This scan projects rays from the objects in the field toward the tank 
        in question. This scan does not perform as well as scan when the 
        objects are bunched together. When small objects are spread out 
        reasonably (more than 5 at a viewing range of 50), this scan performs 
        better.

        Using this scan, large objects can hide behind small objects

        This scan has the feature that it will pick up a lone object 
        guaranteed at any distance.
        '''
        return self.__tank.distanceScan()

    def scan(self, num_points = 360, rel_angle_range = (-180, 180), height = 1):
        '''
        This function scans the map to find the other objects on it. The scan 
        works iteratively, based on the angle range (given relative to the 
        tank's current heading) and the number of points given. This is a more
        realistic scan, but does not work as well with smaller objects and 
        larger distances
        '''
        return self.__tank.scan(num_points, rel_angle_range, height)

    def ping_points(self, num_points = 360, rel_angle_range = (-180, 180), height = 1):
        '''Returns a list of tuples. Each tuple contains the point that can be seen from the tank
        relative to the tank, the relative angle that point was seen at, and the name of the 
        object hit, respectively'''


        return self.__tank.pingPoints(self. num_points, rel_angle_range, height)

    def ping_points_abs(self, num_points = 360, rel_angle_range = (-180, 180), height = 1):
        '''Returns a list of tuples. Each tuple contains the point that can be seen from the tank
        in absolute coordinates, the relative angle that point was seen at, and the name of the 
        object hit, respectively'''


        return self.__tank.pingPointsAbs(self. num_points, rel_angle_range, height)


    def ping_points(self, num_points = 360, rel_angle_range = (-180, 180), height = 1):
        '''Returns a list of tuples. Each tuple contains the distance to the point that can be 
        seen from the tank relative to the tank, the relative angle that point was seen at, 
        and the name of the object hit, respectively'''


        return self.__tank.pingDistance(self. num_points, rel_angle_range, height)

    #WEAPON CONTROL

    def fire(self, power = 1):
        '''Fires a projectile of a type specified by the tank's weapon
        @param power: 0 to 1, how much of the maximum velocity will be given to the projectile'''
        if (amt < 0 or power > 1):
            raise ValueError("Firing power must be between 0 and 1")

        return self.__tank.fire(power)

    def aim_at(self, point = (0,0,0), aim_low = True, power = 1 ):
    	'''Aims at the specified point, moving the tank's weapon
    	@param point: Point3, list, or tuple containing the x,y,z positions of the desired point
    	@param aim_low: Boolean deciding whether the lower trajectory or the higher trajectory will be chosen
    	@param power: 0 to 1, how much power will the bullet be fired with
    	Returns true if it is possible to hit the point
    	'''
    	return self.__tank.aimAt(self, point, power, aim_low)


    def fire_at(self, point, power = 1, aim_low = True):
    '''Calls aim_at and fire in succession'''

        if (self.aim_at(point, aim_low, power):
        	return self.fire(power)
       	else:
       		return false

    def move_weapon(self, heading, pitch):
    	'''Moves the weapon of the tank to the sepcified heading and pitch values
    	This happens instantaneously'''

    	self.__tank.setWeaponHp(heading, pitch)


    #GETTER METHODS?