#!/usr/bin/python3

"""
Author: 	Clint Cooper, Emily Rohrbough, Leah Thompson
Date:   	09/25/15
CSCI 447:	Project 2
"""

# Code for a neural network... Details coming to a theatre near you!!!

import sys
import math
import random
from scipy.special import expit

'''
help_screen = ["Usage   python NN.py <#input> <#hidden_layer> <#_output>"
               " <option> ...","OPTION  DESCRIPTION",
               "-r,-f   test either RBF(-r) or MLP(-f), must choose just one",
               "-i <#>  number of inputs", 
               "-h <#>  number of hidden layers",
               "-o <#>  number of outputs",
               "-g <#>  number of Gaussian basis functions",
               "-m      use momentum, default off", 
               "-s, -l  activation fn, sigmoid or linear"]

if sys.argv[1] in ['-h', '--h', '--help', '-help']:
    print ("\n".join(help_screen))
    sys.exit()
'''

global BiasWeight
BiasWeight = 0
global LearnRate
LearnRate = 0.5

class node:
	def __init__(self, appFunc = '', value = 0):
		self.inputs = []
		self.weights = []
		self.outputs = []
		self.error = 0
		self.func = appFunc
		self.value = value
	def addInputs(self, nodes):
		for x in nodes:
			x.addOutput(self)
			self.inputs.append(x)
			self.weights.append(random.random())
	def calcValue(self):
		summa = 0
		for x in self.inputs:
			summa += x.getValue()*self.weights[self.inputs.index(x)]
		summa += BiasWeight
		if self.func == 'S':
			self.value = expit(summa)
		else:
			self.value = summa
	def getValue(self):
		return self.value
	def addOutput(self, node):
		self.outputs.append(node)
	def getError(self):
		return self.error
	def getWeightForNode(self, node):
		print('Weight from', id(self), 'to', id(node), self.weights[self.inputs.index(node)])
		return self.weights[self.inputs.index(node)]
	def calcHiddenError(self):
		print('Error for', id(self), self.error)
		sigma = 0
		for x in self.outputs:
			sigma += x.getError() * x.getWeightForNode(self)
		self.error = self.value * (1 - self.value) * sigma + BiasWeight

		#Delta Weight is not calculated (no learnrate) at this stage
	def calcOutputError(self, answer):
		self.error = (answer - self.value) * self.value * (1 - self.value) + BiasWeight
	def getError(self):
		return self.error
	def updateOutputWeights(self):
		for x in self.weights:
			x = x + (LearnRate * self.error * self.inputs[self.weights.index(x)].getValue())
	def updateHiddenWeights(self):
		for x in self.weights:
			x = x + (LearnRate * self.error * x)
	def getOutputs(self):
		return self.outputs

def main(inputs, arrangement, outputs, answers, learnrate = 0.5, threshold = 0, bias = 0):
	global StartingNodes
	StartingNodes = []
	global HiddenNodes
	HiddenNodes = []
	global OutputNodes
	OutputNodes = []
	global Threshold
	Threshold = threshold
	global BiasWeight
	BiasWeight = bias
	global AnswerSet
	AnswerSet = answers
	global loops
	loops = 0

	# Make Start Nodes
	for x in inputs:
		n = node(value = x)
		StartingNodes.append(n)
	# Make Hidden Layers
	for y in arrangement:
		temp = []
		for x in y:
			if arrangement.index(y) == 0:
				n = node(appFunc = x)
				n.addInputs(StartingNodes)
				temp.append(n)
			else:
				n = node(appFunc = x)
				n.addInputs(HiddenNodes[arrangement.index(y) - 1])
				temp.append(n)
		HiddenNodes.append(temp)
	# Make Output Layers
	for x in outputs:
		n = node(appFunc = x)
		n.addInputs(HiddenNodes[-1])
		OutputNodes.append(n)
	# Network created

	#for y in HiddenNodes:
	#	for x in y:
	#		print(x, x.getOutputs())

	print('Network Constructed. Calculating result.')

	CalculateNN()
	# Will reach this point when result has been calculated and is within proper threshold results.
	print('\nWeights Found.')
	
	for x in StartingNodes:
		print(id(x), 'has starting value:', x.getValue())
	for y in HiddenNodes:
		for x in y:
			print(id(x), 'has hidden value:', x.getValue())
			print(id(x), 'has hidden error:', x.getError())
	for x in OutputNodes:
		print(id(x), 'has output value:', x.getValue())
		print(id(x), 'has output error:', x.getError())
	

def CalculateNN():
	global StartingNodes
	global HiddenNodes
	global OutputNodes
	global Threshold
	global AnswerSet
	global loops

	backprop = False

	# Forward propagation of solution
	for x in StartingNodes:
		x.getValue()
	for y in HiddenNodes:
		for x in y:
			x.calcValue()
			print('Value of', id(x), x.getValue())
	print(loops)
	for x in OutputNodes:
		x.calcValue()
		x.calcOutputError(AnswerSet[OutputNodes.index(x)])
		if not ((x.getError() <= (AnswerSet[OutputNodes.index(x)] + Threshold)) and (x.getError() >= (AnswerSet[OutputNodes.index(x)] - Threshold))):
			backprop = True
	if (loops < 3):
		loops += 1
		if (backprop == True):
	#		print('BackProping with', x.getError())
			BackPropNN()

def BackPropNN():
	global StartingNodes
	global HiddenNodes
	global OutputNodes
	global LearnRate

	for x in OutputNodes:
		x.updateOutputWeights()
	for y in reversed(HiddenNodes):
		for x in y:
			x.calcHiddenError()
			x.updateHiddenWeights()
	CalculateNN()



# This is a testing set. Build looks like:
	#
	#   2 - A 
	#     X   > C - OUT
	#   3 - B
	#
if __name__== '__main__': main([2,3], [['S', 'S']], ['L'], [101], threshold = 10)




