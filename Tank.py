
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

    def __init__(self, world, attach, name = '', position = Vec3(0,0,0), orientation = Vec3(0,0,0), 
            turretPitch = 0): 

        #Constant Relevant Instatiation Parameters
        self._tankSideLength = 7
        friction = .3
        tankMass = 800.0

        # Rewrite constructor to include these?
        self._maxVel = 4
        self._maxRotVel = 1
        self._maxThrusterAccel = 5000
        self._breakForce = 1000
        turretRelPos = (0, 0, 0) #Relative to tank
       
        self._shape = BulletBoxShape(Vec3(1,1.5,.5)) #chassis
        self._transformState = TransformState.makePos(Point3(0, 0, 0)) #offset 
        print "Tank.__init__: " + name
        DynamicWorldObject.__init__(self, world, attach, name, position, self._shape, orientation, Vec3(0,0,0), mass = tankMass)   #Initial velocity must be 0
        self.__createVehicle(self._tankWorld.getPhysics())

        self._taskTimer = 0;
        self._nodePath.node().setFriction(friction)		
        self._nodePath.setPos(position)
        # Set up turret nodepath
        # (Nodepaths are how objects are managed in Panda3d)
 
        self.onTask = 0

        # Make collide mask (What collides with what)
        self._nodePath.setCollideMask(0xFFFF0000)
        
        self.movementPoint = Point3(10,10,0)

        #register tank
        world.registerTank(self)


        # Set up the 
    def __createVehicle(self,bulletWorld):
        '''
            Creates a vehicle, sets up wheels and does all the things
        '''
        
        self._nodePath.node().setMass(800.0)
         
        # Chassis geometry
        np  = loader.loadModel('box')

        np.reparentTo(self._nodePath)
        np.setScale(Vec3(1,1.5,.5)*2)
        np.setPos(-Vec3(1,1.5,.5)+Vec3(0, 0, 0))
       
        # Vehicle
        self.vehicle = BulletVehicle(bulletWorld, self._nodePath.node())
        self.vehicle.setCoordinateSystem(2)
        bulletWorld.attachVehicle(self.vehicle)
        
    
        wheelNP = loader.loadModel('box')
        wheelNP.setScale(.01,.01,.01) 

        wheelPos = [Point3(1, 1, 0),Point3(-1, 1, 0),
                    Point3(1, -1, 0),Point3(-1, -1, 0)]

        for i in range(4):
            wheel = self.vehicle.createWheel()
            wheel.setWheelAxleCs(Vec3(-2*(i%2)+1, 0, 0))
            wheel.setChassisConnectionPointCs(wheelPos[i])            
            self.__createWheel(wheel)
            self.vehicle.setSteeringValue(0,i)
            wheel.setRollInfluence((-2*(i%2)+1)*0.2)

    def __createWheel(self,wheel):
        '''
            sets up properties for wheel.
        '''
        wheel.setWheelDirectionCs(Vec3(0, 0, -1))
        wheel.setFrontWheel(False)
        wheel.setWheelRadius(0.15)
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

    def moveWeapon(self, heading = 0, pitch = 0):
        rot = self.getHpr()
        print "Tank.moveWeapon: ", rot
        print rot[0] + heading, rot[1] + pitch

        self.setWeaponHp(rot[0] + heading, rot[1] + pitch)

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


    def __bulletRays(self, numPoints, relAngleRange, height):
        '''Helper function for scans and pings. Runs through the 
        relAngleRange (two ints, in degrees) at the given numPoints and height.
        Runs a Bullet rayTestClosest to find the nearest hit.

        Returns a list of BulletClosestHitRayResult objects
        '''

        distanceOfMap = 100000
        results = []
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

            results.append((result, (angle - heading)*180 / math.pi))
        return results

    
    def scan(self, numPoints = 360, relAngleRange = (-180, 180), height = 1):
        '''
        This function scans the map to find the other objects on it. The scan 
        works iteratively, based on the angle range (given relative to the 
        tank's current heading) and the number of points given. This is a more
        realistic scan, but does not work as well with smaller objects and 
        larger distances
        '''
        found = []
        numFound = 0
        results = self.__bulletRays(numPoints, relAngleRange, height)

        for item in results:
            result = item[0]
            if result.hasHit():
                newNode = result.getNode()
                if newNode not in prevNodes:
                    found.append((newNode.getPrevTransform().getPos(), 
                        newNode.getName()))
                    prevNodes[newNode] = 0
                    numFound = numFound + 1     
        return found

    def pingPointsAbs(self, numPoints = 360, relAngleRange = (-180, 180), height = 1):
        '''Returns a list of absolute coordinate points on each of the 

        '''
        
        found = []     
        results = self.__bulletRays(numPoints, relAngleRange, height)

        for item in results:
            result = item[0]
            if result.hasHit():
                newNode = result.getNode()
                found.append((result.getHitPos(), item[1], newNode.getName()))

        return found

    def pingPoints(self, numPoints = 360, relAngleRange = (-180, 180), height = 1):
        found = self.pingPointsAbs(numPoints, relAngleRange, height)
        pos = self.getPos()

        for i in range(len(found)):
            hitPos = found[i][0]
            relPos = Point3(hitPos[0] - pos[0], hitPos[1] - pos[1], hitPos[2] - pos[2])
            found[i] = (relPos, found[i][1], found[i][2])
        return found

    def pingDistance(self, numPoints = 360, relAngleRange = (-180, 180), height = 1):
        found = self.pingPoints(numPoints, relAngleRange, height)

        for i in range(len(found)):
            relPos = found[i][0]
            distance = math.sqrt(relPos[0]**2 + relPos[1]**2)
            found[i] = (distance, found[i][1], found[i][2])

        return found


    def applyThrusters(self, right = 1, left = 1):    #set acceleration
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
        '''Moves using a distance. Adds an updateMoveLoc task to the taskMgr.
        '''        

        heading = self._nodePath.getH() * math.pi/180
        pos = self.getPos()
        self._stop = False
        
        #Of the form (goalLoc, startLoc, distance)
        self._moveLoc = (Point3(pos[0] + math.sin(heading) * dist, pos[1] - math.cos(heading) * dist, pos[2]), pos, dist)
        
        self._tankWorld.taskMgr.add(self.updateMoveLoc,'userTask',uponDeath=self.nextTask)

    def rotate(self, angle):
        angle = self.fixAngle(angle)
        heading = self.fixAngle(self._nodePath.getH())
        newH = self.fixAngle(heading + angle)

        self._moveLoc = (newH, heading, angle)
        self._stop = False

        self._tankWorld.taskMgr.add(self.updateRotateLoc, 'userTask', uponDeath=self.nextTask)


    def moveTime(self, moveTime):
        self._taskTimer = moveTime
        self._tankWorld.taskMgr.add(self.updateMove,'userTask',uponDeath=self.nextTask)
    
    def rotateTime(self, rotateTime):
        self._taskTimer = rotateTime
        self._tankWorld.taskMgr.add(self.updateRotate,'userTask',uponDeath=self.nextTask)


    def waitTime(self, waitTime):
        self._taskTimer = waitTime
        self._tankWorld.taskMgr.add(self.updateWait,'userTask',uponDeath=self.nextTask)

    def updateWait(self, task):
        '''
        Tasks called to wait
        '''
        dt = globalClock.getDt()
        self._taskTimer -= dt

        if self._taskTimer < 0: 
            return task.done
        return task.cont


    def updateRotateLoc(self, task):
        heading = self.fixAngle(self._nodePath.getH())
        toHeading = self._moveLoc[0]
        w = self._nodePath.node().getAngularVelocity()[2]

        #Right wheel direction for rotating in the direction of goal
        rFor = self._moveLoc[2]/abs(self._moveLoc[2]) 

        slowTheta = 2.5 * rFor
        brakePercent = w**2 / (2 * slowTheta * self._maxThrusterAccel)
        theta = self.fixAngle(toHeading - heading)
        thetaFromStart = self.fixAngle(heading - self._moveLoc[1])

        if self._stop:
            if abs(w) < .1:
                self._nodePath.node().setAngularVelocity(Vec3(0,0,0))
                self._nodePath.setH(self._moveLoc[0])
                return task.done
            self.applyBrakes()
            return task.cont
        
        if theta < slowTheta - .25:
            self.applyThrusters(-rFor * brakePercent, rFor * brakePercent)
        elif theta > slowTheta - .25:
            if w < self._maxRotVel:
                self.applyThrusters(rFor, -1 * rFor)
            else:
                self.applyThrusters(0,0)
        else:
            self.applyBrakes(brakePercent)
        
        if theta < .1: 
            self._stop = True
        if abs(thetaFromStart + .1) > abs(self._moveLoc[2]):
            self._stop = True
        
        return task.cont

    def updateMoveLoc(self, task):
        '''Bases how much to slow down on a = v^2/2x. 
        x is slowDist, chosen to play nice. 

        Generally accurate to 5cm, rarely 20cm or worse 

        Stops at an arbitrary low velocity because it will never exit
        at a lower minimum
        '''

        pos = self.getPos()
        toLoc = self._moveLoc[0]
        distance = math.sqrt((pos[0] - toLoc[0])**2 + (pos[1] - toLoc[1])**2)
        v = self._nodePath.node().getLinearVelocity().length()
        slowDist = 1
        brakePercent = v**2 / (2 * slowDist * self._breakForce)
        
        deltaPos = (self.getPos() - self._moveLoc[1])
        distFromStart = deltaPos.length()

        if self._stop:
            if v < .4:
                self._nodePath.node().setLinearVelocity(Vec3(0,0,0))
                self._nodePath.setPos(self._moveLoc[0])
                return task.done
            self.applyBrakes()
            return task.cont
        
        if distance < slowDist:
            self.applyBrakes(brakePercent * 1.1)
        elif distance > slowDist:
            if self._moveLoc[2] > 0:
                self.applyThrusters()
            else:
                self.applyThrusters(-1, -1)
        else:
            self.applyBrakes(brakePercent)
        
        if distance < .01: 
            self._stop = True
        if abs(distFromStart) > abs(self._moveLoc[2]):
            self._stop = True
        
        return task.cont

    
    def nextTask(self,task):
        self.onTask += 1
        if(self._tankWorld.isDead):
            return
        #if self.onTask >= len(self.taskList):
        #   return
        def getNumUserTask():
            
            taskAmount = 0
            for t in self._tankWorld.taskMgr.getTasks():

                if t.getName() == 'userTask':
                    taskAmount +=1
            return taskAmount

        pre = getNumUserTask()
        try:
            self.taskList.next()
            if(getNumUserTask() == pre):
                self.nextTask(task)

        except StopIteration:
            pass
        #self.taskList[self.onTask][0](self.taskList[self.onTask][1])
    
    def runTasks(self):
        self.onTask = 0
        self.nextTask(None)
    
    def setGenerator(self, gen):
        self.taskList = gen

    def updateMove(self, task):
        '''
        Task Called to do movement. This is called once perframe
        '''
        try:
            #small hack to prevent the first frame from doing all the tasks.
            dt = globalClock.getDt()    
            if dt > .1:
                return task.cont
            self._taskTimer -= dt

            if self._taskTimer < 0:
                self.applyBrakes(1)
            else:
                self.applyThrusters(1,1)

            if self._taskTimer < -1: #one second to stop
                return task.done
        except:
            print "ERROR in tank.updateMove"

        return task.cont

    def updateRotate(self, task):

        ''' called to do rotation. This is called once per frame
        '''
        try:
            dt = globalClock.getDt()
            #small hack to prevent the first frame from doing all the tasks.
            if dt > .1:
                return task.cont
            self._taskTimer -= dt


            if self._taskTimer < 0:
                self.applyBrakes(1)
            else:
                self.applyThrusters(1,-1)

            if self._taskTimer < -1: #one second to stop
                return task.done
        except:
            print "ERROR in tank.updateRotate"
        return task.cont

    def update(self, task):
        pass
        
    def aimAt(self, point, aimLow = True):
        self._weapon.aimAt(point, aimLow)


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

    def setWeapon(self, weopwn):
        self._weapon = weopwn

    def setSteering(self, angle):
        pass

    def fire(self, amt = 1):
        return self._weapon.fire(amt)        