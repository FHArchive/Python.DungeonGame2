"""
Year 2017 (ammendments made 10/2018)
Author Kieran

A simple dungeon game that runs in the command line, avoid the monsters to get
to the door.
"""
import sys
import random

level = 1
# Set gameEnd to False for experimental, endless gamemode. Note there will be
# graphics glitches!
gameEnd = True


def spawn(size):
	"""
	Method spawn
	Inputs [none]
	Outputs spawnX, spawnY: integers
	This method gives the player random coordinates
	"""
	# Use SystemRandom
	systemRandom = random.SystemRandom()
	spawnY = systemRandom.randint(0, size)
	spawnX = systemRandom.randint(0, size)
	return spawnX, spawnY


def movement(playerX, playerY, size):
	"""
	Method movement
	Inputs playerX, playerY, size: integers
	outputs playerX, playerY: integers
	This method updates the player position based on the user input
	"""
	movement = input(
		"\nIn which direction would you like to move? (Use WASD) \n>>>")
	movement = movement.upper()
	try:
		movement = movement[0]
	except BaseException:
		print()
	if movement == "D":
		playerX += 1
		if playerX > size:
			playerX = size
	if movement == "A":
		playerX -= 1
		if playerX < 0:
			playerX = 0
	if movement == "S":
		playerY += 1
		if playerY > size:
			playerY = size
	if movement == "W":
		playerY -= 1
		if playerY < 0:
			playerY = 0
	print("Your new position is ({},{})".format(playerX, playerY))
	return playerX, playerY


def moveMonster(monsters, size):

	# Use SystemRandom
	systemRandom = random.SystemRandom()
	selection = systemRandom.randint(0, len(monsters) - 1)
	monsterX = monsters[selection][0]
	monsterY = monsters[selection][1]
	move = systemRandom.randint(0, 3)

	if move == 0:
		monsterX += 1
		if monsterX > size:
			monsterX = size

	if move == 1:
		monsterY += 1
		if monsterY > size:
			monsterY = size
	if move == 2:
		monsterX -= 1
		if monsterX < 0:
			monsterX = 0
	if move == 3:
		monsterY -= 1
		if monsterY < 0:
			monsterY = 0

	return monsterX, monsterY, selection


def checkSpawns(playerX, playerY, monsters, doorX, doorY, monsterNo):
	"""
	Method checkSpawns
	Inputs playerX, playerY, doorX, doorY, monsterNo: integers; monsters: array
	Outputs success: integer
	This method checks that the spawns do not clash. Returns 1 if they do not, 0 if
	they do.
	"""
	for m in range(monsterNo):
		monsterX = monsters[m][0]
		monsterY = monsters[m][1]
		if playerX == monsterX:
			if playerY == monsterY:
				return 0
		if doorX == monsterX:
			if doorY == monsterY:
				return 0

		for m2 in range(m + 1, monsterNo):
			monster2X = monsters[m2][0]
			monster2Y = monsters[m2][1]
			if monster2X == monsterX:
				if monster2Y == monsterY:
					return 0

	if playerX == doorX:
		if playerY == doorY:
			return 0
	return 1


def collisionMonster(playerX, playerY, monsters, monsterNo):
	"""
	Method collisionMonster
	Inputs playerX, playerY, monsters, monsterNo: integers
	Outputs success, level: integers
	This method checks for collisions with any monster on the board. If there is a
	collision, 1 is returned along with the current level (0 for no collisions)
	"""
	for m in range(monsterNo):
		monsterX = monsters[m][0]
		monsterY = monsters[m][1]
		if playerX == monsterX:
			if playerY == monsterY:
				print("\nYou were consumed by the monster...")
				level = 1
				return 1, level
	return 0, level


def collisionDoor(playerX, playerY, doorX, doorY, level):
	"""
	Method collisionDoor
	Inputs playerX, playerY, doorX, doorY, level: integers
	Outputs success, level: integers
	This method checks for collisions with the door on the board. If there is a
	collision, 1 is returned along with the current level (0 for no collision)
	"""
	if playerX == doorX:
		if playerY == doorY:
			print("\nYou made it out of the dungeon alive!")
			level += 1
			return 1, level
	return 0, level


def render(playerX, playerY, doorX, doorY, monsters, size, monsterNo):
	"""
	Method render
	Inputs playerX, playerY, doorX, doorY, monsters,size,monsterNo: integers
	Outputs [none]
	This method displays the board
	"""
	print()
	print("  ", end="")
	for q in range(size + 1):
		for _gap in range(3 - len(str(q))):
			print(" ", end="")
		print("", q, end="")
	print()
	for y in range(size + 1):
		print("", y, end="")
		for x in range(size + 2):
			print("|", end="")
			spaces = 3
			if x == playerX and y == playerY:
				print("P", end="")
				spaces -= 1
			elif x == doorX and y == doorY:
				print("D", end="")
				spaces -= 1
			else:

				for m in range(monsterNo):
					monsterX = monsters[m][0]
					monsterY = monsters[m][1]
					if x == monsterX and y == monsterY:
						print("M", end="")
						spaces -= 1
			for _space in range(spaces):
				print(" ", end="")
		print()


def game(level, gameEnd):
	"""
	Mehtod game
	Inputs level, gameEnd: integers
	Outputs [none]
	This method is the main method and calls the other functions
	"""
	if level > 8 and gameEnd:
		print("Well done, you have beat the dungeon!")
		sys.exit()
	canContinue = 0
	death = 0
	win = 0
	monsters = []
	print("\nLevel:", level, end="\n\n")
	size = level + 1
	while canContinue == 0:
		monsters = []
		playerX, playerY = spawn(size)
		doorX, doorY = spawn(size)
		monsterNo = int(level**1.2)
		for _monster in range(monsterNo):
			monsterX, monsterY = spawn(size)
			monsterPos = []
			monsterPos.append(monsterX)
			monsterPos.append(monsterY)
			monsters.append(monsterPos)
		canContinue = checkSpawns(
                    playerX,
                    playerY,
                    monsters,
                    doorX,
                    doorY,
                    monsterNo)

	print("The {} is at ({},{})".format("player", playerX, playerY))
	for m in range(monsterNo):
		monsterX = monsters[m][0]
		monsterY = monsters[m][1]
		print("Monster {} is at ({},{})".format(m + 1, monsterX, monsterY))
	print("The {} is at ({},{})".format("door", doorX, doorY))

	render(playerX, playerY, doorX, doorY, monsters, size, monsterNo)

	while death == 0 and win == 0:
		playerX, playerY = movement(playerX, playerY, size)
		monsterX, monsterY, selection = moveMonster(monsters, size)
		monsters[selection][0] = monsterX
		monsters[selection][1] = monsterY
		death, level = collisionMonster(playerX, playerY, monsters, monsterNo)
		if death == 0:
			render(playerX, playerY, doorX, doorY, monsters, size, monsterNo)
		win, level = collisionDoor(playerX, playerY, doorX, doorY, level)
	game(level, gameEnd)


game(level, gameEnd)
