from panda3d.core import Vec3, TransparencyAttrib
from panda3d.bullet import (
	BulletWorld,
	BulletDebugNode,
	BulletPlaneShape,
	BulletBoxShape,
	BulletRigidBodyNode,
	BulletGhostNode,
	BulletTriangleMesh,
	BulletTriangleMeshShape,
	BulletHelper
)

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from direct.task import Task

from src.log import log, warn
from src.client.entity import Entity
from src.client.loader import getAsset
from src.client.settingsreader import getSetting

from characterController.PlayerController import PlayerController

MOVEMENT_SPEED = 5 #m/s

class Player():
	def __init__(self, instance, model="player", name = "default"):
		log(f"Entity [{name}] initialized.")

		self.instance = instance
		self.name = name
		self.model = model

		self.entity = None
		'''instance.workspace.world.attachRigidBody(self.entity.node)'''

		self.keymaps = {
			"forward": False,
			"backward": False,
			"left": False,
			"right": False
		}

		#self.entity.set_texture("character_default_skin")

	def init(self):
		self.vignette()
		self.instance.spawnNewTask(
			"player_update", self.update
		)

		#self.controller = PlayerController(self.instance.workspace.world, 'assets/character.json')

	def giveEntity(self):
		self.entity = Entity(self.name, self.instance, self.model, [0, 0, 0], True)

	def vignette(self):
		if not getSetting("video", "vignette"): return
		instance = self.instance

		self.vignetteOverlay = instance.loader.loadModel(
			getAsset("models", "map")
		)

		self.vignetteOverlay.set_transparency(TransparencyAttrib.M_dual)
		self.vignetteOverlay.set_alpha_scale(0)

		self.vignetteOverlay_node = self.vignetteOverlay.reparentTo(instance.render)

		self.vignetteOverlay.set_shader_input("resolution", 
			(instance.win.getXSize(), instance.win.getYSize())
		)

		self.vignetteOverlay.setShader(self.instance.workspace.objects["shaders"][0]["shader"])

		instance.spawnNewTask("followCamera_vignette", self.followCamera_vignette)
		instance.accept("aspectRatioChanged", self.arc)

	async def followCamera_vignette(self, task):
		if self.instance.state != self.instance.states_enum.INGAME:
			warn("Vignette disabled.")
			return Task.done

		cam_pos = self.instance.cam.getPos(self.instance.render)
		x, y, z = cam_pos
		y += 10

		self.vignetteOverlay.setPos((x, y, z))
		self.vignetteOverlay.setHpr(self.instance.cam.getHpr())

		return Task.cont

	def arc(self):
		self.vignetteOverlay.set_shader_input("resolution", (self.instance.win.getXSize(), self.instance.win.getYSize()))

	async def update(self, task):
		if self.entity is not None:
			if self.instance.state != self.instance.states_enum.INGAME:
				return Task.done

			if self.instance.state != self.instance.states_enum.INGAME: return
			movement_factor = MOVEMENT_SPEED * self.instance.clock.dt
			pos = self.entity.getPos()

			if self.keymaps["forward"]:
				self.entity.setPos(
					[
						pos[0] + movement_factor,
						pos[1],
						pos[2]
					]
				)
			elif self.keymaps["backward"]:
				self.entity.setPos(
					[
						pos[0] - movement_factor,
						pos[1],
						pos[2]
					]
				)
			elif self.keymaps["left"]:
				self.entity.setPos(
					[
						pos[0],
						pos[1],
						pos[2] + movement_factor
					]
				)
			elif self.keymaps["right"]:
				self.entity.setPos(
					[
						pos[0],
						pos[1],
						pos[2] - movement_factor
					]
				)

		return Task.cont

	def forward(self):
		self.keymaps["forward"] = True

	def forward_stop(self):
		self.keymaps["forward"] = False

	def left(self):
		self.keymaps["left"] = True

	def left_stop(self):
		self.keymaps["left"] = False

	def right(self):
		self.keymaps["right"] = True

	def right_stop(self):
		self.keymaps["right"] = False

	def backward(self):
		self.keymaps["backward"] = True

	def backward_stop(self):
		self.keymaps["backward"] = False