# characters.py

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

class Character():

	def __init__(self):
		print "character started"

	# create the main character, the Fish
	def createFish(self):
		print "fish created"

	# create the bubble, which position is defined by the player's hand position
	def createBubble(self):
		print "bubble created"

	# create the target object
	def createRandomObject(self):
		print "random object created"



self.fish = Actor("model/clownfish",{"swim":"model/clownfish_swim"})
		self.fish .reparentTo(render)
		self.fish.setPos(0,-900,200)
		self.fish.loop("swim")		
		self.fish.setHpr(-90,0,0)
		self.fish.setScale(2, 2, 2) 
		cs = CollisionSphere(0, 0, 0, 10)
		cnodePath = self.fish.attachNewNode(CollisionNode('cnode1'))
		cnodePath.node().addSolid(cs)
		#cnodePath.show()
		base.cTrav.addCollider(cnodePath, self.collisionHandler)

		cm = CardMaker("sombraFish")
		cm.setFrame(-20, 20, -20, 20)
		self.sombraFish = render.attachNewNode(cm.generate())
		self.sombraFish.setP(270)
		self.sombraFish.setPos(0,0,1)
		self.sombraFish.setTransparency(TransparencyAttrib.MAlpha)
		tex = loader.loadTexture("image/sombra.png")
		self.sombraFish.setTexture(tex)
		return self.fish