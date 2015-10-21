# program template for Spaceship
#import simplegui
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    simplegui.Image._dir_search_first = '../tmp/'
    simplegui.Sound._dir_search_first = '../tmp/'

import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False
Angle_Vel_Ship = 0.1
Friction = 0.01
weapon_charging = False
charging_time = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
#debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")
debris_image = simplegui.load_image("debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
#nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")
nebula_image = simplegui.load_image("nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
#splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
splash_image = simplegui.load_image("splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
#ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
ship_image = simplegui.load_image("double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png, shot4.png, shot5.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
#missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
missile_image = simplegui.load_image("shot3.png")
special_missile_info = ImageInfo([50, 45], [100, 91], 20, 50)
special_missile_image = simplegui.load_image("shot5.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
#asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
asteroid_image = simplegui.load_image("asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
#explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_image = simplegui.load_image("explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
#soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack = simplegui.load_sound("soundtrack.ogg")
#missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound = simplegui.load_sound("missile.ogg")
missile_sound.set_volume(.5)
charging_sound = simplegui.load_sound("alien_machine_gun.ogg")
charging_sound.set_volume(.5)
special_missile_sound = simplegui.load_sound("laser_blasts.ogg")
special_missile_sound.set_volume(.5)
#ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound = simplegui.load_sound("thrust.ogg")
ship_thrust_sound.set_volume(1.)
#explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound = simplegui.load_sound("explosion.ogg")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:    
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def shoot(self):
        global missile_group
        
        Missile_pos = [self.pos[0] + angle_to_vector(self.angle)[0] * self.image_size[0] / 2, self.pos[1] + angle_to_vector(self.angle)[1] * self.image_size[1] / 2]
        Missile_vel = [self.vel[0] + angle_to_vector(self.angle)[0] * 4, self.vel[1] + angle_to_vector(self.angle)[1] * 4]
        a_missile = Sprite(Missile_pos, Missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        
        missile_group.add(a_missile)

    def special_shoot(self):
        global missile_group

        Missile_pos = [self.pos[0] + angle_to_vector(self.angle)[0] * self.image_size[0] / 2, self.pos[1] + angle_to_vector(self.angle)[1] * self.image_size[1] / 2]
        Missile_vel = [self.vel[0] + angle_to_vector(self.angle)[0] * 5, self.vel[1] + angle_to_vector(self.angle)[1] * 5]
        a_missile = Sprite(Missile_pos, Missile_vel, self.angle, 0, special_missile_image, special_missile_info, special_missile_sound)
        
        missile_group.add(a_missile)
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, [self.image_center[0]+self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)                        
            
    def update(self):        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.angle += self.angle_vel        
        
        if self.thrust == True:
            self.vel[0] += angle_to_vector(self.angle)[0] * 0.1
            self.vel[1] += angle_to_vector(self.angle)[1] * 0.1  
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
        
        self.vel[0] *= (1 - Friction)
        self.vel[1] *= (1 - Friction)

    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        if self.animated:
            current_explosion_index = (self.age % 64) // 1
            current_explosion_center = [self.image_center[0] + current_explosion_index * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, current_explosion_center, self.image_size, self.pos, self.image_size, self.angle)    
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]  
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.angle += self.angle_vel
        if self.age < self.lifespan:
            self.age += 1
            return False
        else:
            return True

    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def collide(self, other_object):
        if dist(self.get_position(), other_object.get_position()) <= self.get_radius() + other_object.get_radius():
            return True
        else:
            return False

        
# help function for accessing a group of objects
def process_sprite_group(group, canvas):        
    for element in set(group):
        element.draw(canvas)
        if element.update():
            group.discard(element)

        
# help function for detecting collision between a object and a group       
def group_collide(group, other_object):        
    global explosion_group
    
    for element in set(group):
        if element.collide(other_object):
            group.discard(element)
            a_collision = Sprite(element.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(a_collision)
            return True
    return False


# help function for detecting collisions between the objects in two different groups
def group_group_collide(group1, group2):
    number_of_collision = 0
    
    for ele1 in set(group1):
        if group_collide(group2, ele1):
            number_of_collision += 1
            group1.discard(ele1)
            
    return number_of_collision


# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True

        
def draw(canvas):
    global time, started
    global score, lives
    global weapon_charging, charging_time
    global rock_group, missile_group    
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("score: "+str(score), [30, 50], 40, "Yellow")
    canvas.draw_text("lives: "+str(lives), [30, 100], 40, "Yellow")
    
    my_ship.draw(canvas)
    my_ship.update()
    #a_rock.draw(canvas)
    #a_rock.update()
    #a_missile.draw(canvas)
    #a_missile.update(

    if group_collide(rock_group, my_ship):
        lives -= 1
    
    score += group_group_collide(missile_group, rock_group) * 10
    
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas) 
    process_sprite_group(explosion_group, canvas)

    #print weapon_charging
    if weapon_charging:
        charging_sound.play()
        charging_time += 1
    else:
        charging_sound.rewind()

    canvas.draw_polygon([[20, 580], [35, 580], [35, 460], [20, 460]], 3, 'Red', 'White')
    if charging_time < 120:
        canvas.draw_polygon([[20, 580], [35, 580], [35, 580 - charging_time], [20, 580 - charging_time]], 3, 'Red', 'Orange')
    else:
        if charging_time % 10 == 0:
            canvas.draw_polygon([[20, 580], [35, 580], [35, 460], [20, 460]], 3, 'Red', 'Yellow')
        else:    
            canvas.draw_polygon([[20, 580], [35, 580], [35, 460], [20, 460]], 3, 'Red', 'Blue')
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

    # play soundtrack if started
    if started:
        soundtrack.play()
        
    # reset the game when you have zero live
    if lives == 0:
        score = 0
        lives = 3
        started = False  
        rock_group = set() 
        soundtrack.pause()
        soundtrack.rewind()
        
    
# key up and key down handler for ship        
def keyup(key):
    global Angle_Vel_Ship 
    global weapon_charging, charging_time

    # ship thruster
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = False

    # fire the big missile
    if key == simplegui.KEY_MAP["down"]:
        if charging_time >= 120:
            my_ship.special_shoot()
        weapon_charging = False
        charging_time = 0
        
    # ship rotation
    if my_ship.angle_vel == -Angle_Vel_Ship and key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = 0.
    elif my_ship.angle_vel == Angle_Vel_Ship and key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = 0.

def keydown(key):
    global Angle_Vel_Ship
    global weapon_charging

    # missile 
    if key == simplegui.KEY_MAP["space"]:        
        my_ship.shoot()
  
    # charging the weapon
    if key == simplegui.KEY_MAP["down"]:
        weapon_charging = True

    # ship_thruster
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = True
            
    # ship rotation        
    if my_ship.angle_vel == 0 and key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = -Angle_Vel_Ship
    elif my_ship.angle_vel == 0 and key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = Angle_Vel_Ship
        
    
# timer handler that spawns a rock    
def rock_spawner():
    global started
    global my_ship, rock_group

    if started == True and len(rock_group) < 12:            		        
        # randomly generate a rock with differen pos, vel, angle, angle_vel
        Rand_pos_rock = [random.randrange(WIDTH), random.randrange(HEIGHT)]	        
        Rand_vel_rock = [random.random() * 5 - 2.5, random.random() * 5 - 2.5]
        Rand_angle_rock = random.random() * 6.28 - 3.14
        Rand_angle_vel_rock = random.random() * 0.3 - 0.15
        a_rock = Sprite(Rand_pos_rock, Rand_vel_rock, Rand_angle_rock, Rand_angle_vel_rock, asteroid_image, asteroid_info)
        # ignore a rock spawn event if the spawned rock is too close to the ship
        if dist(my_ship.get_position(), a_rock.get_position()) <= (my_ship.get_radius() + a_rock.get_radius()) * 1.3:
            del a_rock
        else:
            rock_group.add(a_rock)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 1, .01, asteroid_image, asteroid_info)
rock_group = set()
#a_missile = Sprite([WIDTH / 2, HEIGHT / 2], [0, 0], 0, 0, missile_image, missile_info, missile_sound)
missile_group = set()
explosion_group = set()

# register handlers
frame.set_draw_handler(draw)
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
