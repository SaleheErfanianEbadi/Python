# implementation of card game - Memory
# Created by Salehe Erfanian Ebadi
# Contact s.erfanianebadi@qmul.ac.uk

import simplegui
import random

# helper function to initialize globals
def new_game():
    # initialize global variables for a new game
    global deck, exposed, state, pre_clicked, turns
    turns = 0
    label.set_text("Turns = " + str(turns))
    state = 0
    deck = [0, 1, 2, 3, 4, 5, 6, 7] * 2
    random.shuffle(deck)
    exposed = [0] * 16
    pre_clicked = [None, None]
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, state, pre_clicked, turns
    
    clicked_card = pos[0] // 50
    
    # simulate mouse click - determine no. of exposed cards
    if state == 0:
        state = 1
        exposed[clicked_card] = 1
        pre_clicked[0] = clicked_card
        turns += 1
        label.set_text("Turns = " + str(turns))
            
    elif state == 1:
        if exposed[clicked_card] == 0:
            exposed[clicked_card] = 1
            state = 2
            pre_clicked[1] = clicked_card
        else:
            state = 2
            pre_clicked[1] = clicked_card
        
    else:
        if deck[pre_clicked[0]] == deck[pre_clicked[1]]:
            exposed[pre_clicked[0]] = 1
            exposed[pre_clicked[1]] = 1
        else:
            exposed[pre_clicked[0]] = 0
            exposed[pre_clicked[1]] = 0
            
            
        if exposed[clicked_card] == 0:
            exposed[clicked_card] = 1
            state = 1
            turns += 1
            label.set_text("Turns = " + str(turns))
            
        pre_clicked = [clicked_card, clicked_card]
        
        # if all the cards are paired next click starts a new game
        if exposed == [1] * 16:
            new_game()
                         
# cards are logically 50x100 pixels in size    
def draw(canvas):
    x_pos = 0
    for i in range(16):
        if exposed[i] == 0:
            # draw outline for cards that are unexposed
            canvas.draw_polygon([(3 + x_pos, 3), (3 + x_pos, 97), (47 + x_pos, 97), (47 + x_pos, 3)], 2, "Teal")
            canvas.draw_polygon([(4 + x_pos, 4), (4 + x_pos + 10, 4), (4 + x_pos, 4 + 10)], 3, "Teal", "Teal")
            x_pos += 50
        else:
            # draw outline for cards that are exposed
            canvas.draw_polygon([(3 + x_pos, 3), (3 + x_pos, 97), (47 + x_pos, 97), (47 + x_pos, 3)], 2, "Olive")
            canvas.draw_polygon([(46 + x_pos - 10, 96), (46 + x_pos, 96), (46 + x_pos, 86)], 3, "Olive", "Olive")
            
            # draw card number
            canvas.draw_text(str(deck[i]), (12 + x_pos, 65), 50, 'White')
            x_pos += 50
            
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric
