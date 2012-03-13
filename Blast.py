from Projectile import *

class Blast(Projectile):

	'''Class Blast - Dynamic World Object fired by Blaster'''

	def __init__(self, weapon, power):
		

		#Parameters to be set
		speed = 100 * power
		damage = 1 #Blast should be weakest, base damage
		mass = .1 

		direction = weapon.getTank()._nodePath.getHpr()		
		shape = BulletSphereShape(.2)
		name = weapon.getTank()._nodePath.node().getName() + ' blast'

		pos = weapon.getTank().getPos()
		pos = Point3(pos[0], pos[1], pos[2] + 5)

		#print direction

		direction.normalize()
		vel = direction * speed #LVecBase3f
		vel = Vec3(vel[0], vel[1], vel[2])

		#print direction, vel

		Projectile(weapon, pos, name, shape, vel, mass, damage)