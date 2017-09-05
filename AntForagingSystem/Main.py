import numpy as np
import array as ar
import matplotlib
import matplotlib.pyplot as plt
import time
import os

from AntForagingSystem.Plot import Environment
from AntForagingSystem.AntAgent import AntAgent


def main():
	os.environ["QT_API"] = "pyside"
	matplotlib.use('Qt5Agg')
	
	#===============================================================================
	# Function Parameters
	#===============================================================================
	nbrHuman = 0
	fieldSize = 40
	Agents = []
	lifeTime = 200
	HOME = 1
	FOOD = 0
	nestPosition = fieldSize//2  #general nest position
	#keep the parameters under or equal to 0.2
	foodDiff = 0.001
	homeDiff = 0.01	
	#
	collectedSugar = 0
	plotDelay = 0.001 #--> not working right now
	#
	maxFoodAmount = 100
	maxFoodPheromone = 3.5
	maxHomePheromone = 90
	#
	npaFood = np.array([])
	npaIterations = np.array([])
	#
	nIterations = 200000
	#
	#nestPosition = None
	# for the plotting
	subPlot1_Home, subPlot2_Food,  pheromoneFigure, pheroHomePlot, pheroFoodPlot = Environment.PheromoneGridFigure(fieldSize, maxFoodPheromone, maxHomePheromone)
	antsSubPlot, antsFigure, antsPlotFood, antPlotHome, sugarPlot, nestPlot = Environment.AntGridFigure(fieldSize, maxFoodAmount, nestPosition)
	
	
	#===============================================================================
	# GRID RESOURCES --> ANTS
	#===============================================================================
	gridInfo = np.zeros((fieldSize,fieldSize,3))
	for i in range(fieldSize):
		for j in range(fieldSize):
			gridInfo[i][j] = [0,0,0] #[PheromeForaging, PheromoneRetHome, SugarAmount]
		#
	#
	
	for i in range(nestPosition-2,nestPosition+3):
		for j in range(nestPosition-2,nestPosition+3):
			gridInfo[i][j][2] = -1
		#
	#
	
	#===========================================================================
	# PLOT INFO 
	#===========================================================================
	plotInfo = np.zeros((fieldSize,fieldSize,3))
	for i in range(fieldSize):
		for j in range(fieldSize):
			plotInfo[i][j] = [0,0,0] #[state, health, SugarAmount]
		#
	#

	#===========================================================================
	# Initialization of the sugar
	#===========================================================================
	spawn = 0
	gridInfo[5][5][2] = maxFoodAmount
	plotInfo[5][5][2] = maxFoodAmount
	gridInfo[35][5][2] = maxFoodAmount
	plotInfo[35][5][2] = maxFoodAmount

	for it in range(nIterations):
		if(it%200 == 199):
			xPos = np.random.random_integers(0,fieldSize-1)
			yPos = np.random.random_integers(0,fieldSize-1)
			while gridInfo[xPos][yPos][2] == -1:
				xPos = np.random.random_integers(0,fieldSize-1)
				yPos = np.random.random_integers(0,fieldSize-1)
			gridInfo[xPos][yPos][2] = maxFoodAmount
			plotInfo[xPos][yPos][2] = maxFoodAmount

		#spawn new ant from nest
		#if spawn:
		if(it%2 == 0 and spawn == 0):
			xPos = nestPosition
			yPos = nestPosition
			Agents.append(AntAgent(xPos, yPos, lifeTime))
			nbrHuman += 1
		#

		if(spawn > 0):
			spawn -= 1
		#
		
		#moves all agents once		
		i = 0
		while i < nbrHuman:
			[pos,oldPos,health] = Agents[i].Move(gridInfo)
			plotInfo[oldPos[0]][oldPos[1]][1] = 0 #reset state
			plotInfo[oldPos[0]][oldPos[1]][1] = 0 #reset HP
			if health < 0: #the ant die
				del Agents[i]
				nbrHuman -= 1
			else:
				if gridInfo[pos[0]][pos[1]][2] > 0  and Agents[i].GetState() == FOOD : 
					#to recognise sugar
					Agents[i].ChangeState(HOME)
					plotInfo[pos[0]][pos[1]][2] -= 1
					gridInfo[pos[0]][pos[1]][2] -= 1
				# if
				if gridInfo[pos[0]][pos[1]][2] == -1 and Agents[i].GetState() == HOME : 
					#to recognise nest
					#print(Agents[i].GetHealth(),'Health Left')
					Agents[i].ChangeState(FOOD)
					spawn += 1
					collectedSugar += 1
				# if
			# else
			i += 1
		# while

		for i in range(nbrHuman):
			[x,y] = Agents[i].GetPos()
			plotInfo[x][y][0] = Agents[i].GetState()
			plotInfo[x][y][1] = Agents[i].GetHealth()
		# for

		diffGrid = np.zeros((fieldSize,fieldSize,3))

		for i in range(fieldSize):
			for j in range(fieldSize):
				diffGrid[i][j][0] -= gridInfo[i][j][0]*foodDiff*4
				diffGrid[i][j][1] -= gridInfo[i][j][1]*homeDiff*4

				diffGrid[(i+1)%fieldSize][(j)%fieldSize][0] += gridInfo[i][j][0]*foodDiff
				diffGrid[(i+1)%fieldSize][(j)%fieldSize][1] += gridInfo[i][j][1]*homeDiff

				diffGrid[(i)%fieldSize][(j-1)%fieldSize][0] += gridInfo[i][j][0]*foodDiff
				diffGrid[(i)%fieldSize][(j-1)%fieldSize][1] += gridInfo[i][j][1]*homeDiff

				diffGrid[(i-1)%fieldSize][(j)%fieldSize][0] += gridInfo[i][j][0]*foodDiff
				diffGrid[(i-1)%fieldSize][(j)%fieldSize][1] += gridInfo[i][j][1]*homeDiff

				diffGrid[(i)%fieldSize][(j+1)%fieldSize][0] += gridInfo[i][j][0]*foodDiff
				diffGrid[(i)%fieldSize][(j+1)%fieldSize][1] += gridInfo[i][j][1]*homeDiff

				gridInfo[i][j][0] -= gridInfo[i][j][0]*0.05
				if gridInfo[i][j][0] < 0.1:
					gridInfo[i][j][0] = 0
					diffGrid[i][j][0] = 0
				gridInfo[i][j][1] -= gridInfo[i][j][1]*0.001
			# for
		# for

		gridInfo = gridInfo + diffGrid
		plotW8 = 1 # how often to plot, e.i once every "plotW8" iterations
		if it%plotW8 == 0:
			print(collectedSugar/(it+1),'FoodCollected average')
			print(collectedSugar,'total sugar')
			print(it,'iterations')
			print(nbrHuman,'number of ants')
			npaFood = np.append(npaFood, collectedSugar)#
			npaIterations = np.append(npaIterations, it)
	
			Environment.AntGridPlot(np.copy(plotInfo), fieldSize, plotDelay, 
										antPlotHome, antsPlotFood, sugarPlot, nestPlot,
										antsSubPlot, antsFigure, nestPosition)		
			#Save Figures	
			#antsFigure.savefig('PLots/' + 'AntGrid_' + str(it) + '.png')
			#antsFigure.savefig('Plots/' + 'AntGrid_' + str(it) + '.eps')

			Environment.PheromoneGridPlot(pheromoneFigure, subPlot1_Home, subPlot2_Food,
										np.copy(gridInfo), fieldSize, plotDelay,  
										pheroHomePlot, pheroFoodPlot)
			#Save Figures
			#pheromoneFigure.savefig('Plots/' + 'PheromoneGrid_' + str(it) + '.png')
			#pheromoneFigure.savefig('PLots/' + 'PheromoneGrid_' + str(it) + '.eps')	#
		# if
	# for

if __name__ == '__main__':
	main()
