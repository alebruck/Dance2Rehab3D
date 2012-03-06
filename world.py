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

class World():

	def __init__(self):
		print "world started"
		self.createGround()
		self.createWalls()
		self.startFog()

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


