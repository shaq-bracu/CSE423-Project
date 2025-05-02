from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# Coordinate System Constants
X_MIN = -250  # Left edge of road
X_MAX = 250   # Right edge of road
Y_MIN = 0     # Ground level
Y_MAX = 300   # Maximum height
Z_MIN = 0     # Start line
Z_MAX = 10000 # Finish line position

# Game State
LANE_COUNT = 3
LANE_WIDTH = (X_MAX - X_MIN) / LANE_COUNT
LANE_POSITIONS = [
    X_MIN + (LANE_WIDTH/2),                # Left lane
    X_MIN + (LANE_WIDTH/2) + LANE_WIDTH,   # Middle lane
    X_MIN + (LANE_WIDTH/2) + 2*LANE_WIDTH  # Right lane
]

# Player variables
player_pos = [0, 20, 0]  # Initial position in coordinate system
current_lane = 1         # Middle lane (0=left, 1=middle, 2=right)
move_speed = 5           # Units per frame in Z direction
target_x = 0             # Target X position for smooth movement
is_transitioning = False # Whether car is currently changing lanes
transition_speed = 2.0   # Speed of lane transition

# Game state
camera_mode = "third"    # Third-person view by default
game_over = False
game_won = False
score = 0
super_power_active = False
bullets = []

# Game objects
humans = []
coins = []

def map_to_lane(lane_index):
    """Convert lane index to X coordinate"""
    return LANE_POSITIONS[lane_index]

def draw_car():
    """Draw the player's car at its current position in the coordinate system"""
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
    """Draw the road using coordinate system boundaries"""
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

    # Lane dividers (dashed white lines)
    glEnable(GL_LINE_STIPPLE)
    glLineStipple(1, 0x00FF)  # Dash pattern
    glLineWidth(4)
    for i in range(1, LANE_COUNT):
        lane_x = X_MIN + i * LANE_WIDTH
        glBegin(GL_LINES)
        glVertex3f(lane_x, Y_MIN + 1.5, Z_MIN)
        glVertex3f(lane_x, Y_MIN + 1.5, Z_MAX)
        glEnd()
    glDisable(GL_LINE_STIPPLE)

def draw_finish_line():
    """Draw checkered finish line and banner"""
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

def draw_human(human):
    """Draw a human character with walking animation"""
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
    
    # Legs with walking animation
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
    """Draw a spinning coin"""
    if not coin['active']:
        return

    glPushMatrix()
    glTranslatef(coin['pos'][0], coin['pos'][1], coin['pos'][2])
    
    # Make the coin stand up (rotate 90 degrees around x-axis)
    glRotatef(90, 1, 0, 0)
    
    # Spin the coin around its own axis
    glRotatef(coin['rotation'], 0, 0, 1)
    
    # Draw a golden coin using cylinder and disks
    glColor3f(1, 0.85, 0.1)  # Gold color
    
    # Create quadric object for drawing
    quadric = gluNewQuadric()
    
    # Draw the coin edge (thin cylinder)
    gluCylinder(quadric, 15, 15, 3, 32, 1)
    
    # Draw front face (disk)
    glPushMatrix()
    gluDisk(quadric, 0, 15, 32, 1)
    glPopMatrix()
    
    # Draw back face (disk)
    glPushMatrix()
    glTranslatef(0, 0, 3)
    gluDisk(quadric, 0, 15, 32, 1)
    glPopMatrix()
    
    glPopMatrix()

def draw_bullet(bullet):
    """Draw a bullet for super power"""
    if not bullet['active']:
        return
        
    glPushMatrix()
    glTranslatef(bullet['pos'][0], bullet['pos'][1], bullet['pos'][2])
    glColor3f(1, 0.5, 0)  # Orange color
    glutSolidSphere(5, 10, 10)  # Small sphere for the bullet
    
    # Add a glowing trail
    glColor4f(1, 0.3, 0, 0.5)  # Semi-transparent orange
    glPushMatrix()
    glScalef(1, 1, 5)  # Elongated in z direction
    glutSolidSphere(4, 8, 8)
    glPopMatrix()
    
    glPopMatrix()

def initialize_obstacles():
    """Initialize all game objects in the coordinate system"""
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
    
    # Spawn coins in lanes
    for _ in range(20):
        lane = random.randint(0, LANE_COUNT-1)
        coins.append({
            'pos': [LANE_POSITIONS[lane], Y_MIN + 25, random.randint(500, Z_MAX-500)],
            'active': True,
            'rotation': random.uniform(0, 360)
        })

def setup_camera():
    """Set up the camera view using coordinate system"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.25, 0.1, Z_MAX + 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if camera_mode == "third":
        # Third-person view behind the car
        cam_x = player_pos[0]
        cam_y = Y_MIN + 150
        cam_z = player_pos[2] - 200
        
        # Look at point ahead of player
        look_x = player_pos[0]
        look_y = Y_MIN + 50
        look_z = player_pos[2] + 100
        
        gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 1, 0)
    else:
        # First-person view from driver's seat
        cam_x = player_pos[0]
        cam_y = player_pos[1] + 40
        cam_z = player_pos[2] + 40
        gluLookAt(cam_x, cam_y, cam_z,
                  cam_x, cam_y, cam_z + 100,
                  0, 1, 0)

def check_super_power_activation():
    """Check if player has enough score to activate super power"""
    global super_power_active
    if score >= 50 and not super_power_active:
        super_power_active = True

def shoot_bullet():
    """Create a new bullet in front of the car"""
    global bullets
    if super_power_active:
        bullet = {
            'pos': [player_pos[0], player_pos[1] + 10, player_pos[2] + 40],
            'active': True
        }
        bullets.append(bullet)

def update_bullets():
    """Update bullet positions and check for collisions"""
    global bullets
    bullet_speed = 20
    
    # Move bullets forward
    for bullet in bullets:
        if bullet['active']:
            bullet['pos'][2] += bullet_speed
            
            # Check collision with humans
            for human in humans:
                if human['active']:
                    dx = bullet['pos'][0] - human['pos'][0]
                    dz = bullet['pos'][2] - human['pos'][2]
                    distance = math.sqrt(dx**2 + dz**2)
                    
                    if distance < 30:  # Collision threshold
                        human['active'] = False  # Deactivate human
                        bullet['active'] = False  # Deactivate bullet
                        break
            
            # Remove bullets that go too far
            if bullet['pos'][2] > player_pos[2] + 1000:
                bullet['active'] = False
    
    # Remove inactive bullets
    bullets = [b for b in bullets if b['active']]

def check_collisions():
    """Check for collisions between player and game objects"""
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

def calculate_target_position():
    """Calculate target X position based on current lane"""
    global target_x
    target_x = LANE_POSITIONS[current_lane]

def keyboard_listener(key, x, y):
    """Handle keyboard input"""
    global current_lane, is_transitioning, camera_mode
    
    key = key.decode('utf-8').lower()
    
    if game_over or game_won:
        if key == 'r':  # Restart game
            restart_game()
        return
    
    # Only accept new lane changes if not currently transitioning
    if not is_transitioning:
        # Move left
        if key == 'a' and current_lane < LANE_COUNT - 1:
            current_lane += 1
            calculate_target_position()
            is_transitioning = True
        
        # Move right
        elif key == 'd' and current_lane > 0:
            current_lane -= 1
            calculate_target_position()
            is_transitioning = True
    
    # Toggle camera view
    if key == 'c':
        camera_mode = "first" if camera_mode == "third" else "third"
    
    # Manual fire bullet with super power
    if key == ' ' and super_power_active:
        shoot_bullet()

def mouse_listener(button, state, x, y):
    """Handle mouse input"""
    global camera_mode
    
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Toggle between third-person and first-person camera view
        camera_mode = "first" if camera_mode == "third" else "third"

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    """Draw text on screen"""
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

def show_screen():
    """Main display function"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setup_camera()
    
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
    
    # Draw UI elements
    draw_text(10, 770, f"Score: {score}")
    
    
    if super_power_active:
        draw_text(10, 710, "SUPER POWER ACTIVE!")
    
    if game_over:
        draw_text(400, 400, "GAME OVER! Press R to restart")
    elif game_won:
        draw_text(400, 400, "YOU WON! Press R to play again")
    
    glutSwapBuffers()

def restart_game():
    """Reset the game to initial state"""
    global game_over, game_won, score, player_pos, current_lane, super_power_active, bullets
    game_over = False
    game_won = False
    score = 0
    current_lane = 1
    player_pos = [0, 20, 0]
    super_power_active = False
    bullets = []
    calculate_target_position()
    initialize_obstacles()

def idle():
    """Main game loop function"""
    global player_pos, game_over, game_won, score, is_transitioning
    
    if not game_over and not game_won:
        # Automatic forward movement
        player_pos[2] += move_speed
        
        # Handle smooth lane transitions
        if is_transitioning:
            # Calculate distance to target
            distance = target_x - player_pos[0]
            # If we're close enough to the target, snap to it and end transition
            if abs(distance) < transition_speed:
                player_pos[0] = target_x
                is_transitioning = False
            else:
                # Move toward target position
                player_pos[0] += transition_speed * (1 if distance > 0 else -1)
        
        # Check for super power activation
        check_super_power_activation()
        
        # Auto-shoot if super power is active (every 20 frames)
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
                human['pos'][2] = player_pos[2] + (Z_MAX/2) + random.randint(100, 500)
                # Randomize starting side again
                start_side = random.choice([-1, 1])
                human['pos'][0] = (X_MAX + 20) * start_side
                human['dir'] = -start_side
        
        # Update coins
        for coin in coins:
            coin['rotation'] = (coin['rotation'] + 5) % 360
            if coin['pos'][2] < player_pos[2] - 200:
                coin['pos'][2] = player_pos[2] + random.randint(100, 1000)
                coin['active'] = True
        
        check_collisions()
    
    glutPostRedisplay()

def main():
    """Initialize and start the game"""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Subway Runner")
    
    # Enable depth testing for 3D rendering
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Initialize game state
    calculate_target_position()
    initialize_obstacles()
    
    # Register callback functions
    glutDisplayFunc(show_screen)
    glutKeyboardFunc(keyboard_listener)
    glutMouseFunc(mouse_listener)
    glutIdleFunc(idle)
    
    # Start the main loop
    glutMainLoop()

if __name__ == "__main__":
    main()
