from panda3d.core import Vec3, TransparencyAttrib
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from direct.task import Task

from src.client.log import *
from src.client.entity import Entity
from src.client.loader import getAsset
from src.client.settingsreader import getSetting

class Player():
	def __init__(self, instance, model="player", name = "default"):
		log(f"Entity [{name}] initialized.")

		self.inputManager = instance.inputManager
		self.instance = instance

		self.entity = Entity(name, instance, model)

		self.entity.set_texture("character_default_skin")

	def init(self):
		self.vignette()

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

		pitch = self.instance.cam.getP(self.instance.render)
		heading = self.instance.cam.getH(self.instance.render)

		self.vignetteOverlay.setPos((x, y, z))
		self.vignetteOverlay.setHpr(pitch, heading, 0)

		return Task.cont

	def arc(self):
		self.vignetteOverlay.set_shader_input("resolution", (self.instance.win.getXSize(), self.instance.win.getYSize()))

	async def update(self, task):
		if self.instance.state != self.instance.states_enum.INGAME:
			return Task.done

		#TODO: [WIP]Add player movement logic here, [DONE]possibly through InputManager polling.		

		return Task.cont