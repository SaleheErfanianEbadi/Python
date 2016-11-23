# Implementation of classic arcade game Pong
# Created by Salehe Erfanian Ebadi
# Contact s.erfanianebadi@qmul.ac.uk

# Player one: Arrow Keys
# Player two: 'W' and 'S' Keys

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
score1 = 0
score2 = 0

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]

paddle1_pos = [[HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]
paddle2_pos = [[WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]
paddle1_vel = 0#-1 #[paddle1_pos[0][1] + -300, paddle1_pos[1][1] + -300] # vertical coordinates for beginning and end of the paddle
paddle2_vel = 0#1 #[paddle2_pos[0][1], paddle2_pos[1][1]]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240) / 60 # velocity per second
        ball_vel[1] = -random.randrange(60, 180) / 60
    elif direction == LEFT:
        ball_vel[0] = -random.randrange(120, 240) / 60
        ball_vel[1] = -random.randrange(60, 180) / 60
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    score1 = 0
    score2 = 0
    
    paddle1_pos = [[HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]
    paddle2_pos = [[WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]
    paddle1_vel = 0
    paddle2_vel = 0
    
    spawn_ball(LEFT)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # top edge collision
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    # bottom edge collision
    elif ball_pos[1] >= (HEIGHT -1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
        
    # left gutter collission
    if (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH):
        if ((ball_pos[1] >= paddle1_pos[0][1]) and (ball_pos[1] <= paddle1_pos[1][1])):
            # increase ball speed by 10% and change direction
            ball_vel[0] = -(ball_vel[0] + 0.1 * ball_vel[0])
            ball_vel[1] = (ball_vel[1] + 0.1 * ball_vel[1])
        else:
            # hit the gutter, spawn the ball in the opposite direction
            spawn_ball(RIGHT)
            score1 += 1
            
    # right gutter collission
    elif ball_pos[0] >= (WIDTH -1) - BALL_RADIUS - PAD_WIDTH:
        if ((ball_pos[1] >= paddle2_pos[0][1]) and (ball_pos[1] <= paddle2_pos[1][1])):
            # increase ball speed by 10% and change direction
            ball_vel[0] = -(ball_vel[0] + 0.1 * ball_vel[0])
            ball_vel[1] = (ball_vel[1] + 0.1 * ball_vel[1])
        else:
            # hit the gutter, spawn the ball in the opposite direction
            spawn_ball(LEFT)
            score2 += 1
            
            
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    
    # update paddle's vertical position, keep paddle on the screen
    # left paddle    
    if paddle1_pos[0][1] <= 0:
        paddle1_pos[0][1] = 1
        paddle1_pos[1][1] = 1 + PAD_HEIGHT
        
    elif paddle1_pos[1][1] >= HEIGHT:
        paddle1_pos[0][1] = HEIGHT - PAD_HEIGHT - 1
        paddle1_pos[1][1] = HEIGHT - 1
        
    else:
        paddle1_pos[0][1] += paddle1_vel
        paddle1_pos[1][1] += paddle1_vel
        
    # right paddle
    if paddle2_pos[0][1] <= 0:
        paddle2_pos[0][1] = 1
        paddle2_pos[1][1] = 1 + PAD_HEIGHT
        
    elif paddle2_pos[1][1] >= HEIGHT:
        paddle2_pos[0][1] = HEIGHT - PAD_HEIGHT - 1
        paddle2_pos[1][1] = HEIGHT - 1
        
    else:
        paddle2_pos[0][1] += paddle2_vel
        paddle2_pos[1][1] += paddle2_vel
    
    
    # draw paddles
    # paddle1 - left
    c.draw_line(paddle1_pos[0], paddle1_pos[1], PAD_WIDTH, "White")
    # paddle2 - right
    c.draw_line(paddle2_pos[0], paddle2_pos[1], PAD_WIDTH, "White")
    
    
    # draw scores
    c.draw_text(str(score2), (220, 60), 60, "White", "monospace")
    c.draw_text(str(score1), (340, 60), 60, "White", "monospace")
        
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 10
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += vel
        
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= vel
        
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += vel
        
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= vel
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    vel = 10
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel -= vel
        
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel += vel
        
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel -= vel
        
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel += vel

def restart():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', restart)


# start frame
new_game()
frame.start()
