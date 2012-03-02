<<<<<<< HEAD
from DynamicWorldObject import *
=======
####### WE NEED TO START DEFINING IN HERE WHAT THE VARIABLES DO. #######
####### Currently it is impossible to tell what heading, etc are #######

from DynamicWorldObject import DynamicWorldObject
>>>>>>> 384873c965b41dc24ad96b477723afbe0ec3bdae

class Tank(DynamicWorldObject):

    '''Child of WorldObject, with all of the things that makes a Tank a tank.

    Includes a Turret and whatever Bullets it fires and are still alive. (Bullets not written yet.)

    '''
    def __init__(self, world, attach, weapon = None, name = '', xCoord = 0, yCoord = 0, zCoord = 0, heading = 0, pitch = 0, roll = 0, turretPitch = 0):
		
        #Constant Relevant Instatiation Parameters
        tankSideLength = 7
        friction = .3

        # Rewrite constructor to include these?
        self._maxVel = 20
        self._maxThrusterAccel = 4
        turretRelPos = (0, 0, 0) #Relative to tank
        
        # Create the tank's shape
        self._shape = BulletBoxShape(Vec3(tankSideLength, tankSideLength, tankSideLength)) 
        DynamicWorldObject.__init__(self, world, attach, name, xCoord, yCoord, zCoord, self._shape, heading, pitch, roll, 0, 0, 0, mass = 800.0) #Initial velocity must be 0
		
        self._nodePath.node().setFriction(friction)		
		
        # Set up turret nodepath
        # (Nodepaths are how objects are managed in Panda3d)
        self._weapon = weapon
	
        ## FILLER:
        ## Set up the weapon initial conditions !!!
        ## END FILLER

        # Make collide mask (What collides with what)
        self._nodePath.setCollideMask(0xFFFF0000)

	
    def setWeaponHp(self, heading, pitch):
        '''
        float heading
        float pitch
        '''
		
        #Note: currently instantaneous - we need to figure out how to move continuously (or not, Turrets don't collide...)
        self._weapon.setHp(heading,pitch)


    ### METHODS TO DEFINE:

    def applyThrusters(self, amt=1):    #set acceleration
        '''change acceleration to a percent of the maximum acceleration'''
        self.
        pass

    def setVel(self, goal	):
        pass 

    def move(self, dist):   
        pass

    def backward(self,dist):
        if (dist <=0):
            raise ValueError("Distance must be positive")
        else:
            self.move(-1*distance)
    
    def forward(self, distance):
	if (dist <=0):
            raise ValueError("Distance must be positive")
        else:
            self.move(distance)

    def applyRotThrusters(self,amt=1):
        pass

    def setRotVel(self, goal):
        pass

    def gotoAngle(self,deg):
        pass

    def fire(self):
        pass
