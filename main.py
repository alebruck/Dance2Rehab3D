# Author: Alessandro Diogo Bruckheimer
# alebruck at gmail dot com
# main.py

import direct.directbase.DirectStart
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32,Point3,VBase4
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math

from direct.interval.IntervalGlobal import *




from pandac.PandaModules import ColorBlendAttrib

import direct.directbase.DirectStart 
from direct.gui.DirectGui import * 
from direct.task import Task 

import world
import sys
import direct.directbase.DirectStart 
from direct.showbase.Transitions import Transitions 

import time

class Main(DirectObject):
	side = True
	worm = None
	sd = ['Direita','Esquerda']
	pontosEsquerdo = 0
	pontosDireito = 0
	def __init__(self):
		print sys.argv
		self.side = int(sys.argv[1])
		base.camLens.setFov(60)
		base.disableMouse()
		print "game init"
		# start Game
		self.config()
		taskMgr.add(self.timerTask, 'timerTask')
		self.setCamera()
		self.world = world.World(self)
		self.showside['text'] = self.sd[self.side]

	def exit(self):
		time.sleep(10)
		sys.exit()
		
	# define some game configuration
	def config(self):
		# scape to exit
		self.accept("escape",self.exit)
		# define game clock label
		self.mytimer = DirectLabel(scale=.07,pos=(0,0,0.9))
		self.scoreLeft = DirectLabel(scale=.07,pos=(0.95,0,0.9))
		self.scoreRight = DirectLabel(scale=.07,pos=(-0.95,0,0.9))
		self.showside = DirectLabel(scale=.07,pos=(0,0,0.8))

		self.scoreLeft['text'] = str(self.pontosEsquerdo)
		self.scoreRight['text'] = str(self.pontosDireito)

		# every 30 seconds
		taskMgr.doMethodLater(30, self.changeSide, 'changeSide')
		

	# control the time in game
	def timerTask(self,task): 
		self.secondsTime = int(task.time) 
	  	self.minutesTime = int(self.secondsTime/60)
	  	self.mytimer['text'] = "%02d:%02d" % (self.minutesTime%60, self.secondsTime%60)
	  	return Task.cont

	# change current game side
	def changeSide(self, task):
		self.displayText("TROCA O LADO")
		self.side = not self.side
		if self.world.ladoAlvoAtual != self.side:
			self.world.target.remove()
			self.world.x.remove()
			self.world.createTarget()
		print "LADO"
		print self.side
		print self.sd[self.side]
		self.showside['text'] = self.sd[self.side]
		return task.again

	# define camera position
	def setCamera(self):
		base.cam.setHpr(0,-15,0)
		base.cam.setPos(0, 0, 200)

	def displayText(self,text):
		newTextNode = TextNode('text')
		newTextNode.setText(text)
		newTextNode.setAlign(TextNode.ACenter)
		newTextNode.setWordwrap(16.0)
		text_generate = newTextNode.generate()
		newTextNodePath = render.attachNewNode(text_generate)
		newTextNodePath.setPos(0,1000,190)
		newTextNodePath.setScale(30,30,30)
		self.textEffects(newTextNodePath)
		return newTextNodePath

	def textEffects(self,textNodePath):
		x = random.randint(-5,5)
		y = random.randint(10,40)
		z = random.randint(-5,5)
		tnpPosInterval = LerpPosInterval(textNodePath, 6, Point3(x,y,z))

		r = random.choice([0,128,255])
		g = random.choice([0,128,255])
		b = random.choice([0,128,255])
		a = random.choice([0,128,255])
		tnpColorInterval = LerpColorInterval(textNodePath, 6, VBase4(r,g,b,a))

		tnpScaleInterval = LerpScaleInterval(textNodePath, 6, 1+random.random()) 

		current_rotation = textNodePath.getHpr()[2]
		rotation=current_rotation + random.randint(60,120)
		tnpHprInterval = LerpHprInterval(textNodePath, 6, Vec3(0,0,rotation))

		textSequence = Sequence(Parallel(tnpPosInterval,tnpColorInterval,tnpScaleInterval,tnpHprInterval),Func(self.textEffects, textNodePath))
		textSequence.start()
		





 

w = Main()
run()
		
