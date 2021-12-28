from panda3d.core import Vec3
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from direct.task import Task

from src.client.log import *
from src.client.entity import Entity

class Player(Entity):
	def __init__(self, instance, model, name = "default"):
		super(Entity, self).__init__(name, instance, model)
		log(f"Entity [{name}] initialized.")

		self.inputManager = instance.inputManager
		self.instance = instance

	async def update(self, task):
		if self.instance.state != self.instance.states_enum.INGAME:
			return Task.done

		#TODO: Add player movement logic here, possibly through InputManager polling.		

		return Task.cont