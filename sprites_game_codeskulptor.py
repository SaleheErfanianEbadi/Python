# implementation of Spaceship - program template for RiceRocks
# Made by: Salehe Erfanian Ebadi
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
start_score = 0
score = start_score
start_lives = 3
lives = start_lives
time = 0
#score = 0
#lives = 3
#time = 0
started = False

MAX_ROCK_NUMBER = 12
SHIP_VICINITY = 100
EXPLOSION_AGE = 23

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
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
    def get_position(self):
        return self.pos
        
    def set_position(self, new_pos):
        self.pos = [new_pos[0], new_pos[1]]
        
    def set_vel(self, new_vel):
        self.vel = [new_vel[0],new_vel[1]]
        
    def set_angle(self):
        self.angle_vel = 0
        self.angle = 0
    
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
        if self.animated:
            # animated explosions
            # images is tiles in 1x24
            EXPLOSION_DIM = 24
            explosion_index = [self.age % 24]
            canvas.draw_image(explosion_image, [self.image_center[0] + explosion_index[0] * self.image_size[0], 
                     self.image_center[1]], 
                     self.image_size, self.pos, self.image_size)
        
        else:
            # draw an un-animated object
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        self.age += 1
        
        if self.age < self.lifespan:
            return False
        else:
            return True
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def get_age(self):
        return self.age
        
    def collide(self, other_object):
        # get the distance between two objects
        distance = dist(self.get_position(), other_object.get_position())
        if distance <= self.radius + other_object.get_radius():
            # there was a collision
            return True
        return False
  
        
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, score, lives, start_score, start_lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        
    # reset score and lives
    score = start_score
    lives = start_lives
    
    # play the game soundtrack
    soundtrack.rewind()
    soundtrack.play()
    soundtrack.set_volume(.5)    

def draw(canvas):
    global time, started, lives, rock_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw ship
    my_ship.draw(canvas)
    
    
    # draw and update sprites
    #a_rock.draw(canvas)
    #a_rock.update()
    process_sprite_group(rock_group, canvas)
    
    # draw and update missiles
    #a_missile.draw(canvas)
    #a_missile.update()
    process_sprite_group(missile_group, canvas)
    
    # draw and update explosions
    process_sprite_group(explosion_group, canvas)
    
    
    # check for collisions between the ship and rocks
    if group_collide(rock_group, my_ship):
        # if collision occurs decrease the number of lives by one
        lives -= 1
        if lives == 0:
            started = False
            # pause the game sound track
            soundtrack.pause()
            # remove all rocks and no rocks are respawned until start of new game
            rock_group = set([])
            # put the ship in the center
            my_ship.set_position([WIDTH / 2, HEIGHT / 2])
            my_ship.set_vel([0, 0])
            #my_ship.set_angle()
        
    # collisons between missiles and rocks    
    group_group_collide(rock_group, missile_group)

    # update ship
    my_ship.update()
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started
    # add a rock to the rock group only when there are less than maximum number of rocks on screen
    if len(rock_group) < MAX_ROCK_NUMBER and started:
        #create a rock in a random position inside the canvas but not close to the ship
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        while dist(rock_pos, my_ship.get_position()) < SHIP_VICINITY:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        
        #rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        rock_avel = random.random() * .2 - .1
        
        # if the score is greater than 12 increase the rock velocity to increase fun
        if score > 12:
            rock_vel = [random.random() * (score / 20) - .3, random.random() * (score / 20) - .3]
            #rock_avel = random.random() * (score / 60) - .1 
            
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        # add a rock to the rock group
        rock_group.add(a_rock)
        
        
def process_sprite_group(sprite_group, canvas):
    # handle removal of old missiles (called sprite here because of function)
    sprite_remove = set([])
    for sprite in sprite_group:
        if sprite.update():
            sprite_remove.add(sprite)
    # actual removal
    sprite_group.difference_update(sprite_remove)
    
    # handle removal of old explosions
    explosion_remove = set([])
    for explosion in explosion_group:
        # image is tiles 1x24 so a duration is 0-23
        if explosion.get_age() > EXPLOSION_AGE:
            explosion_remove.add(explosion)
        # actual removal
        explosion_group.difference_update(explosion_remove)
        #print explosion.get_age()
    
    
    # draw and update each sprite in the sprite group
    for sprite in sprite_group:
        sprite.update()
        sprite.draw(canvas)
    
                
def group_collide(group, other_object):
    global explosion_group
    
    # objects to remove
    remove_group = set([])
    collision_occurred = False
    for sprite in group:
        if sprite.collide(other_object):
            # remove this rock from the group
            remove_group.add(sprite)
            collision_occurred = True
            # create a new explosion
            # pos, vel, ang, ang_vel, image, info, sound = None
            explosion_pos = sprite.get_position()
            new_explosion = Sprite(explosion_pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(new_explosion)
            
    # remove that sprite from the group
    group.difference_update(remove_group)
    return collision_occurred
        
        
def group_group_collide(group_one, group_two):
    global score
    
    group_one_copy = group_one
    number_collided = 0
    #remove_sprite = set([])
    
    for item in group_one_copy:
        if group_collide(group_two, item):
            number_collided += 1
            #remove_sprite.add(item)
            group_one.discard(item)
            
    score += number_collided
    return number_collided


    
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)
rock_group = set([])
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
missile_group = set([])
explosion_group = set([])


# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
