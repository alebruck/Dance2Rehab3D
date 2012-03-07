# world.py

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

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.interval.IntervalGlobal import *
import sys

from pandac.PandaModules import *
#for directx object support
from direct.showbase.DirectObject import DirectObject
#for tasks
from direct.task import Task
#for Actors
from direct.actor.Actor import Actor
#for Pandai
from panda3d.ai import *

import random
import socket
from pandac.PandaModules import TransparencyAttrib 

import sys, random
import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

from direct.filter.CommonFilters import CommonFilters

loadPrcFileData("", "prefer-parasite-buffer #f")

class World():

	def __init__(self, world):
		print "world started"
		self.world = world
		self.createGround()
		self.createWalls()
		#self.createWorm()
		self.criaObjetoGuia()
		self.startFog()
		self.createFish()
		self.setAI()
		#taskMgr.add(self.traverseTask, "tsk_traverse")
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		server_socket.bind(("", 5000))
		self.sock = server_socket
		taskMgr.add(self.moveGuia, "tsk_moveGui")

		self.light = render.attachNewNode(Spotlight("Spot"))
		self.light.node().setScene(render)
		self.light.setPos(0, 150, 300)
		self.light.setP(-45)
		self.light.node().showFrustum()
		self.light.node().getLens().setFov(40)
		self.light.node().getLens().setNearFar(10,100)
		render.setLight(self.light)

		self.alight = render.attachNewNode(AmbientLight("Ambient"))
		self.alight.node().setColor(Vec4(0.4, 0.4, 0.4, 1))
		render.setLight(self.alight)

		# Important! Enable the shader generator.
		render.setShaderAuto()

		# default values
		self.cameraSelection = 0
		self.lightSelection = 0


	def createGround(self):
		cm = CardMaker("ground")
		cm.setFrame(0, 1000, 0, 1000)
		ground = render.attachNewNode(cm.generate())
		ground.setP(270)
		ground.setPos(-500,300,0)
		tex = loader.loadTexture("misc/images/solo.jpg")
		ground.setTexture(tex)

	def createWalls(self):

		tex = loader.loadTexture("misc/images/water.png")

		glass1 = CardMaker("plane1")
		glass1.setFrame(0, 1000, 0, 1000)
		glass1 = render.attachNewNode(glass1.generate())
		glass1.setHpr(90,180,0)
		glass1.setTransparency(TransparencyAttrib.MAlpha)
		glass1.setPos(200,300,500)
		glass1.setTexture(tex)

		glass2 = CardMaker("plane2")
		glass2.setFrame(0, 1000, 0, 1000)
		glass2 = render.attachNewNode(glass2.generate())
		glass2.setHpr(270,180,0)
		glass2.setTransparency(TransparencyAttrib.MAlpha)
		glass2.setPos(-200,1300,500)
		glass2.setTexture(tex)

	def startFog(self):
		colour = (0.2,0.6,0.6)
		linfog = Fog("A linear-mode Fog node")
		linfog.setColor(*colour)
		linfog.setLinearRange(500,1000)
		render.attachNewNode(linfog)
		render.setFog(linfog)
		base.setBackgroundColor( colour )


	def criaObjetoGuia(self):	
		self.worm = Actor("misc/models/sphere.egg.pz")
		self.worm.reparentTo(render)
		self.worm.setPos(0,300,100)
		self.worm.setHpr(0,0,0)
		self.worm.setScale(10, 10, 10)

		attrib = ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne) 
		self.worm.node().setAttrib(attrib) 
		self.worm.setBin('fixed', 0)


	def moveGuia(self,task):
		from numpy import interp
		data, address = self.sock.recvfrom(256)
		#print data		
		x1,y1,z1,x2,y2,z2 = data.split(' ')

		p1 = ponto(int(x1),int(y1),int(z1))
		p2 = ponto(int(x2),int(y2),int(z2))
		
		x = int(interp(float(x1),[-700,700],[0,500]))
		y = int(interp(float(y1),[-700,700],[-300,300]))
		if interp(float(z1)) > 1300 :
			z = 700
		else:
			z = 300
		self.worm.setPos(x,z,y)
		print x,y,z

		return task.cont

	def createFish(self):
		self.fish = Actor("misc/models/clownfish",{"ani1":"misc/models/clownfish_swim"})
		self.fish .reparentTo(render)
		self.fish.setPos(0,350,100)		
		self.fish.setHpr(-90,0,0)
		self.fish.setScale(2, 2, 2) 
		self.fish.setShaderInput("texDisable",1,1,1,1)
		cs = CollisionSphere(0, 0, 0, 10)
		cnodePath = self.fish.attachNewNode(CollisionNode('cnode1'))
		cnodePath.node().addSolid(cs)
		#cnodePath.show()
		#base.cTrav.addCollider(cnodePath, self.collisionHandler)
		return self.fish

	def setAI(self):
		
		self.AIworld = AIWorld(render)
		
		self.AIchar1 = AICharacter("fish",self.fish, 100, 0.5, 5)
		self.AIworld.addAiChar(self.AIchar1)

		self.AIchar2 = AICharacter("worm",self.worm, 100, 0.5, 5)
		self.AIworld.addAiChar(self.AIchar2)

		self.AIbehaviors = self.AIchar1.getAiBehaviors()
		self.AIbehaviors.pursue(self.worm, 10)

		self.fish.loop("ani1")
		#AI World update        
		taskMgr.add(self.AIUpdate,"AIUpdate")

	#to update the AIWorld    
	def AIUpdate(self,task):
		self.AIworld.update()            
		return Task.cont

	def traverseTask(self,task=None):
		self.collisionHandler.sortEntries()
	  	for i in range(self.collisionHandler.getNumEntries()):
			try:
				print "ok"
			except ValueError:
				pass
		return task.cont

	def createTarget(self,modelo):
		import random
		star= Actor(modelo)
		star.reparentTo(render)

		if(self.side):
			'''
				Lado Esquerdo
			'''
			if(self.nivelEsquerdo == 1):
				star.setPos(random.randint(-200,200),100,random.randint(0,350))
			elif(self.nivelEsquerdo == 2):
				star.setPos(random.randint(-200,200),-(random.randint(200,700)),random.randint(60,350))
			else:
				star.setPos(random.randint(-200,200),-(random.randint(200,700)),random.randint(60,350))
		else:
			'''
				Lado Direito
			'''
			if(self.nivelEsquerdo == 1):
				star.setPos(random.randint(-200,200),-(random.randint(200,700)),random.randint(60,350))
			elif(self.nivelEsquerdo == 2):
				star.setPos(random.randint(-200,200),-(random.randint(200,700)),random.randint(60,350))
			else:
				star.setPos(random.randint(-200,200),-(random.randint(200,700)),random.randint(60,350))
		
		star.setHpr(0,180,0)
		star.setScale(10, 10, 10) 
		i = star.hprInterval(duration=10, hpr=VBase3(720,720, 720))
		i.loop()
		cs = CollisionSphere(0, 0, 0, 1)
		cnodePath = star.attachNewNode(CollisionNode('cnode2'))
		cnodePath.node().addSolid(cs)
		#cnodePath.show()

		cm = CardMaker("x")
		cm.setFrame(-20, 20, -20, 20)
		self.x = render.attachNewNode(cm.generate())
		self.x.setP(270)
		x,z,y = star.getPos()
		self.x.setPos(x,z,1)
		self.x.setTransparency(TransparencyAttrib.MAlpha)
		tex = loader.loadTexture("image/x.png")
		self.x.setTexture(tex)
		taskMgr.add(self.next, "next")
		self.killTime = globalClock.getFrameTime()
		return star


