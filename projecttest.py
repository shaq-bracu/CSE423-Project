from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# Game state variables
game_over = False
game_won = False
score = 0

# Coordinate system constants
X_MIN = -400
X_MAX = 400
Y_MIN = 0
Y_MAX = 300
Z_MIN = 0
Z_MAX = 10000  # Finish line position

# Camera-related variables
camera_pos = (-500, 0, 700)
fovY = 60  # Field of view
GRID_LENGTH = 600  # Length of grid lines

# Player position and movement
player_pos = [0, 20, 0]  # [x, y, z] in coordinate system
move_speed = 5
super_power_active = False
bullets = []

# Game objects
humans = []
coins = []

class CBullet:
    def __init__(self, x, y, z):
        self.pos = [x, y, z + 50]
        self.active = True
         
    def update_position(self):
        if self.active:
            self.pos[2] += 20
            
            # Deactivate bullets that go too far
            if self.pos[2] > player_pos[2] + 1000:
                self.active = False

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
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

def draw_car():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    
    # Car body (blue box)
    glColor3f(0.2, 0.7, 1.0)
    glPushMatrix()
    glScalef(40, 20, 80)
    glutSolidCube(1)
    glPopMatrix()
    
    # Car top (darker blue)
    glColor3f(0.1, 0.4, 0.8)
    glPushMatrix()
    glTranslatef(0, 20, -10)
    glScalef(30, 15, 40)
    glutSolidCube(1)
    glPopMatrix()
    
    # Wheels (four corners)
    glColor3f(0.1, 0.1, 0.1)
    wheel_positions = [
        (-20, -10, -30),  # Front left
        (20, -10, -30),   # Front right
        (-20, -10, 30),   # Rear left
        (20, -10, 30)     # Rear right
    ]
    
    for pos in wheel_positions:
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        glRotatef(90, 0, 1, 0)
        glutSolidTorus(5, 8, 16, 16)
        glPopMatrix()
    
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
    
    # Arms with walking animation
    arm_angle = 25 * math.sin(human['walk_cycle'])
    
    # Left arm
    glColor3f(0.2, 0.4, 0.8)
    glPushMatrix()
    glTranslatef(-8, 35, 0)
    glRotatef(arm_angle, 1, 0, 0)
    glTranslatef(0, -10, 0)
    glScalef(3, 20, 3)
    glutSolidCube(1)
    glPopMatrix()
    
    # Right arm
    glPushMatrix()
    glTranslatef(8, 35, 0)
    glRotatef(-arm_angle, 1, 0, 0)
    glTranslatef(0, -10, 0)
    glScalef(3, 20, 3)
    glutSolidCube(1)
    glPopMatrix()
    
    # Legs with walking animation
    leg_angle = 25 * math.sin(human['walk_cycle'])
    
    # Left leg
    glColor3f(0.1, 0.1, 0.3)  # Dark blue pants
    glPushMatrix()
    glTranslatef(-5, 15, 0)
    glRotatef(leg_angle, 1, 0, 0)
    glTranslatef(0, -10, 0)
    glScalef(4, 20, 4)
    glutSolidCube(1)
    glPopMatrix()
    
    # Right leg
    glPushMatrix()
    glTranslatef(5, 15, 0)
    glRotatef(-leg_angle, 1, 0, 0)
    glTranslatef(0, -10, 0)
    glScalef(4, 20, 4)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()

def draw_coin(coin):
    if not coin['active']:
        return
    
    glPushMatrix()
    glTranslatef(coin['pos'][0], coin['pos'][1], coin['pos'][2])
    
    # Make the coin stand upright
    glRotatef(0, 1, 0, 0)
    
    # Draw a gold ring
    glColor3f(1, 0.85, 0.1)  # Gold color
    glutSolidTorus(3, 15, 24, 32)  # Inner radius, outer radius, sides, rings
    
    glPopMatrix()

def draw_bullet(bullet):
    if not bullet.active:
        return
        
    glPushMatrix()
    glTranslatef(bullet.pos[0], bullet.pos[1], bullet.pos[2])
    glColor3f(1, 0.5, 0)  # Orange color
    glutSolidSphere(5, 10, 10)
    
    # Add a trail effect
    glColor4f(1, 0.3, 0, 0.5)  # Semi-transparent orange
    glPushMatrix()
    glScalef(1, 1, 5)
    glutSolidSphere(4, 8, 8)
    glPopMatrix()
    
    glPopMatrix()

def draw_road():
    # Main road surface
    glColor3f(0.3, 0.3, 0.3)  # Dark gray for the road
    glBegin(GL_QUADS)
    glVertex3f(X_MIN, Y_MIN, Z_MIN)
    glVertex3f(X_MAX, Y_MIN, Z_MIN)
    glVertex3f(X_MAX, Y_MIN, Z_MAX)
    glVertex3f(X_MIN, Y_MIN, Z_MAX)
    glEnd()

    # Road borders (solid white lines)
    glColor3f(1, 1, 1)
    glLineWidth(6)
    glBegin(GL_LINES)
    # Left border
    glVertex3f(X_MIN, Y_MIN + 1, Z_MIN)
    glVertex3f(X_MIN, Y_MIN + 1, Z_MAX)
    # Right border
    glVertex3f(X_MAX, Y_MIN + 1, Z_MIN)
    glVertex3f(X_MAX, Y_MIN + 1, Z_MAX)
    glEnd()

    # Middle dashed line
    glEnable(GL_LINE_STIPPLE)
    glLineStipple(1, 0x00FF)  # Dash pattern
    glLineWidth(4)
    glBegin(GL_LINES)
    glVertex3f(0, Y_MIN + 1.5, Z_MIN)
    glVertex3f(0, Y_MIN + 1.5, Z_MAX)
    glEnd()
    glDisable(GL_LINE_STIPPLE)

def draw_finish_line():
    # Checkered floor pattern
    glPushMatrix()
    segment_length = 10
    zigzag_height = 10
    finish_start = Z_MAX - 50
    finish_end = Z_MAX
    
    glTranslatef(0, Y_MIN + 0.1, finish_start)  # Slightly above road
    
    num_segments = int((finish_end - finish_start) / segment_length)
    num_zigzags = int((X_MAX - X_MIN) / zigzag_height)

    for i in range(num_segments):
        z = i * segment_length
        for j in range(num_zigzags):
            x_start = X_MIN + j * zigzag_height
            # Alternate black and white
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)  # White
            else:
                glColor3f(0, 0, 0)  # Black
                
            glBegin(GL_TRIANGLES)
            # First triangle
            glVertex3f(x_start, 0, z)
            glVertex3f(x_start + zigzag_height, 0, z + segment_length / 2)
            glVertex3f(x_start, 0, z + segment_length)
            glEnd()

            # Second triangle
            glBegin(GL_TRIANGLES)
            glVertex3f(x_start + zigzag_height, 0, z + segment_length / 2)
            glVertex3f(x_start + zigzag_height, 0, z + segment_length)
            glVertex3f(x_start, 0, z + segment_length)
            glEnd()
    glPopMatrix()
    
    # Banner above finish line
    banner_height = 150
    banner_top = 200
    banner_z = Z_MAX - 30
    
    # Left pole
    glColor3f(0.7, 0.7, 0.7)  # Gray
    glPushMatrix()
    glTranslatef(X_MIN - 10, Y_MIN, banner_z)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 5, banner_top, 16, 16)
    glPopMatrix()
    
    # Right pole
    glPushMatrix()
    glTranslatef(X_MAX + 10, Y_MIN, banner_z)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 5, banner_top, 16, 16)
    glPopMatrix()
    
    # Banner with stripes
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
        glVertex3f(X_MIN - 10, y_bottom, banner_z)
        glVertex3f(X_MAX + 10, y_bottom, banner_z)
        glVertex3f(X_MAX + 10, y_top, banner_z)
        glVertex3f(X_MIN - 10, y_top, banner_z)
        glEnd()

def initialize_obstacles():
    global humans, coins
    humans = []
    coins = []
    
    # Spawn humans walking sideways across the road
    for z in range(500, Z_MAX-500, 400):
        # Some humans start from left, some from right
        start_side = random.choice([-1, 1])
        
        # Position just outside the road
        start_x = (X_MAX + 20) * start_side
        
        humans.append({
            'pos': [start_x, Y_MIN, z],  # Start outside the road
            'dir': -start_side,          # Walk toward the opposite side
            'speed': random.uniform(1.5, 3.0),  # Walking speed
            'walk_cycle': random.uniform(0, 6.28),  # Random start phase
            'active': True
        })
    
    # Spawn coins
    for _ in range(20):
        x_pos = random.uniform(X_MIN + 50, X_MAX - 50)
        coins.append({
            'pos': [x_pos, Y_MIN + 25, random.randint(500, Z_MAX-500)],
            'active': True
        })

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, Z_MAX + 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Third-person view behind the car
    cam_x = player_pos[0]
    cam_y = Y_MIN + 150
    cam_z = player_pos[2] - 200
    
    # Look at point ahead of player
    look_x = player_pos[0]
    look_y = Y_MIN + 50
    look_z = player_pos[2] + 100
    
    gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 1, 0)

def check_super_power_activation():
    global super_power_active
    if score >= 40 and not super_power_active:
        super_power_active = True

def shoot_bullet():
    global bullets
    if super_power_active:
        bullets.append(CBullet(player_pos[0], player_pos[1], player_pos[2]))

def update_bullets():
    global bullets
    
    # Move bullets forward
    for bullet in bullets:
        if bullet.active:
            bullet.update_position()
            
            # Check collision with humans
            for human in humans:
                if human['active']:
                    dx = bullet.pos[0] - human['pos'][0]
                    dz = bullet.pos[2] - human['pos'][2]
                    distance = math.sqrt(dx**2 + dz**2)
                    
                    if distance < 30:  # Collision threshold
                        human['active'] = False  # Deactivate human
                        bullet.active = False  # Deactivate bullet
                        break
    
    # Remove inactive bullets
    bullets = [b for b in bullets if b.active]

def check_collisions():
    global score, game_over, game_won
    
    # Check for finish line
    if player_pos[2] >= Z_MAX - 50:
        game_won = True
        return
    
    # Check for collisions with humans
    for human in humans:
        if not human['active']:
            continue
            
        dx = player_pos[0] - human['pos'][0]
        dz = player_pos[2] - human['pos'][2]
        distance = math.sqrt(dx**2 + dz**2)
        
        if distance < 40:
            game_over = True
            return
    
    # Check for collisions with coins
    for coin in coins:
        if not coin['active']:
            continue
            
        dx = player_pos[0] - coin['pos'][0]
        dz = player_pos[2] - coin['pos'][2]
        distance = math.sqrt(dx**2 + dz**2)
        
        if distance < 40:
            coin['active'] = False
            score += 10

def keyboardListener(key, x, y):
    global player_pos, game_over, game_won
    
    if game_over or game_won:
        if key == b'r':  # Restart
            restart_game()
        return
    
    # Move left
    if key == b'd' and player_pos[0] > X_MIN + 50:
        player_pos[0] -= 25
    
    # Move right
    if key == b'a' and player_pos[0] < X_MAX - 50:
        player_pos[0] += 25
    
    # Shoot bullet with super power
    if key == b' ' and super_power_active:
        shoot_bullet()

def restart_game():
    global game_over, game_won, score, player_pos, super_power_active, bullets
    game_over = False
    game_won = False
    score = 0
    player_pos = [0, 20, 0]
    super_power_active = False
    bullets = []
    initialize_obstacles()

def idle():
    global player_pos, game_over, game_won, score
    
    if not game_over and not game_won:
        # Automatic forward movement
        player_pos[2] += move_speed
        
        # Check for super power activation
        check_super_power_activation()
        
        # Auto-shoot if super power is active
        if super_power_active and int(player_pos[2]) % 100 == 0:
            shoot_bullet()
        
        # Update bullets
        update_bullets()
        
        # Update humans walking sideways
        for human in humans:
            # Move sideways (left/right)
            human['pos'][0] += human['dir'] * human['speed']
            
            # Update walking animation cycle
            human['walk_cycle'] += 0.1
            
            # If human reaches the other side of the road, reverse direction
            if (human['dir'] > 0 and human['pos'][0] > X_MAX + 20) or \
               (human['dir'] < 0 and human['pos'][0] < X_MIN - 20):
                human['dir'] *= -1
            
            # If human is far behind player, reposition ahead
            if human['pos'][2] < player_pos[2] - 200:
                new_z = min(player_pos[2] + random.randint(500, 2000), Z_MAX - 600)
                human['pos'][2] = new_z
                # Randomize starting side again
                start_side = random.choice([-1, 1])
                human['pos'][0] = (X_MAX + 20) * start_side
                human['dir'] = -start_side
        
        # Update coins
        for coin in coins:
            if coin['pos'][2] < player_pos[2] - 200:
                new_z = min(player_pos[2] + random.randint(500, 2000), Z_MAX - 600)
                new_x = random.uniform(X_MIN + 50, X_MAX - 50)
                coin['pos'][0] = new_x
                coin['pos'][2] = new_z
                coin['active'] = True
        
        check_collisions()
    
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    
    setupCamera()
    
    # Draw game elements
    draw_road()
    draw_car()
    draw_finish_line()
    
    # Draw game objects
    for human in humans:
        draw_human(human)
    
    for coin in coins:
        draw_coin(coin)
    
    for bullet in bullets:
        draw_bullet(bullet)
    
    # Display game info
    draw_text(10, 770, f"Score: {score}")
    
    if super_power_active:
        draw_text(10, 740, "SUPER POWER ACTIVE! Press SPACE to shoot")
    
    if game_over:
        draw_text(400, 400, "GAME OVER! Press R to restart")
    elif game_won:
        draw_text(400, 400, "YOU WON! Press R to play again")
    
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Subway Runners")
    
    # Enable depth testing
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Initialize game state
    initialize_obstacles()
    
    # Register callbacks
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutIdleFunc(idle)
    
    # Start the main loop
    glutMainLoop()

if __name__ == "__main__":
    main()
