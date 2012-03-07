# Author: Alessandro Diogo Bruckheimer
# alebruck at gmail dot com
# main.py

import direct.directbase.DirectStart
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math


from pandac.PandaModules import ColorBlendAttrib

import direct.directbase.DirectStart 
from direct.gui.DirectGui import * 
from direct.task import Task 

import world
#, characters

class Main(DirectObject):
	side = True
	worm = None
	def __init__(self):
		print "game init"
		# start Game
		self.config()
		taskMgr.add(self.timerTask, 'timerTask')
		self.setCamera()
		a = world.World(self)

	# define some game configuration
	def config(self):
		# scape to exit
		self.accept("escape",sys.exit)
		# define game clock label
		self.mytimer = DirectLabel(scale=.05,pos=(-0.95,0,0.9))
		self.score = DirectLabel(scale=.05,pos=(0.95,0,0.9))

		

		self.score['text'] = str(0)

		# 30 seconds
		taskMgr.doMethodLater(30, self.changeSide, 'changeSide')
		# 60 seconds
		taskMgr.doMethodLater(60, self.changeSide, 'changeSide')
		# 90 seconds
		taskMgr.doMethodLater(90, self.changeSide, 'changeSide')
		# 120 seconds
		taskMgr.doMethodLater(120, self.changeSide, 'changeSide')

	# control the time in game
	def timerTask(self,task): 
		self.secondsTime = int(task.time) 
	  	self.minutesTime = int(self.secondsTime/60)
	  	self.mytimer['text'] = "%02d:%02d" % (self.minutesTime%60, self.secondsTime%60)
	  	return Task.cont

	# change current game side
	def changeSide(self, task):
		self.side = not self.side

	# define camera position
	def setCamera(self):
		base.cam.setHpr(0,-15,0)
		base.cam.setPos(0, 0, 200)
		





 

w = Main()
run()
		