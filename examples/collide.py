import pyglet
from pyglet.window import key#, MouseCursor
from pyglet.window import mouse
import ratcave as rc
import numpy as np

# Create Window
window = pyglet.window.Window(800, 600)
keys = key.KeyStateHandler()
window.push_handlers(keys)
window.set_mouse_visible(True)

def update(dt):
    pass
pyglet.clock.schedule(update)

# Insert filename into WavefrontReader.
obj_filename = rc.resources.obj_primitives
obj_reader = rc.WavefrontReader(obj_filename)

z_glob = -10

# Create Meshes
monkey = obj_reader.get_mesh("Monkey", scale=2, position=(0, 0, z_glob))
# center_x = ((monkey.vertices[:, :1]).max() + (monkey.vertices[:, :1]).min())/2
# center_y = ((monkey.vertices[:, :2]).max() + (monkey.vertices[:, :2]).min())/2
# center_z = ((monkey.vertices[:, :3]).max() + (monkey.vertices[:, :3]).min())/2


# scale = np.linalg.norm(monkey.vertices[:, :3], axis=1).max()
# sphere = obj_reader.get_mesh("Sphere",  scale=scale)
# sphere.draw_mode = sphere.points
# sphere.position.xyz = (center_x, center_y, center_z)
# monkey.add_child(sphere, modify=False)

# Create Collision Sphere
col_sphere = rc.SphereCollisionChecker(mesh=monkey, visible=True)

# Create Scene
scene = rc.Scene(meshes=monkey, bgColor=(0,0,0))
scene.camera.projection.z_far = 20

def move_camera(dt):
    speed = 3
    if keys[key.LEFT]:
        monkey.position.y -= speed * dt
    if keys[key.RIGHT]:
        monkey.position.y += speed * dt
pyglet.clock.schedule(move_camera)

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        # adjust coordinates
        x = (x-400)/100
        y = (y-300)/100
        collide = col_sphere.collides_with(xyz=(x,y,z_glob))

        if collide:
            # change color on collision
            monkey.uniforms['diffuse'][0] = np.random.randint(1, high = 5)
            monkey.uniforms['diffuse'][1] = np.random.randint(1, high = 5)
        print('The left mouse button was pressed.', collide)

@window.event
def on_draw():
    monkey.rotation.y += 0.5
    with rc.default_shader:
        scene.draw()

pyglet.app.run()
