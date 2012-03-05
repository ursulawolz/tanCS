
from DynamicWorldObject import *
from direct.task import Task
from panda3d.core import TransformState
from panda3d.bullet import BulletVehicle

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
       
        self._shape = BulletBoxShape(Vec3(0.7, 1.5, 0.5)) #chassis
        self._transformState = TransformState.makePos(Point3(0, 0, .5)) #offset 
        
        DynamicWorldObject.__init__(self, world, attach, name, xCoord, yCoord, zCoord, self._shape, heading, pitch, roll, 0, 0, 0, mass = 800.0) #Initial velocity must be 0
        self.__createVehicle(world)

        self._nodePath.node().setFriction(friction)		

        # Set up turret nodepath
        # (Nodepaths are how objects are managed in Panda3d)
        self._weapon = weapon

        ## FILLER:
        ## Set up the weapon initial conditions !!!
        ## END FILLER

        # Make collide mask (What collides with what)
        self._nodePath.setCollideMask(0xFFFF0000)


        # Set up the 
    def __createVehicle(self,bulletWorld):
        '''
            Creates a vehicle, sets up wheels and does all the things
        '''
        
        self._nodePath.setPos(0, 0, 1)
        self._nodePath.node().setMass(800.0)
         
        # Chassis geometry
        #loader.loadModel('path/to/model').reparentTo(chassisNP)
         
        # Vehicle
        self.vehicle = BulletVehicle(bulletWorld, self._nodePath.node())
        self.vehicle.setCoordinateSystem(2)
        bulletWorld.attachVehicle(self.vehicle)
        self._nodePath.setPos(0,0,1)
    
        wheelNP = loader.loadModel('box')
        wheelNP.setScale(.01,.01,.01) 

        wheelPos = [Point3(0.8, 1.1, 0.3),Point3(-0.8, 1.1, 0.3),
                    Point3(0.8, -1.1, .3),Point3(-0.8, -1.1, .3)]

        for i in range(4):
            wheel = self.vehicle.createWheel()
            wheel.setWheelAxleCs(Vec3(-2*(i%2)+1, 0, 0))
            wheel.setChassisConnectionPointCs(wheelPos[i])
            wheel.setFrontWheel(i/2)
            self.__createWheel(wheel)
  

    def __createWheel(self,wheel):
        '''
            sets up properties for wheel.
        '''
        wheel.setWheelDirectionCs(Vec3(0, 0, -1))
        wheel.setWheelRadius(0.25)
        wheel.setMaxSuspensionTravelCm(40.0)
        wheel.setSuspensionStiffness(40.0)
        wheel.setWheelsDampingRelaxation(2.3)
        wheel.setWheelsDampingCompression(4.4)
        wheel.setFrictionSlip(100.0)
        wheel.setRollInfluence(0.1)

    def getWheels(self):
        '''
            returns a list of wheelPos
        '''
        return self.vehicle.getWheels()

    def setWeaponHp(self, heading, pitch):
        '''
        float heading
        float pitch
        '''
		
        #Note: currently instantaneous - we need to figure out how to move continuously (or not, Turrets don't collide...)
        self._weapon.setHp(heading,pitch)

    def distanceScan(self):
        '''
        This scan projects rays from the objects in the field toward the tank in question. This scan does not perform as well as scan when the 
        objects are bunched together. When small objects are spread out reasonably (more than 5 at a viewing range of 50), this scan performs better.

        Using this scan, large objects can hide behind small objects

        This scan has the feature that it will pick up a lone object guaranteed at any distance.
        '''

        potentialNPs = self._tankWorld.render.getChildren()
        found = []

        for np in potentialNPs:
            if type(np.node()) == BulletRigidBodyNode and np != self:
                pFrom = np.getPos() 
                pTo = self.getPos() + self.getPos() - pFrom #Creates a Vec3, turned to a point in the call
                result = self._tankWorld.getPhysics().rayTestClosest(pFrom, Point3(pTo[0], pTo[1], pTo[2]))
                if result.hasHit() and result.getNode() == self._nodePath.node():
                    found.append((np.node().getPrevTransform().getPos(), np.node().getName()))      
        return found



    
    def scan(self, numPoints = 360, relAngleRange = (-180, 180), height = 1):
        '''
        This function scans the map to find the other objects on it. The scan works iteratively, based on the angle range (given relative to the tank's current heading)
        and the number of points given. This is a more realistic scan, but does not work as well with smaller objects and larger distances
        '''
        distanceOfMap = 100000
        found = []
        numFound = 0
        scanResolution = numPoints / 360.0
        pos = self._nodePath.getPos()   
        prevNodes = dict()
        heading = self._nodePath.getH()
        for i in range(int(relAngleRange[0] * scanResolution), int(relAngleRange[1] * scanResolution) + 1):
            angle = i * math.pi / (180 * scanResolution) + heading
            pFrom = Point3(math.sin(angle) * self._tankSideLength + pos[0], math.cos(angle) *  self._tankSideLength + pos[1], height)
            pTo = Point3(math.sin(angle) * distanceOfMap + pos[0], math.cos(angle) * distanceOfMap + pos[1], height)
            result = self._tankWorld.getPhysics().rayTestClosest(pFrom, pTo)
            if result.hasHit():
                newNode = result.getNode()
                if newNode not in prevNodes:
                    found.append((newNode.getPrevTransform().getPos(), newNode.getName()))
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

