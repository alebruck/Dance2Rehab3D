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

import direct.directbase.DirectStart 
from direct.gui.DirectGui import * 
from direct.task import Task 

#import world, characters

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1),
                        pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1,1,1,1),
                        pos=(1.3,-0.95), align=TextNode.ARight, scale = .07)


class Main(DirectObject):

	def __init__(self):
		print "game init"

		# Start With de Game
		#self.config()
		#taskMgr.add(self.timerTask, 'timerTask')

	# define some game configuration
	def config(self):
		# scape to exit
		self.accept("escape",sys.exit)
		# define game clock label
		self.mytimer = DirectLabel(scale=.05,pos=(0,0,0))
		# 60 seconds
		taskMgr.doMethodLater(60, chageSide, 'Change Side')
		# 120 seconds
		taskMgr.doMethodLater(120, changeSide, 'ChangeSide')

	# control the time in game
	def timerTask(self,task): 
		self.secondsTime = int(task.time) 
	  	self.minutesTime = int(self.secondsTime/60)
	  	self.mytimer['text'] = "%02d:%02d" % (self.minutesTime%60, self.secondsTime%60)
	  	return Task.cont

	def changeSide(self, task):
		side = not side





 

w = Main()
run()
		