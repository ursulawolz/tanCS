
from DynamicWorldObject import *
from direct.task import Task
from panda3d.core import TransformState
from panda3d.bullet import BulletVehicle

####### WE NEED TO START DEFINING IN HERE WHAT THE VARIABLES DO. #######
####### Currently it is impossible to tell what heading, etc are #######

from DynamicWorldObject import DynamicWorldObject

class Tank(DynamicWorldObject):

    '''Child of WorldObject, with all of the things that makes a Tank a tank.

    Includes a Weapon
    '''

    def __init__(self, world, attach, weapon = None, name = '', position = Vec3(0,0,0), orientation = Vec3(0,0,0), 
            turretPitch = 0): 

        #Constant Relevant Instatiation Parameters
        self._tankSideLength = 7
        friction = .3
        tankMass = 800.0

        # Rewrite constructor to include these?
        self._maxVel = 4
        self._maxThrusterAccel = 5000
        self._breakForce = 1000
        turretRelPos = (0, 0, 0) #Relative to tank
       
        self._shape = BulletBoxShape(Vec3(0.7, 1.5, 0.5)) #chassis
        self._transformState = TransformState.makePos(Point3(0, 0, .5)) #offset 
        
        DynamicWorldObject.__init__(self, world, attach, name, position, self._shape, orientation, Vec3(0,0,0), mass = tankMass)   #Initial velocity must be 0
        self.__createVehicle(self._tankWorld.getPhysics())

        self._taskTimer = 0;
        self._nodePath.node().setFriction(friction)		

        # Set up turret nodepath
        # (Nodepaths are how objects are managed in Panda3d)
        self._weapon = weapon

        ## FILLER:
        ## Set up the weapon initial conditions !!!
        ## END FILLER
        self.taskList = [[self.moveTime,1], [self.moveTime,1], [self.rotateTime,1], [self.moveTime,1], [self.rotateTime,1], [self.rotateTime,2],[self.moveTime,2], [self.rotateTime,2],[self.moveTime,2], [self.rotateTime,2]]
        self.onTask = 0

        #send of the first task
        self.taskList[0][0](self.taskList[0][1])

        # Make collide mask (What collides with what)
        self._nodePath.setCollideMask(0xFFFF0000)
        
        self.movementPoint = Point3(10,10,0)

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
            #wheel.setFrontWheel(i/2)
            wheel.setFrontWheel(False)
            self.__createWheel(wheel)
            self.vehicle.setSteeringValue(0,i)
            wheel.setRollInfluence((-2*(i%2)+1)*0.2)

    def __createWheel(self,wheel):
        '''
            sets up properties for wheel.
        '''
        wheel.setWheelDirectionCs(Vec3(0, 0, -1))
        wheel.setWheelRadius(0.35)
        wheel.setMaxSuspensionTravelCm(40.0)
        wheel.setSuspensionStiffness(40.0)
        wheel.setWheelsDampingRelaxation(2.3)
        wheel.setWheelsDampingCompression(4.4)
        wheel.setFrictionSlip(100.0)
        

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
		
        #Note: currently instantaneous - we need to figure out how to move 
        #continuously (or not, Turrets don't collide...)
        self._weapon.setHp(heading,pitch)

    def distanceScan(self):
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

        potentialNPs = self._tankWorld.render.getChildren()
        found = []

        for np in potentialNPs:
            if type(np.node()) == BulletRigidBodyNode and np != self:
                pFrom = np.getPos() 
                pTo = self.getPos() + self.getPos() - pFrom 
                #pTo is a Vec3, turned to a point for rayTest
                
                result = self._tankWorld.getPhysics().rayTestClosest(
                        pFrom, Point3(pTo[0], pTo[1], pTo[2]))
                if result.hasHit() and result.getNode() == self._nodePath.node():
                    found.append((np.node().getPrevTransform().getPos(),
                        np.node().getName()))      
        return found



    
    def scan(self, numPoints = 360, relAngleRange = (-180, 180), height = 1):
        '''
        This function scans the map to find the other objects on it. The scan 
        works iteratively, based on the angle range (given relative to the 
        tank's current heading) and the number of points given. This is a more
        realistic scan, but does not work as well with smaller objects and 
        larger distances
        '''
        distanceOfMap = 100000
        found = []
        numFound = 0
        scanResolution = numPoints / 360.0
        pos = self._nodePath.getPos()   
        prevNodes = dict()
        heading = self._nodePath.getH()
        
        for i in range(int(relAngleRange[0] * scanResolution), 
                int(relAngleRange[1] * scanResolution) + 1):
            
            angle = i * math.pi / (180 * scanResolution) + heading
            pFrom = Point3(math.sin(angle) * self._tankSideLength + pos[0], 
                    math.cos(angle) *  self._tankSideLength + pos[1], height)
            pTo = Point3(math.sin(angle) * distanceOfMap + pos[0], 
                    math.cos(angle) * distanceOfMap + pos[1], height)
            result = self._tankWorld.getPhysics().rayTestClosest(pFrom, pTo)
            
            if result.hasHit():
                newNode = result.getNode()
                if newNode not in prevNodes:
                    found.append((newNode.getPrevTransform().getPos(), 
                        newNode.getName()))
                    prevNodes[newNode] = 0
                    numFound = numFound + 1     
        return found

    ### METHODS TO DEFINE:

    def applyThrusters(self, right, left):    #set acceleration
        '''change acceleration to a percent of the maximum acceleration'''
        
        #if right > 1 or amt < 0:
        #   raise ValueError("amt must be between 0 and 1")
        
        # tankNode = self._nodePath.node()
        # angle = self.nodePath.getH() #Apply force in current direction
        # magnitude = amt * (self._maxThrusterAccel) + (tankNode.getFriction() * 
        #     self._nodePath.node().getMass())
        # force = Vec3(magnitude * math.cos(angle), 
        #     magnitude * math.sin(angle), 0)
        # self.nodePath.node().applyForce(force)
        self.vehicle.reset_suspension()
        self.applyBrakes(0)
        vel = self.vehicle.getChassis().getLinearVelocity()

        for i in range(4):
            self.vehicle.applyEngineForce(0,i)  
            self.vehicle.setBrake(0,i)

        if vel.length() < self._maxVel:
            self.vehicle.applyEngineForce(-left*self._maxThrusterAccel,0)
            self.vehicle.applyEngineForce(right*self._maxThrusterAccel,1)
            self.vehicle.applyEngineForce(-left*self._maxThrusterAccel,2)
            self.vehicle.applyEngineForce(right*self._maxThrusterAccel,3)
            #for i in range(0,1):
            #    self.vehicle.applyEngineForce((left*(i)%2+right*(i+1)%2)*self._maxThrusterAccel,i)

            #for i in range(2):
            #   self.vehicle.applyEngineForce((left*(i)%2+right*(i+1)%2)*self._maxThrusterAccel,i+2)
                #self.vehicle.applyEngineForce((2*i%2-1)*engineForce,i)
                ## for 1 and 3useleft 
                ## for 0 and 2 use right

                

        else:
            for i in range(4):
                #self.vehicle.applyEngineForce((2*i%2-1)*engineForce,i)
                self.vehicle.applyEngineForce(0,i)
            
    def applyBrakes(self, amt=1):
        
        for i in range(4):
            #self.vehicle.applyEngineForce((2*i%2-1)*engineForce,i)
            self.vehicle.applyEngineForce(0,i)
            self.vehicle.setBrake(amt*self._breakForce,i)
        

    def setVel(self, goal	):
        pass 

    def move(self, dist):   
        
        '''	Two possible ways to do this'''

        ''' 	First way: Create a target location. Each iteration, calculate the distance between current position and target location. Break accordingly.'''
        #	def move(self,dist):
        #		Calculate target location (x,y,z)
        #		moveLocation(self,location)
        #	
        #	def moveLocation(self,location):
        #		if Distance between Current Location and Target Location equals (Current Velocity)^2/(2*Max_Deceleration):
        #			self.applyBreaks(Max_Deceleration)
        #		else
        #			self.applyThrusters
        #		moveLocation(self,location)
        '''	Second Way: Update required distance to travel after each iteration. Break accordingly.'''
        #	def move(self,dist):
        #		if Distance between Current Location and Target Location equals (Current Velocity)^2/(2*Max_Deceleration):
        #			self.applyBreaks(Max_Deceleration)
        #		else
        #			self.applyThrusters
        #		Calculate distance travelled within this iteration.
        #		newDistance=dist-distanceTravelled
        #		move(self, newDistance)
        pass
    def moveTime(self, moveTime):
        self._taskTimer = moveTime
        taskMgr.add(self.updateMove,'updateMove',uponDeath=self.nextTask)
    def rotateTime(self, rotateTime):
        self._taskTimer = rotateTime
        taskMgr.add(self.updateRotate,'updateRotate',uponDeath=self.nextTask)
    def nextTask(self,task):
        self.onTask += 1
        if self.onTask >= len(self.taskList):
            return
        
        print taskMgr.getTasks()
        self.taskList[self.onTask][0](self.taskList[self.onTask][1])

    def updateMove(self, task):
        print "doing movement"
        dt = globalClock.getDt()
        self._taskTimer -= dt

        if self._taskTimer < 0:
            self.applyBrakes(1)
        else:
            self.applyThrusters(1,1)

        if self._taskTimer < -1: #one second to stop
            return task.done

        return task.cont

    def updateRotate(self, task):
        dt = globalClock.getDt()
        self._taskTimer -= dt

        if self._taskTimer < 0:
            self.applyBrakes(1)
        else:
            self.applyThrusters(1,-1)

        if self._taskTimer < -1: #one second to stop
            return task.done
        return task.cont

    def update(self, task):
        pass
        

    def backward(self, dist):
        if dist <=0:
            raise ValueError("Distance must be positive")
        else:
            self.move(-1*distance)
    
    def forward(self, distance):
	if (dist <=0):
            raise ValueError("Distance must be positive")
        else:
            self.move(distance)

    def setSteering(self, angle):
        pass

    def fire(self):
        pass

