from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import sys

GROUND_SIZE = (6000, 6000)
BUILDING_SIZE = (10, 40, 10)
ROAD_SIZE = (GROUND_SIZE[0], 1, 10)
ENEMY_SIZE = (1.5, 2, 1)
BUILDING_POS = (0, 20, 0)
ROAD_POS = (0, 1, 80)
NORMAL_FOV = 90
ZOOMED_IN_FOV = 20

class Enemy(Entity):
	def __init__(self):
		pos = (random.randint(-500, 500), 2.5, ROAD_POS[2] + 2)
		super().__init__(model="cube", color=color.white, scale=ENEMY_SIZE, position=pos, collider="box", rotation_y=90)

	def update(self):
		self.position += self.forward * time.dt * 2

class Game(Ursina):
	def __init__(self):
		super().__init__()
		window.fullscreen = True
		window.exit_button.visible = False
		Entity.default_shader = lit_with_shadows_shader
		self.sun = DirectionalLight()
		self.sun.look_at((1, -1, 1))
		Sky()
		self.ground = Entity(model="quad", scale=GROUND_SIZE, texture="grass", rotation_x=90, collider="box")
		self.building = Entity(model="cube", color=color.white, texture="white_cube", scale=BUILDING_SIZE, position=BUILDING_POS, collider="box")
		self.road = Entity(model="cube", color=color.black, scale=ROAD_SIZE, position=ROAD_POS, collider="box")
		self.yellow_line = Entity(parent=self.road, model="cube", color=color.yellow, scale=(1, 0.1, 0.1), position=(0, 0.5, 0))
		self.player = FirstPersonController(position=(0, 50, 0))
		self.gun = Entity(parent=camera, model="cube", color=color.black, scale=(5, 0.2, 0.2), position=(1, -0.5, 1), rotation_x=90, rotation_z=90)
		self.scope = Entity(parent=self.gun, model="cube", color=color.black, scale=(0.3, 1.5, 1.5), position=(-0.2, 0, -1.5))
		self.stand = Entity(parent=self.gun, model="cube", color=color.black, scale=(0.3, 0.8, 0.8), position=(-0.5, -1, 0))
		self.magazine = Entity(parent=self.gun, model="cube", color=color.black, scale=(0.2, 0.8, 0.8), position=(-0.2, 0, 1))
		self.scope_filter = Entity(parent=camera, model="quad", texture="src/circle at center.png", scale=(1, 0.8, 0.8), position=(0, 0, 1), visible=False)
		self.sniper_sound = Audio("src/sniper sound effect.mp3", autoplay=False)
		self.gun.cooldown_on = False
		self.enemies = [Enemy() for enemy in range(50)]

	def shoot(self):
		if not self.gun.cooldown_on:
			self.gun.cooldown_on = True
			invoke(setattr, self.gun, "cooldown_on", False, delay=1.5)
			self.sniper_sound.play()
			if mouse.hovered_entity:
				if mouse.hovered_entity.name == "enemy":
					mouse.hovered_entity.blink(color.red)
					invoke(destroy, mouse.hovered_entity, delay=0.09)

	def update(self):
		if held_keys["escape"]:
			sys.exit()
		if held_keys["right mouse"]:
			camera.fov = ZOOMED_IN_FOV
			self.scope_filter.visible = True
		else:
			camera.fov = NORMAL_FOV
			self.scope_filter.visible = False
		if held_keys["left mouse"]:
			self.shoot()
			

if __name__ == "__main__":
	game = Game()
	update = game.update
	game.run()