
from DynamicWorldObject import *
from direct.task import Task

####### WE NEED TO START DEFINING IN HERE WHAT THE VARIABLES DO. #######
####### Currently it is impossible to tell what heading, etc are #######

from DynamicWorldObject import DynamicWorldObject

class Tank(DynamicWorldObject):

    '''Child of WorldObject, with all of the things that makes a Tank a tank.

    Includes a Turret and whatever Bullets it fires and are still alive. (Bullets not written yet.)

    '''
    def __init__(self, world, attach, weapon = None, name = '', xCoord = 0, yCoord = 0, zCoord = 0, heading = 0, pitch = 0, roll = 0, turretPitch = 0): 

        #Constant Relevant Instatiation Parameters
        self._tankSideLength = 7
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

    def perfectScan(self):
        '''
        This scan projects rays from the objects in the field toward the tank in question. This scan does not perform as well as scan when the 
        objects are bunched together. 

        Using this scan, large objects can hide behind small objects
        '''

        potentialNPs = self._tankWorld.render.getChildren()
        found = []

        for np in potentialNPs:
            if type(np.node()) == BulletRigidBodyNode and np != self:
                pFrom = np.getPos() 
                pTo = self.getPos() + self.getPos() - pFrom #Creates a Vec3, turned to a point in the call
                result = self._tankWorld.getPhysics().rayTestClosest(pFrom, Point3(pTo[0], pTo[1], pTo[2]))
                if result.hasHit() and result.getNode() == self._nodePath.node():
                    found.append((np.node().getPrevTransform(), np.node().getName()))      
        return found



    
    def scan(self, numPoints = 360, relAngleRange = (-180, 180)):
        '''
        This function scans the map to find the other objects on it. The scan works iteratively, based on the angle range (given relative to the tank's current heading)
        and the number of points given. This is a more realistic scan.
        '''
        distanceOfMap = 1000
        found = []
        numFound = 0
        scanResolution = numPoints / 360.0
        pos = self._nodePath.getPos()   
        prevNodes = dict()
        heading = self._nodePath.getH()
        for i in range(int(relAngleRange[0] * scanResolution), int(relAngleRange[1] * scanResolution) + 1):
            angle = i * math.pi / (180 * scanResolution) + heading
            pFrom = Point3(math.sin(angle) * self._tankSideLength + pos[0], math.cos(angle) *  self._tankSideLength + pos[1], pos[2])
            pTo = Point3(math.sin(angle) * distanceOfMap + pos[0], math.cos(angle) * distanceOfMap + pos[1], pos[2])
            result = self._tankWorld.getPhysics().rayTestClosest(pFrom, pTo)    
            if result.hasHit():
                newNode = result.getNode()
                if newNode not in prevNodes:
                    found.append((newNode.getPrevTransform(), newNode.getName()))
                    prevNodes[newNode] = 0
                    numFound = numFound + 1     
        return found

    ### METHODS TO DEFINE:

    def applyThrusters(self, amt=1):    #set acceleration
        '''change acceleration to a percent of the maximum acceleration'''
        if amt > 1 or amt < 0:
            raise ValueError("amt must be between 0 and 1")
        else:
            angle = self.nodePath.getH() #Apply force in current direction
            magnitude = amt * (self._maxThrusterAccel + self.nodePath.node().getFriction() ) * self._nodePath.node(),getMass()
            force = Vec3(magnitude * math.cos(angle), magnitude * math.sin(angle), 0)
            self.nodePath.node().applyForce(force)

        

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

