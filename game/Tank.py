
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
        self._tankSize = Vec3(1, 1.5, .5) # Actually a half-size
        self._tankSideLength = max(self._tankSize)
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
        DynamicWorldObject.__init__(self, world, attach, name, position, self._shape, orientation, Vec3(0,0,0), mass = tankMass)   #Initial velocity must be 0
        self.__createVehicle(self._tankWorld.getPhysics())

        self._collisionCounter = 0
        self._taskTimer = 0
        self._nodePath.node().setFriction(friction)		
        self._nodePath.setPos(position)
        # Set up turret nodepath
        # (Nodepaths are how objects are managed in Panda3d)
 
        self.onTask = 0

        # Make collide mask (What collides with what)
        self._nodePath.setCollideMask(0xFFFF0000)
        #self._nodePath.setCollideMask(BitMask32.allOff())

        self.movementPoint = Point3(10,10,0)

        #print "Tank.__init__: " + name
        
        # Set up the 
    def __createVehicle(self,bulletWorld):
        '''
            Creates a vehicle, sets up wheels and does all the things
        '''
        
        self._nodePath.node().setMass(800.0)
         
        # Chassis geometry
        np  = loader.loadModel('media/tankBody.x')
        np.setHpr(90,0,0)
        np.reparentTo(self._nodePath)
        #np.setScale(self._tankSize*2)
        np.setPos(-self._tankSize+Vec3(1, 0, .5))
       
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

        self._weapon.setHp(heading,pitch)

    def moveWeapon(self, heading = 0, pitch = 0):
        rot = self.getHpr()

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
        self.wait(.1)
        potentialNPs = self._tankWorld.render.getChildren()

        found = []

        for np in potentialNPs:
            if type(np.node()) == BulletRigidBodyNode and np != self and not np.isHidden():
                
                pFrom = np.getPos(render) 
                #Fix for cubeObjects (z = 0). They collide with the floor
                if pFrom[2] < 1:
                    pFrom[2] = 1.1

                pTo = self.getPos() + self.getPos() - pFrom 
                #pTo is a Vec3, turned to a point for rayTest
                
                result = self._tankWorld.getPhysics().rayTestClosest(
                        pFrom, Point3(pTo[0], pTo[1], pTo[2]))

                if result.hasHit() and result.getNode() == self._nodePath.node():

                    #found.append((np.node().getPrevTransform().getPos(),
                    #    np.node().getName()))

                    found.append((np.getPos(render),
                        np.node().getName()))
                elif result.hasHit():
                    #print "Tank.distanceScan: ",
                    #print np, result.getNode(), pFrom, pTo
                    #print "Neigh"
                    x = 1                    

        return found


    def __bulletRays(self, numPoints, relAngleRange, height):
        '''Helper function for scans and pings. Runs through the 
        relAngleRange (two ints, in degrees) at the given numPoints and height.
        Runs a Bullet rayTestClosest to find the nearest hit.

        Returns a list of BulletClosestHitRayResult objects
        '''

        distanceOfMap = 100000
        results = []
        #scanResolution = numPoints / 360.0
        angleSweep = relAngleRange[1] - relAngleRange[0] + 0.0
        pos = self._nodePath.getPos()
        heading = self._nodePath.getH()
        
        for i in range(numPoints):

            if angleSweep == 0:
                angle = (heading + relAngleRange[0]) * (math.pi / 180)
            else:
                angle = (i / angleSweep + heading + relAngleRange[0]) * (math.pi / 180)

            pFrom = Point3(math.sin(angle) * self._tankSideLength + pos[0], 
                    math.cos(angle) *  self._tankSideLength + pos[1], height)
            pTo = Point3(math.sin(angle) * distanceOfMap + pos[0], 
                    math.cos(angle) * distanceOfMap + pos[1], height)
            result = self._tankWorld.getPhysics().rayTestClosest(pFrom, pTo)

            results.append((result, angle * 180 / math.pi - heading))

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
        prevNodes = dict()

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

        self._tankWorld.taskMgr.add(self.updateMoveLoc,'userTank '+self.getName(),uponDeath=self.nextTask)


    def rotate(self, angle):
        '''Rotate function. All angles given between 0 and 360
        Angle changes are between -180 and 180
        '''

        angle = angle % 360
        if angle > 180:
            angle -= 360

        
        heading = self.fixAngle(self._nodePath.getH())
        newH = self.fixAngle(heading + angle)

        self._moveLoc = (newH, heading, angle)
        self._stop = False

        self._tankWorld.taskMgr.add(self.updateRotateLoc, 'userTank '+self.getName(), uponDeath=self.nextTask)


    def moveTime(self, moveTime):
        self._taskTimer = moveTime
        self._tankWorld.taskMgr.add(self.updateMove,'userTank '+self.getName(),uponDeath=self.nextTask)
    
    def rotateTime(self, rotateTime):
        self._taskTimer = rotateTime
        self._tankWorld.taskMgr.add(self.updateRotate,'userTank '+self.getName(),uponDeath=self.nextTask)


    def wait(self, waitTime):
        self._taskTimer = waitTime
        self._tankWorld.taskMgr.add(self.updateWait,'userTank '+self.getName(),uponDeath=self.nextTask)

    def updateWait(self, task):
        '''
        Tasks called to wait
        '''
        try:
            if self._tankWorld.isRealTime():
                dt = globalClock.getDt()
            else:
                dt = 1.0/60.0
            #print "Tank.updateWait: ", dt
            self._taskTimer -= dt

            if self._taskTimer < 0: 
                return task.done

            return task.cont
        except:
            print "error, tank.wait"

    def updateRotateLoc(self, task):
        heading = self.fixAngle(self._nodePath.getH())
        toHeading = self._moveLoc[0]
        w = self._nodePath.node().getAngularVelocity()[2]

        #Right wheel direction for rotating in the direction of goal
        rFor = self._moveLoc[2]/abs(self._moveLoc[2]) 

        slowTheta = 1.5 * rFor
        brakePercent = w**2 / (2 * slowTheta * self._maxThrusterAccel)
        theta = self.fixAngle(toHeading - heading)
        if theta > 180:
            theta -= 360
        thetaFromStart = heading - self._moveLoc[1]
        thetaFromStart = thetaFromStart % 360
        if thetaFromStart > 180:
            thetaFromStart -= 360

        if self._stop:
            if abs(w) < .1:
                self._nodePath.node().setAngularVelocity(Vec3(0,0,0))
                self._nodePath.setH(self._moveLoc[0])
                return task.done
            self.applyBrakes()
            return task.cont
        
        if abs(theta) < slowTheta - .25:
            self.applyThrusters(-rFor * brakePercent, rFor * brakePercent)
        elif abs(theta) > slowTheta - .25:
            if w < self._maxRotVel:
                self.applyThrusters(rFor, -1 * rFor)
            else:
                self.applyThrusters(0,0)
        else:
            self.applyBrakes(brakePercent)
        
        if abs(theta) < .1:
            self._stop = True
        if abs(thetaFromStart + .1) > abs(self._moveLoc[2]):
            self._stop = True
        
        #emergency stop based on a long time.
        if task.time > 3:
            #print "Tank.updateRotateLoc", "your rotate could not be completed, sorry"
            return task.done
            
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
        slowAccel = 2
        slowDist = v**2 / (2 * slowAccel * self._breakForce)
        brakePercent = slowAccel * self._nodePath.node().getMass() / self._breakForce

        deltaPos = (self.getPos() - self._moveLoc[1])
        distFromStart = deltaPos.length()

        if self._stop:
            if v < .4:
                #self._nodePath.node().setLinearVelocity(Vec3(0,0,0))
                #self._nodePath.setPos(self._moveLoc[0])
                return task.done
            self.applyBrakes()
            return task.cont
        
        if distance < slowDist:
            self.applyBrakes(brakePercent * 1.1)
        elif distance > slowDist:
            if self._moveLoc[2] > 0:
                self.applyThrusters(1,1)
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
        self._nodePath.node().setActive(True)
        self.onTask += 1
        if(self._tankWorld.isDead or self._tankWorld.isOver):
            return
        #if self.onTask >= len(self.taskList):
        #   return
       
        def getNumUserTask():
            
            taskAmount = 0
            for t in self._tankWorld.taskMgr.getTasks():

                if t.getName() == 'userTank '+self.getName():
                    taskAmount +=1
            return taskAmount

        pre = getNumUserTask()
        try:
            self.taskList.next()
            if(getNumUserTask() == pre):
                self.nextTask(task)

        except StopIteration:
            #print 'Tank.nextTask error'
            pass
        #self.taskList[self.onTask][0](self.taskList[self.onTask][1])
    
    def runTasks(self):
        self.onTask = 0
        self.nextTask(None)
    
    def setGenerator(self, gen):
        self.taskList = gen
        self.runTasks()

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
        
    def aimAt(self, point, amt = 1, aimLow = True):
        return self._weapon.aimAt(point, aimLow)

    def setWeapon(self, weopwn):
        self._weapon = weopwn


    def fire(self, amt = 1):

        x = self._weapon.fire(amt)        
        self.wait(.1)
        return x

    def deleteAfter(self, task = None):
        if not self._nodePath.is_empty():
            x = self._nodePath.node()
            self._tankWorld.removeRigidBody(x)
            self.hide()                 
            self._tankWorld.lose()                               
            #self._nodePath.detachNode()

    def handleCollision(self, collide, taskName):
        self._collisionCounter += 1

        forReal = True

        hitBy = collide.getNode0()
        if hitBy.getName() == self._nodePath.node().getName():
            hitBy = collide.getNode1()

        allowedNames = ['floor', 'wall', 'State']

        for name in allowedNames:
            if name in hitBy.getName():
                forReal = False

        if not self._nodePath.is_empty():        
            
            if forReal:
                print "Tank.handleCollision:(pos) ", self.getPos(), 'obj 1', collide.getNode0().getName(), 'obj 2', collide.getNode1().getName()
            
                self._tankWorld.taskMgr.remove(taskName)
                self._tankWorld.doMethodLater(.01, self.deleteAfter, 'deleteAfter')

        else:
            print "Tank.handleCollision Failed to have _nodepath"
            self._tankWorld.taskMgr.remove(taskName)