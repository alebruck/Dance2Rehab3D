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
	world = None
	collisionHandler = CollisionHandlerQueue()
	nivelEsquerdo = 1
	nivelDireito = 1
	ladoAlvoAtual = None
	def __init__(self, world):
		print "world started"
		base.cTrav=CollisionTraverser()
		taskMgr.add(self.traverseTask, "tsk_traverse")
		self.world = world
		self.createGround()
		self.createWalls()
		self.criaObjetoGuia()
		self.startFog()
		self.createFish()
		self.createTarget()
		#self.createPlants()
		self.sounds()
		self.setAI()
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
		server_socket.bind(("", 5000))
		self.sock = server_socket
		self.world.pontosEsquerdo = 0
		self.world.pontosDireito = 0
		taskMgr.add(self.moveReference, "tsk_moveGui")

		self.light = render.attachNewNode(Spotlight("Spot"))
		self.light.node().setScene(render)
		self.light.setPos(0, 100, 450)
		self.light.setP(-40)
		self.light.node().showFrustum()
		self.light.node().getLens().setFov(75)
		self.light.node().getLens().setNearFar(10,100)
		render.setLight(self.light)

		self.alight = render.attachNewNode(AmbientLight("Ambient"))
		self.alight.node().setColor(Vec4(0.5, 0.5, 0.5, 1))
		render.setLight(self.alight)

		# Important! Enable the shader generator.
		render.setShaderAuto()

		# default values
		self.cameraSelection = 0
		self.lightSelection = 0

	def sounds(self):
		self.bgSound = loader.loadSfx('misc/sounds/sound.ogg')
		self.sound = loader.loadSfx("misc/sounds/done.ogg")
		self.bgSound.setLoop(True)
		self.bgSound.setVolume(0.5)	
		self.bgSound.setLoopCount(0)
		self.bgSound.play()


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
		glass1.setPos(300,300,500)
		glass1.setTexture(tex)

		glass2 = CardMaker("plane2")
		glass2.setFrame(0, 1000, 0, 1000)
		glass2 = render.attachNewNode(glass2.generate())
		glass2.setHpr(270,180,0)
		glass2.setTransparency(TransparencyAttrib.MAlpha)
		glass2.setPos(-300,1300,500)
		glass2.setTexture(tex)
	
	def createPlants(self):
		self.loadModel("misc/models/plant2.egg",(-100,830,0),(-45,0,40),(35, 35, 35),(0,1,0))
		self.loadModel("misc/models/plant2.egg",(200,850,0),(-45,0,0),(35, 35, 35),(0,1,0))
		self.loadModel("misc/models/plant1.egg",(100,870,0),(-45,0,0),(35, 35, 35),(3,-10,0))
		self.loadModel("misc/models/plant1.egg",(-100,950,0),(0,0,0),(35, 35, 35),(3,-10,0))
		self.loadModel("misc/models/plant1.egg",(-50,870,0),(0,0,0),(35, 35, 35),(3,-10,0))
		self.loadModel("misc/models/rock10-32",(-150,750,0),(0,-10,10),(5, 5, 5),(3,-10,0))
		self.loadModel("misc/models/rock10-32",(-110,700,0),(0,-10,10),(5, 5, 5),(3,-10,0))
		self.loadModel("misc/models/rock10-32",(-170,760,0),(0,-10,10),(10, 10, 10),(3,-10,0))
		self.loadModel("misc/models/rock10-32",(-50,770,0),(0,-10,10),(5, 5, 5),(3,-10,0))
		self.loadModel("misc/models/rock10-32",(-190,670,0),(0,-10,10),(5, 5, 5),(3,-10,0))
		self.loadModel("misc/models/rock10-32",(280,570,0),(0,-10,10),(2, 2, 2),(3,-10,0))
		self.loadModel("misc/models/rock10-32",(270,590,0),(0,-10,10),(2, 2, 2),(3,-10,0))
		self.loadModel("misc/models/rock10-32",(-270,500,0),(0,-10,10),(2, 2, 2),(3,-10,0))
		self.loadModel("misc/models/rock10-32",(-270,490,0),(0,-10,10),(1, 1, 1),(3,-10,0))
		self.loadModel("misc/models/rock10-32",(160,790,0),(0,-10,0),(15, 15, 15),(3,-10,0))
		self.loadModel("misc/models/rock10-32",(0,840,0),(0,-10,0),(25, 25, 25),(3,-10,0))
	
	def loadModel(self,model,pos,ang,scale,color):
		var = loader.loadModel(model)
		var.reparentTo(render)
		var.setPos(pos[0],pos[1],pos[2])
		var.setHpr(ang[0],ang[1],ang[2])
		var.setScale(scale[0],scale[1],scale[2])
		var.setColor(color[0],color[1],color[2])

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
		cm = CardMaker("sombraWorm")
		cm.setFrame(-20, 20, -20, 20)
		self.sombraWorm = render.attachNewNode(cm.generate())
		self.sombraWorm.setP(270)
		self.sombraWorm.setPos(0,0,1)
		self.sombraWorm.setTransparency(TransparencyAttrib.MAlpha)
		tex = loader.loadTexture("misc/images/sombra.png")
		self.sombraWorm.setTexture(tex)
		taskMgr.add(self.vaiSombra, "tsk_traverse")


	'''
	#self.worm = Actor("misc/models/sphere.egg.pz")
			self.worm = Actor("misc/models/hand.egg")
			self.worm.reparentTo(render)
			self.worm.setPos(0,300,100)
			self.worm.setHpr(250,-10,0)
			self.worm.setScale(15, 15, 15)

			attrib = ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne) 
			#self.worm.node().setAttrib(attrib) 
			self.worm.setBin('fixed', 0)
			cm = CardMaker("sombraWorm")
			cm.setFrame(-20, 20, -20, 20)
			self.sombraWorm = render.attachNewNode(cm.generate())
			self.sombraWorm.setP(270)
			self.sombraWorm.setPos(0,0,1)
			self.sombraWorm.setTransparency(TransparencyAttrib.MAlpha)
			tex = loader.loadTexture("misc/images/sombra.png")
			self.sombraWorm.setTexture(tex)
			taskMgr.add(self.vaiSombra, "tsk_traverse")
	'''

	def moveReference(self,task):
		from numpy import interp
		data, address = self.sock.recvfrom(256)
		#print data		
		x1,y1,z1,x2,y2,z2 = data.split(' ')

		if self.world.side:
			x,y,z = x1,y1,z1
		else:
			x,y,z = x2,y2,z2
		
		x = int(interp(float(x),[-800,800],[-250,250]))
		y = int(interp(float(y),[-400,600],[10,180]))
		z = int(interp(float(z),[1200,1400],[650,300]))		

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
		cs = CollisionSphere(0, 0, 0, 5)
		cnodePath = self.fish.attachNewNode(CollisionNode('cnode1'))
		cnodePath.node().addSolid(cs)
		#cnodePath.show()

		cm = CardMaker("sombraFish")
		cm.setFrame(-20, 10, -20, 10)
		self.sombraFish = render.attachNewNode(cm.generate())
		self.sombraFish.setP(270)
		self.sombraFish.setPos(0,0,1)
		self.sombraFish.setTransparency(TransparencyAttrib.MAlpha)
		tex = loader.loadTexture("misc/images/sombra.png")
		self.sombraFish.setTexture(tex)

		base.cTrav.addCollider(cnodePath, self.collisionHandler)
		return self.fish

	def vaiSombra(self,task=None):
		x,z,y = self.fish.getPos()
		self.sombraFish.setPos(x,z,1)
		x,z,y = self.worm.getPos()
		self.sombraWorm.setPos(x,z,1)
		return task.cont

	def setAI(self):
		
		self.AIworld = AIWorld(render)
		
		self.AIchar1 = AICharacter("fish",self.fish, 10, 10, 20)
		self.AIworld.addAiChar(self.AIchar1)

		self.AIchar2 = AICharacter("worm",self.worm, 10, 10, 20)
		self.AIworld.addAiChar(self.AIchar2)

		self.AIbehaviors = self.AIchar1.getAiBehaviors()
		self.AIbehaviors.pursue(self.worm, 10)

		self.AIchar1.setMaxForce(38)

		self.fish.loop("ani1")
		#AI World update        
		taskMgr.add(self.AIUpdate,"AIUpdate")

	#to update the AIWorld    
	def AIUpdate(self,task):
		self.AIworld.update()            
		return Task.cont

	def traverseTask(self,task):
		self.collisionHandler.sortEntries()
	  	for i in range(self.collisionHandler.getNumEntries()):
			#print "ENTROU"
			try:
				if self.world.side:
					print "LADO1"
					print self.world.pontosEsquerdo
					self.world.pontosEsquerdo = self.world.pontosEsquerdo + 1
				else:
					print "LADO2"
					self.world.pontosDireito
					self.world.pontosDireito = self.world.pontosDireito + 1
				self.sound.play()
				self.target.remove()
				self.x.remove()
				self.createTarget()
				print "ok"
			except ValueError:
				pass

		self.world.scoreRight['text'] = str(self.world.pontosEsquerdo)
		self.world.scoreLeft['text'] = str(self.world.pontosDireito)
		return task.cont

	def createTarget(self,modelo="misc/models/star"):
		import random
		self.target= Actor(modelo)
		self.target.reparentTo(render)
		self.ladoAlvoAtual = self.world.side
		print	"self.world.side"
		print self.world.side
		if not self.world.side:
			'''
				Lado Esquerdo
			'''
			if(self.nivelEsquerdo == 1):
				self.target.setPos(random.randint(0,200),random.choice([450,640]),random.randint(120,170))
			elif(self.nivelEsquerdo == 2):
				self.target.setPos(random.randint(-200,200),random.choice([450,640]),random.randint(60,350))
			else:
				self.target.setPos(random.randint(-200,200),random.choice([450,640]),random.randint(60,350))
		else:
			'''
				Lado Direito
			'''
			if(self.nivelEsquerdo == 1):
				self.target.setPos(random.randint(-200,0),random.choice([450,640]),random.randint(120,170))
			elif(self.nivelEsquerdo == 2):
				self.target.setPos(-random.randint(0,200),random.choice([450,640]),random.randint(60,350))
			else:
				self.target.setPos(-random.randint(0,200),random.choice([450,640]),random.randint(60,350))
		print "POSITION"		
		print self.target.getPos()
		self.target.setHpr(0,180,0)
		self.target.setScale(10, 10, 10) 
		i = self.target.hprInterval(duration=10, hpr=VBase3(720,720, 720))
		i.loop()

		cs = CollisionSphere(0, 0, 0, 4)
		cnodePath = self.target.attachNewNode(CollisionNode('cnode2'))
		cnodePath.node().addSolid(cs)
		#cnodePath.show()

		cm = CardMaker("x")
		cm.setFrame(-20, 20, -20, 20)
		self.x = render.attachNewNode(cm.generate())
		self.x.setP(270)
		x,z,y = self.target.getPos()
		self.x.setPos(x,z,1)
		self.x.setTransparency(TransparencyAttrib.MAlpha)
		tex = loader.loadTexture("misc/images/x.png")
		self.x.setTexture(tex)
		return self.target

