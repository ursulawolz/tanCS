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

		vel = direction.normalize() * speed #Vec3

		Projectile(weapon, name, shape, vel, mass, damage)