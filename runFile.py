from TankWorld import TankWorld
from weapon.Blaster import Blaster
from Tank import *
import string

class PermissionError(Exception):
	'''Not sure how to name this. It it the error that gets raised when a user
	tries to access things they shouldn't
	'''

	def __init__(self, illegalChars, codeLine):
		self.value = illegalChars
		self.line = codeLine
		self.levelData = {}

	def __str__(self):
		return "\n" + self.line + "User defined scripts are not allowed to include \"" + self.value + "\""

def getInitialWhitespace(string):
	res = 0
	for letter in string:
		if letter == ' ':
			res += 1
		elif letter == '\t':
			res += 4
		else:
			break
	return ' ' * res

def getFunctionNames(lines):
	functions = []
	for line in lines:
		if line[0:4] == 'def ' or line.count(' def ')!=0:
			#function on this line
			c = line.split('def ')
			fName = c[1].split('(')[0]
			args = c[1].split('(')[1].split(')')[0].split(',')
			functions.append([fName, args])
	return functions

def runFile(filename, tankWorld):
	'''readFile opens and runs a user file, making sure that none of the 
	things in said file are illegal in TankWorld, in illegalStrings


	'''
	illegalStrings = ['__', 'TankWorld', 'tankWorld', 'WorldObject', 'Tank']
	appendToBeginning = '''

tank = tankWorld.getUserTank()
levelData = tankWorld.getLevelData()

def userFun(tank, levelData):
'''
	appendToEnd = '''
x = userFun(tank, levelData)
tank.setGenerator(x)
tank.runTasks()'''

	yieldClause = 'yield()\n'
	tabClause = '    '

	script = open(filename, 'rb')
	lines = script.readlines()
	userFunc = getFunctionNames(lines)
	#Check for illegal strings in file
	for line in lines:
		for illegal in illegalStrings:
			if illegal in line:
				print line
				raise PermissionError(illegal, line)

	#If no errors:
	code = appendToBeginning
	prevTabs = ''

	for line in lines:
		if line[len(line) - 1] != '\n':
			line += '\n'
		x = line.strip()

		prevTabs = getInitialWhitespace(line)
		
		if x == '' or ':' in line or '#' is x[0]:
			code = code + tabClause
		else:
			code = code + tabClause

		hasBroke = False
		for function in userFunc:

			if line.count(function[0]) != 0:
				#grab the user funcions
				spl = line.split(function[0]+'(')
				#if not on the line with def
				if spl[0].count('def ') ==0:
					args = spl[len(spl)-1]

					code = code + prevTabs + 'for i in '  + function[0]+'('+args.strip()+':\n'
					code = code + prevTabs+tabClause+tabClause+yieldClause
					hasBroke = True
					break

		if hasBroke:
			continue

		if x == '' or ':' in line or '#' is x[0]:
			code = code+ line
		else:
			code = code +line + tabClause + prevTabs + yieldClause



	code = code + appendToEnd
	
	filenamestr = filename.split('/')
	
	filename = filenamestr[0]+'/run' +filenamestr[1]
	f = open(filename, 'w')
	f.close()

	edited = open(filename, 'r+b')
	edited.seek(0)
	edited.write(code)
	edited.close()

	execfile(filename)










