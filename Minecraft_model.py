from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
sky_texture   = load_texture('assets/skybox.png')
arm_texture   = load_texture('assets/arm_texture.png')
punch_sound   = Audio('assets/punch_sound',loop = False, autoplay = False)
block_pick = 1
world_voxels = []

window.fps_counter.enabled = False
window.exit_button.visible = False

def update():
	global block_pick

	if game_menu.enabled:
		return

	if held_keys['left mouse'] or held_keys['right mouse']:
		hand.active()
	else:
		hand.passive()

	if held_keys['1']: block_pick = 1
	if held_keys['2']: block_pick = 2
	if held_keys['3']: block_pick = 3
	if held_keys['4']: block_pick = 4

class Voxel(Button):
	def __init__(self, position = (0,0,0), texture = grass_texture):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/block',
			origin_y = 0.5,
			texture = texture,
			color = color.hsv(0, 0, random.uniform(0.9, 1)),
			scale = 0.5)
		world_voxels.append(self)

	def input(self,key):
		if self.hovered:
			if key == 'left mouse down':
				punch_sound.play()
				if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
				if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
				if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
				if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)

			if key == 'right mouse down':
				punch_sound.play()
				world_voxels.remove(self)
				destroy(self)

class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_texture,
			scale = 150,
			double_sided = True)

class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = arm_texture,
			scale = 0.2,
			rotation = Vec3(150,-10,0),
			position = Vec2(0.4,-0.6))

	def active(self):
		self.position = Vec2(0.3,-0.5)

	def passive(self):
		self.position = Vec2(0.4,-0.6)

def create_world():
	for z in range(20):
		for x in range(20):
			Voxel(position = (x,0,z))

def open_game_menu():
	game_menu.enabled = True
	player.enabled = False
	mouse.locked = False

def close_game_menu():
	game_menu.enabled = False
	player.enabled = True
	mouse.locked = True

def restart_game():
	for voxel in world_voxels[:]:
		destroy(voxel)
	world_voxels.clear()
	create_world()
	player.position = (10, 3, 10)
	player.rotation = (0, 0, 0)
	close_game_menu()

def input(key):
	if key == 'escape':
		if game_menu.enabled:
			close_game_menu()
		else:
			open_game_menu()

create_world()
player = FirstPersonController()
sky = Sky()
hand = Hand()

game_menu = Entity(parent=camera.ui, enabled=False)
Entity(parent=game_menu, model='quad', scale=(0.55, 0.65), color=color.black66)
Text(parent=game_menu, text='Paused', y=0.22, origin=(0, 0), scale=1.5)
Button(parent=game_menu, text='Resume', y=0.08, scale=(0.35, 0.08), on_click=close_game_menu)
Button(parent=game_menu, text='Restart', y=-0.04, scale=(0.35, 0.08), on_click=restart_game)
Button(parent=game_menu, text='Quit', y=-0.16, scale=(0.35, 0.08), on_click=application.quit)

app.run()
