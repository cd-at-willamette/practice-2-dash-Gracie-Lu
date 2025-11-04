from pgl import *

# Constants
WINDOW = 400
TICK_MS = 100

# Derived Constants
BLOCK = WINDOW / 10
GROUND = WINDOW - BLOCK
GRAVITY = BLOCK / 4
FLOOR = GROUND - BLOCK # Blocks need to be placed block height above the ground to be on the floor.
DANGER = 3 * BLOCK # anything within a block, on either side, of the hazard impacts the hazard

# Window setup
gw = GWindow(WINDOW,WINDOW)

# ground code here, possibly
ground = GLine(0, GROUND, WINDOW, GROUND)
gw.add(ground)

# player code here, possibly
player = GRect(BLOCK, FLOOR, BLOCK, BLOCK)
player.set_filled(True)
player.set_color('pink')
gw.add(player)

# hazard code here, possibly
hazard = GRect(WINDOW, FLOOR, BLOCK, BLOCK)
hazard.set_filled(True)
hazard.set_color('teal')
gw.add(hazard)

pause = True
start = True
gw.vy = 40
gw.vx = BLOCK
score = [0]

def hit(x, y):
    global start
    obj = gw.get_element_at(x, y)
    if obj is hazard:
        print("Your score is:", score[0])
        start = True
        score[0] = 0
        hazard.set_location(WINDOW, FLOOR)

def tick():
    global pause
    global start
    if start:
        return
    gw.x = hazard.get_x()
    gw.x -= gw.vx
    hazard.set_location(gw.x, FLOOR)
    if gw.x < 0:
        hazard.set_location(WINDOW, FLOOR)
    hit(player.get_x(), player.get_y())
    if pause:
        return
    gw.y = player.get_y()
    gw.y -= gw.vy
    gw.vy -= GRAVITY
    player.set_location(BLOCK, gw.y)
    if gw.y >= GROUND - BLOCK:
        gw.vy = 0
        pause = True
        gw.vy = 40
        score[0] += 1
    pass

def jump(e):
    global pause
    global start
    x = e.get_x()
    y = e.get_y()
    if 0 <= x <= WINDOW and 0 <= y <= WINDOW:
        pause = False
        start = False
    pass

# Event setup
gw.set_interval(tick, TICK_MS)
gw.add_event_listener("click", jump)
