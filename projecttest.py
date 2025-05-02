from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# Global variables
fovY = 100
player_pos = [0, 0, 0]  # Car starting position (x, y, z)
camera_mode = "third"
camera_distance = 500
camera_height = 300
camera_angle = 0
game_over = False
game_won = False
score = 0
ROAD_LENGTH = 2000  # The finish line will be at this z position
ROAD_WIDTH = 400
LANE_COUNT = 3  # Number of lanes
LANE_WIDTH = ROAD_WIDTH / LANE_COUNT
current_lane = 1  # Middle lane
move_speed = 5  # Forward movement speed
automatic_forward = True
# Constants for finish line
finish_line_start_z = ROAD_LENGTH - 50
finish_line_end_z = ROAD_LENGTH
finish_line_width = ROAD_WIDTH

# Obstacles
humans = []
coins = []
enemies = []

def draw_car():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    
    # Car body (main box)
    glColor3f(0.2, 0.2, 0.8)  # Blue car
    glPushMatrix()
    glScalef(40, 20, 80)  # Width, height, length
    glutSolidCube(1)
    glPopMatrix()
    
    # Car top/cabin
    glColor3f(0.3, 0.3, 0.9)
    glPushMatrix()
    glTranslatef(0, 20, -10)  # Position on top of the main body
    glScalef(30, 15, 40)      # Slightly smaller than the main body
    glutSolidCube(1)
    glPopMatrix()
    
    # Windshield
    glColor3f(0.7, 0.7, 0.9)  # Light blue for glass
    glPushMatrix()
    glTranslatef(0, 20, 15)   # Front of the cabin
    glRotatef(45, 1, 0, 0)    # Angled windshield
    glScalef(28, 1, 15)       # Thin plate
    glutSolidCube(1)
    glPopMatrix()
    
    # Wheels (four corners)
    glColor3f(0.1, 0.1, 0.1)  # Black tires
    wheel_positions = [
        (-20, -10, -30),  # Front left
        (20, -10, -30),   # Front right
        (-20, -10, 30),   # Rear left
        (20, -10, 30)     # Rear right
    ]
    
    for pos in wheel_positions:
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        glRotatef(90, 0, 1, 0)  # Rotate to align with the car's movement
        glutSolidTorus(5, 8, 16, 16)  # Inner radius, outer radius, sides, rings
        glPopMatrix()
    
    glPopMatrix()

def draw_road():
    # Draw the main road
    glColor3f(0.3, 0.3, 0.3)  # Dark gray for the road
    glBegin(GL_QUADS)
    glVertex3f(-ROAD_WIDTH/2, 0, 0)
    glVertex3f(ROAD_WIDTH/2, 0, 0)
    glVertex3f(ROAD_WIDTH/2, 0, ROAD_LENGTH)
    glVertex3f(-ROAD_WIDTH/2, 0, ROAD_LENGTH)
    glEnd()

    # Draw solid white borders
    glColor3f(1, 1, 1)
    glLineWidth(6)
    glBegin(GL_LINES)
    # Left border
    glVertex3f(-ROAD_WIDTH/2, 1, 0)
    glVertex3f(-ROAD_WIDTH/2, 1, ROAD_LENGTH)
    # Right border
    glVertex3f(ROAD_WIDTH/2, 1, 0)
    glVertex3f(ROAD_WIDTH/2, 1, ROAD_LENGTH)
    glEnd()

    # Draw dashed white lane dividers
    glEnable(GL_LINE_STIPPLE)
    glLineStipple(1, 0x00FF)  # Dash pattern
    glLineWidth(4)
    for i in range(1, LANE_COUNT):
        lane_x = -ROAD_WIDTH/2 + i * LANE_WIDTH
        glBegin(GL_LINES)
        glVertex3f(lane_x, 1.5, 0)
        glVertex3f(lane_x, 1.5, ROAD_LENGTH)
        glEnd()
    glDisable(GL_LINE_STIPPLE)

    # # Draw finish line
    # glColor3f(1, 0, 0)  # Red finish line
    # glBegin(GL_QUADS)
    # glVertex3f(-ROAD_WIDTH/2, 2, ROAD_LENGTH - 50)
    # glVertex3f(ROAD_WIDTH/2, 2, ROAD_LENGTH - 50)
    # glVertex3f(ROAD_WIDTH/2, 2, ROAD_LENGTH - 40)
    # glVertex3f(-ROAD_WIDTH/2, 2, ROAD_LENGTH - 40)
    # glEnd()
    
def draw_finish_line_floor():
    glPushMatrix()
    glTranslatef(0, 0.1, finish_line_start_z)  # Slightly above road to avoid z-fighting
    segment_length = 10
    zigzag_height = 10
    num_segments = int((finish_line_end_z - finish_line_start_z) / segment_length)
    num_zigzags = int(finish_line_width / zigzag_height)

    for i in range(num_segments):
        z = i * segment_length
        for j in range(num_zigzags):
            x_start = -finish_line_width / 2 + j * zigzag_height
            # Alternate black and white triangles to form zigzag
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)  # White
            else:
                glColor3f(0, 0, 0)  # Black
            glBegin(GL_TRIANGLES)
            # Triangle 1
            glVertex3f(x_start, 0, z)
            glVertex3f(x_start + zigzag_height, 0, z + segment_length / 2)
            glVertex3f(x_start, 0, z + segment_length)
            glEnd()

            # Triangle 2
            glBegin(GL_TRIANGLES)
            glVertex3f(x_start + zigzag_height, 0, z + segment_length / 2)
            glVertex3f(x_start + zigzag_height, 0, z + segment_length)
            glVertex3f(x_start, 0, z + segment_length)
            glEnd()
    glPopMatrix()

def draw_finish_line_banner():
    banner_height = 150  # Height from ground
    banner_top = 200     # Top of banner
    banner_z = ROAD_LENGTH - 30  # Position along road
    
    # Draw the banner poles
    glPushMatrix()
    
    # Left pole
    glColor3f(0.7, 0.7, 0.7)  # Gray
    glPushMatrix()
    glTranslatef(-ROAD_WIDTH/2 - 10, 0, banner_z)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 5, banner_top, 16, 16)
    glPopMatrix()
    
    # Right pole
    glPushMatrix()
    glTranslatef(ROAD_WIDTH/2 + 10, 0, banner_z)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 5, banner_top, 16, 16)
    glPopMatrix()
    
    # Banner cloth - alternating red and white stripes
    stripe_height = 20
    num_stripes = int((banner_top - banner_height) / stripe_height)
    
    for i in range(num_stripes):
        if i % 2 == 0:
            glColor3f(1, 0, 0)  # Red
        else:
            glColor3f(1, 1, 1)  # White
            
        y_bottom = banner_height + i * stripe_height
        y_top = y_bottom + stripe_height
        
        glBegin(GL_QUADS)
        glVertex3f(-ROAD_WIDTH/2 - 10, y_bottom, banner_z)
        glVertex3f(ROAD_WIDTH/2 + 10, y_bottom, banner_z)
        glVertex3f(ROAD_WIDTH/2 + 10, y_top, banner_z)
        glVertex3f(-ROAD_WIDTH/2 - 10, y_top, banner_z)
        glEnd()
    
    glPopMatrix()


def draw_human(human):
    if not human['active']:
        return
    
    glPushMatrix()
    glTranslatef(human['pos'][0], human['pos'][1], human['pos'][2])
    
    # Face direction of movement
    if human['dir'] > 0:  # Moving right
        glRotatef(90, 0, 1, 0)
    else:  # Moving left
        glRotatef(-90, 0, 1, 0)
    
    # Body (torso)
    glColor3f(0.2, 0.4, 0.8)  # Blue shirt
    glPushMatrix()
    glTranslatef(0, 25, 0)
    glScalef(10, 20, 6)
    glutSolidCube(1)
    glPopMatrix()
    
    # Head
    glColor3f(0.9, 0.7, 0.6)  # Skin tone
    glPushMatrix()
    glTranslatef(0, 45, 0)
    glutSolidSphere(8, 16, 16)
    glPopMatrix()
    
    # Arms - animate based on walking cycle
    arm_angle = 25 * math.sin(human['walk_cycle'])
    
    # Left arm
    glColor3f(0.2, 0.4, 0.8)
    glPushMatrix()
    glTranslatef(-8, 35, 0)
    glRotatef(arm_angle, 1, 0, 0)  # Swing forward/back
    glTranslatef(0, -10, 0)
    glScalef(3, 20, 3)
    glutSolidCube(1)
    glPopMatrix()
    
    # Right arm
    glPushMatrix()
    glTranslatef(8, 35, 0)
    glRotatef(-arm_angle, 1, 0, 0)  # Opposite swing
    glTranslatef(0, -10, 0)
    glScalef(3, 20, 3)
    glutSolidCube(1)
    glPopMatrix()
    
    # Legs - animate based on walking cycle
    leg_angle = 25 * math.sin(human['walk_cycle'])
    
    # Left leg
    glColor3f(0.1, 0.1, 0.3)  # Dark blue pants
    glPushMatrix()
    glTranslatef(-5, 15, 0)
    glRotatef(leg_angle, 1, 0, 0)  # Swing forward/back
    glTranslatef(0, -10, 0)
    glScalef(4, 20, 4)
    glutSolidCube(1)
    glPopMatrix()
    
    # Right leg
    glPushMatrix()
    glTranslatef(5, 15, 0)
    glRotatef(-leg_angle, 1, 0, 0)  # Opposite swing
    glTranslatef(0, -10, 0)
    glScalef(4, 20, 4)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()



def draw_coin(coin):
    if not coin['active']:
        return

    glPushMatrix()
    # Move to coin's position
    glTranslatef(coin['pos'][0], coin['pos'][1], coin['pos'][2])

    # Spin around z-axis (left-to-right)
    glRotatef(coin['rotation'], 0, 0, 1)

    # Draw a gold ring (torus)
    glColor3f(1, 0.85, 0.1)
    # glutSolidTorus(innerRadius, outerRadius, sides, rings)
    glutSolidTorus(4, 15, 24, 32)

    glPopMatrix()



def initialize_obstacles():
    global humans, coins
    humans = []
    coins = []
    
    # Spawn humans walking sideways across the road
    for i in range(200, ROAD_LENGTH-200, 400):  # Space them out along the road
        # Some humans start from left, some from right
        start_side = random.choice([-1, 1])
        
        # Position just outside the road
        start_x = (ROAD_WIDTH/2 + 20) * start_side
        
        humans.append({
            'pos': [start_x, 0, i],  # Start outside the road
            'dir': -start_side,      # Walk toward the opposite side
            'speed': random.uniform(1.5, 3.0),  # Walking speed
            'walk_cycle': random.uniform(0, 6.28),  # Random start phase
            'active': True
        })
    
    # Spawn coins
    for _ in range(20):
        lane = random.randint(0, LANE_COUNT-1)
        lane_center = -ROAD_WIDTH/2 + (lane + 0.5) * LANE_WIDTH
        coins.append({
            'pos': [lane_center, 25, random.randint(500, ROAD_LENGTH-200)],
            'active': True,
            'rotation': random.uniform(0, 360)
        })

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.25, 0.1, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if camera_mode == "third":
        # Third-person view behind the car
        cam_x = player_pos[0]
        cam_y = player_pos[1] + 150
        cam_z = player_pos[2] - 200
        gluLookAt(cam_x, cam_y, cam_z,
                  player_pos[0], player_pos[1] + 50, player_pos[2] + 100,
                  0, 1, 0)
    else:
        # First-person view from driver's seat
        cam_x = player_pos[0]
        cam_y = player_pos[1] + 40
        cam_z = player_pos[2] + 40
        gluLookAt(cam_x, cam_y, cam_z,
                  cam_x, cam_y, cam_z + 100,
                  0, 1, 0)

def check_collisions():
    global score, game_over, game_won
    
    # Check for finish line
    if player_pos[2] >= ROAD_LENGTH - 50:
        game_won = True
        return
    
    # Check for collisions with humans
    for human in humans:
        if not human['active']:
            continue
            
        dx = player_pos[0] - human['pos'][0]
        dz = player_pos[2] - human['pos'][2]
        
        if abs(dx) < 40 and abs(dz) < 40:
            game_over = True
            return
    
    # Check for collisions with coins
    for coin in coins:
        if not coin['active']:
            continue
            
        dx = player_pos[0] - coin['pos'][0]
        dz = player_pos[2] - coin['pos'][2]
        
        if abs(dx) < 40 and abs(dz) < 40:
            coin['active'] = False
            score += 10

def keyboardListener(key, x, y):
    global current_lane, game_over, game_won, score, player_pos
    
    key = key.decode('utf-8').lower()
    
    if game_over or game_won:
        if key == 'r':  # Restart game
            restartGame()
        return
    
    # Move left (decrease lane)
    if key == 'a' and current_lane > 0:
        current_lane -= 1
        updatePlayerPosition()
    
    # Move right (increase lane)
    elif key == 'd' and current_lane < LANE_COUNT - 1:
        current_lane += 1
        updatePlayerPosition()

def mouseListener(button, state, x, y):
    global camera_mode
    
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Toggle between third-person and first-person camera view
        if camera_mode == "third":
            camera_mode = "first"
        else:
            camera_mode = "third"
def updatePlayerPosition():
    global player_pos
    # Calculate x position based on current lane (0: leftmost, LANE_COUNT-1: rightmost)
    lane_center = -ROAD_WIDTH/2 + (current_lane + 0.5) * LANE_WIDTH
    player_pos[0] = lane_center
    player_pos[1] = 20  # Keep car slightly above road surface

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    
    # Draw game elements
    draw_road()
    draw_car()
    draw_finish_line_banner()
    draw_finish_line_floor() 
       
    for human in humans:
        draw_human(human)
    
    for coin in coins:
        draw_coin(coin)
    
    # Draw UI elements
    draw_text(10, 770, f"Score: {score}")
    
    if game_over:
        draw_text(400, 400, "GAME OVER! Press R to restart" )
    elif game_won:
        draw_text(400, 400, "YOU WON! Press R to play again")
    

    
    glutSwapBuffers()



def restartGame():
    global game_over, game_won, score, player_pos, current_lane
    game_over = False
    game_won = False
    score = 0
    current_lane = 1
    player_pos = [0, 20, 0]
    initialize_obstacles()

def idle():
    global player_pos, game_over, game_won, score
    if not game_over and not game_won:
        # Automatic forward movement
        player_pos[2] += move_speed
        
        # Update humans walking sideways
        for human in humans:
            # Move sideways (left/right)
            human['pos'][0] += human['dir'] * human['speed']
            
            # Update walking animation cycle
            human['walk_cycle'] += 0.1
            
            # If human reaches the other side of the road, reverse direction
            if (human['dir'] > 0 and human['pos'][0] > ROAD_WIDTH/2 + 20) or \
               (human['dir'] < 0 and human['pos'][0] < -ROAD_WIDTH/2 - 20):
                human['dir'] *= -1
            
            # If human is far behind player, reposition ahead
            if human['pos'][2] < player_pos[2] - 200:
                human['pos'][2] = player_pos[2] + ROAD_LENGTH/2 + random.randint(100, 500)
                # Randomize starting side again
                start_side = random.choice([-1, 1])
                human['pos'][0] = (ROAD_WIDTH/2 + 20) * start_side
                human['dir'] = -start_side
        
        # Update coins (your existing code)
        for coin in coins:
            coin['rotation'] = (coin['rotation'] + 5) % 360
            if coin['pos'][2] < player_pos[2] - 200:
                coin['pos'][2] = player_pos[2] + random.randint(100, 1000)
                coin['active'] = True
        
        check_collisions()
        check_win_condition()
    glutPostRedisplay()

def check_win_condition():
    global game_won
    if player_pos[2] >= ROAD_LENGTH:
        game_won = True

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Subway Runner")
    glEnable(GL_DEPTH_TEST)  
    updatePlayerPosition()
    initialize_obstacles()    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
