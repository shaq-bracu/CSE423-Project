from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

bullets = []
fps = True
vtog = True
plife = 5
bmiss = 0
score = 0

gameover = False
if plife<=0:
    gameover = not gameover


# Camera-related variables
cheat = False
ca = 0
cx,cy,cz = 0,500,500
cd = math.sqrt(cx**2 + cy**2 + cz**2)
# camera_pos = (0,500,500)
camera_pos = (cd*math.sin(math.degrees(ca)),cd*math.cos(math.degrees(ca)),600)
# camera_pos =(-970.0, 707.1067811865476, 2382) 
camera_pos = (-500,000,700)



fovY = 120  # Field of view
GRID_LENGTH = 5000  # Length of grid lines
rand_var = 423
xi,yi,zi,rt = 0,0,0,0
brt = 0
bx,by,bz = xi,yi,120
bix,biy,biz = 0,0,00

lx,ly,lz = 0,0,0

bdx = 50*math.cos(math.radians(rt)) 
bdy = 50*math.sin(math.radians(rt)) 

class cbullet:
    def __init__(self,brt,bix,biy,biz):
        # ox,oy = GRID_LENGTH*8,-GRID_LENGTH*8
        ox,oy = 0,0

        self.brt = brt
        self.bix = bix +ox
        self.biy = biy +oy
        self.bdx = math.cos(math.radians(self.brt))
        self.bdy = math.sin(math.radians(self.brt))
        self.biz = biz+300
         
    def update_position(self):
        # if not pause

        self.bix += 10*self.bdx
        self.biy += 10*self.bdy


        # if self.x > rx or self.x < -rx:
        #     self.dx = -self.dx
        # if self.y > ry or self.y < -ry:
        #     self.dy = -self.dy
    # self.x ,self.y,self.rt = 
        # draw_bullet()
enemys = []


def obstacle():
    glPushMatrix()

    # gluSphere(gluNewQuadric(), 100, 10, 10)




    glPopMatrix() 





r1,r2 = random.randint(-200,200),random.randint(-200,200)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_bullet():
    global bdx,bdy, bullet_flag,brt, bullets,bix,biy,biz
    bdx += .5*math.cos(math.radians(brt)) 
    bdy += .5*math.sin(math.radians(brt)) 

    glPushMatrix()  # Save the current matrix state
    
    glColor3f(.5, 1, 1)
    # glTranslatef(bx,by,bz)
    for i in bullets:
        # glTranslatef(xi,yi, 00)
        glTranslatef(i.bix,i.biy,i.biz)
        glutSolidCube(60)
        glTranslatef(-i.bix,-i.biy,-i.biz)


    

    glTranslatef(bx,by,bz)
    glTranslatef(bdx,bdy,0)
    
    
    glutSolidCube(60)
    

    glPopMatrix() 
    bullet_flag = False


def draw_enemy():
    global enemys,xi,yi 

      # Save the current matrix state
    
    for i in enemys:
        glPushMatrix()
        glColor3f(1, 0, 0)
        glTranslatef( 0, 0, 100)

    
        glTranslatef( i[0], i[1], 0)
        print(i[-1])
        gluSphere(gluNewQuadric(), i[-1], 10, 10)  # parameters are: quadric, radius, slices, stacks
        glTranslatef( 0, 0, 150)

        glColor3f(0, 0, 0)
        gluSphere(gluNewQuadric(), 60, 10, 10)  

        glPopMatrix()  # Restore the previous matrix state




def draw_player():
    global xi,yi,rt, bullet_flag,cheat,brt,gameover,zi
    if not gameover:
        if cheat:
            rt+=1

        glPushMatrix() 
        
        glTranslatef(xi,yi, 100+zi)
        if zi>=0:
            zi -= .5
        glRotate(90,0,0,1)

        glRotatef(rt,0 , 0, 1) 


        glColor3f(1, 0, 0) #leg
        glTranslatef(60, 0, 100) 
        glRotatef(180, 1, 0, 0)  
        gluCylinder(gluNewQuadric(), 30, 20, 200, 10, 10)

        glTranslatef(-120, 0, 00) 

        gluCylinder(gluNewQuadric(), 30, 20, 200, 10, 10)

        glColor3f(1, 1, 0)
        glTranslatef(60, 0, -30)

        glRotatef(180, 1, 0, 0) 

        

        rbd,gbd,bbd = 1,1,0

        #bpody

        glTranslatef(30, 0, 00) 
        
        glColor3f(rbd,gbd,bbd)

        glutSolidCube(60)
        glTranslatef(0, 0, 60) 

        glutSolidCube(60)
        glTranslatef(0, 0, 60) 

        glutSolidCube(60)

        glTranslatef(-60, 0, 0)  #right 

        glutSolidCube(60)
        glTranslatef(0, 0, -60) #down

        glutSolidCube(60)
        glTranslatef(0, 0, -60) 

        glutSolidCube(60)
        glTranslatef(30, -30,120) 

        # hands and gun
        glColor3f(0, 1, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 20, 18, 150, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
        # bdx,bdy = 
        if bullet_flag:
            brt = rt
            draw_bullet()
            cbullet()

        glColor3f(0, 0, 1) 
        glTranslatef(60, 0, 0) 
        gluCylinder(gluNewQuadric(), 25, 10, 70, 10, 10)

        glTranslatef(-120, 0, 0) 
        gluCylinder(gluNewQuadric(), 25, 10, 70, 10, 10)


        glColor3f(1, 0, 0)#head
        glTranslatef(60, 50, 10) 

        gluSphere(gluNewQuadric(), 30, 10, 10)  # parameters are: quadric, radius, slices, stacks

        

        glPopMatrix()
      # Restore the previous matrix state
    else:
        glPushMatrix() 
        
        glTranslatef(xi,yi, 100)
        glRotate(90,0,0,1)
        glRotate(90,0,1,0)

        glRotatef(rt,0 , 0, 1) 


        glColor3f(1, 0, 0) #leg
        glTranslatef(60, 0, 100) 
        glRotatef(180, 1, 0, 0)  
        gluCylinder(gluNewQuadric(), 30, 10, 100, 10, 10)

        glTranslatef(-120, 0, 00) 

        gluCylinder(gluNewQuadric(), 30, 10, 100, 10, 10)

        glColor3f(1, 1, 0)
        glTranslatef(60, 0, -30)

        glRotatef(180, 1, 0, 0) 

        

        rbd,gbd,bbd = 1,1,0

        #bpody

        glTranslatef(30, 0, 00) 
        
        glColor3f(rbd,gbd,bbd)

        glutSolidCube(60)
        glTranslatef(0, 0, 60) 

        glutSolidCube(60)
        glTranslatef(0, 0, 60) 

        glutSolidCube(60)

        glTranslatef(-60, 0, 0)  #right 

        glutSolidCube(60)
        glTranslatef(0, 0, -60) #down

        glutSolidCube(60)
        glTranslatef(0, 0, -60) 

        glutSolidCube(60)
        glTranslatef(30, -30,120) 

        # hands and gun
        glColor3f(0, 1, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 20, 2, 150, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
        # bdx,bdy = 
        if bullet_flag:
            brt = rt
            draw_bullet()
            cbullet()

        glColor3f(0, 0, 1) 
        glTranslatef(60, 0, 0) 
        gluCylinder(gluNewQuadric(), 25, 10, 70, 10, 10)

        glTranslatef(-120, 0, 0) 
        gluCylinder(gluNewQuadric(), 25, 10, 70, 10, 10)


        glColor3f(1, 0, 0)#head
        glTranslatef(60, 50, 10) 

        gluSphere(gluNewQuadric(), 30, 10, 10)  # parameters are: quadric, radius, slices, stacks

        

        glPopMatrix()



def keyboardListener(key, x, y):
    global camera_pos, xi,yi,rt,cheat,bix,biy,vtog,enemys,gameover,zi
    # m = math.tan(math.degrees(rt))
    # print(m,'mm')

    x, y, z = camera_pos
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    # Move forward (W key) 
    if not gameover:
        if key == b'q':
            rt+=5
            rt = rt %360
        if key == b'e':
            rt-=5
            rt = rt %360
             
        if key == b' ':
            zi +=60
            # pass
            
        if key == b'w':   

            yi+= 25*math.sin(math.radians(rt)) 
            xi+= 25*math.cos(math.radians(rt)) 
            biy+= 25*math.sin(math.radians(rt)) 
            bix+= 25*math.cos(math.radians(rt)) 
            

        # Move backward (S key) 
        if key == b's': 
            yi-= 25*math.sin(math.radians(rt)) 
            xi-= 25*math.cos(math.radians(rt)) 
            biy-= 25*math.sin(math.radians(rt)) 
            bix-= 25*math.cos(math.radians(rt)) 
        for i in enemys:
            i[2],i[3] = xi,yi

        # # Rotate gun left (A key) 
        if key == b'a':
            yi+= 25*math.cos(math.radians(rt)) 
            xi-= 25*math.sin(math.radians(rt)) 
            biy+= 25*math.cos(math.radians(rt)) 
            bix-= 25*math.sin(math.radians(rt)) 
            

        # # Rotate gun right (D key) 
        if key == b'd':  # dash
            yi-= 25*math.cos(math.radians(rt)) 
            xi+= 25*math.sin(math.radians(rt)) 
            biy-= 25*math.cos(math.radians(rt)) 
            bix+= 25*math.sin(math.radians(rt)) 
        

        print(xi,yi,zi,rt)

        # # Toggle cheat mode (C key) 
        # if key == b'c':
        #     cheat = not cheat



        # # Toggle cheat vision (V key) 
        # if key == b'v':
        #     vtog = not vtog 

    # # Reset the game if R key is pressed
    if key == b'r':
        yi+= 250*math.sin(math.radians(rt)) 
        xi+= 250*math.cos(math.radians(rt)) 
        biy+= 250*math.sin(math.radians(rt)) 
        bix+= 250*math.cos(math.radians(rt))
        



def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos,rt
    x, y, z = camera_pos

    print(camera_pos,rt)
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        z+=50

    # # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        z-=50

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x-= 50
        # x -= 10*math.cos(math.radians(5))
        # y -= 10*math.sin(math.radians(5))  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x+= 50
        # x += 11*math.cos(math.radians(5))
        # y += 11*math.sin(math.radians(5)) # Small angle increment for smooth movement

    if key==GLUT_KEY_PAGE_UP:
       y-=50
        # draw_bullet()
        
    if key==GLUT_KEY_PAGE_DOWN:
        y+=50
    # print(camera_pos,rt)

    camera_pos = (x, y, z)

bullet_flag = False
def mouseListener(button, state, x, y):
    global bdx,bdy,bullet_flag,bullets,bix,biy,biz,rt,fps,gameover
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a bullet
    if not gameover:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            # bdy += 25*math.sin(math.radians(rt)) 
            # bdx += 25*math.cos(math.radians(rt)) 
            bullets.append(cbullet(rt,bix,biy,biz))
            # bullet_flag = True



            # # Right mouse button toggles camera tracking mode
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            fps = not fps


def setupCamera():
    global fps,xi,yi,GRID_LENGTH,rt,vtog

    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 15000) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    if fps :
        if vtog :
            x,y,z =   xi,yi ,100+400
            lx,ly,lz = 200+xi,yi,500
            
        else:

            x,y,z =   xi,yi ,100+400
            # lx,ly,lz = 20*math.cos(math.radians(rt)),20*math.sin(math.radians(rt)),0
            lx,ly,lz = 200*math.cos(math.radians(rt))+xi,200*math.sin(math.radians(rt))+yi,0
    else:
        x, y, z = camera_pos
        # x, y, z = xi,yi,500

    # Position the camera and set its orientation
        # lx,ly,lz = GRID_LENGTH*8,GRID_LENGTH*8,0

        lx,ly,lz = 0,0,0
        # lx,ly,lz = xi,yi,zi
    gluLookAt(x, y, z,  # Camera position
              lx,ly,lz,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)

# def dead_enemy():
#     global xi,yi
#     ex,ey = random.randint(-1000,1000),random.randint(-1000,1000)
#     disx = xi - ex 
#     disy = yi -ey
#     dis = math.sqrt((disx)**2 + (disy)**2)
#     # dex,dey = 
#     enemys.append((ex,ey,xi,yi,disx,disy,dis))

def idle():
    global rt,cheat,xi,yi,plife,zi,bix, biy
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # draw_bullet()

    # # this is for running automatic. commented this for easy coding and fixing

    # yi+= 2.5*math.sin(math.radians(rt)) 
    # xi+= 2.5*math.cos(math.radians(rt)) 
    # biy+= 2.5*math.sin(math.radians(rt)) 
    # bix+= 2.5*math.cos(math.radians(rt)) 
    if cheat:
        rt+=1
    for i in bullets:
        # glTranslatef(xi,yi, 00)
        i.update_position()

    
    for i in enemys:
        i[4] = i[2]-i[0]
        i[5] = i[3]-i[1]
        i[0] += .0001*i[4]
        i[1] += .0001*i[5]
        if i[4] ==0 and i[5] == 0:
            plife -=1

        s = 1
        if i[-1] >180:
            s = -.001
        if i[-1]<60:
            s = .001
        i[-1] += s
    # for i in range(len(bullets)):
    #     for j in range(len(enemys)):

    #         if (bullets[i].bix +30 <= enemys[j][0] or bullets[i].bix -30>= enemys[j][0] )and (bullets[i].biy +30 <= enemys[j][1] or bullets[i].biy -30>= enemys[j][1]):
    #             enemys.pop(j)
    #             bullets.pop()
        

    # draw_player()
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective
    # draw_player()
    

    # Draw a random points
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Draw the grid (game floor)
    glPushMatrix()
    glTranslatef(-10000, 100, 100) 
    # glTranslatef(-GRID_LENGTH*8,-GRID_LENGTH*8,0)
    for i in range(8):
        # glTranslatef(0,2*GRID_LENGTH, 00) 
        for j in range( 8):
            glTranslatef(2*GRID_LENGTH, 0, 00) 
            glBegin(GL_QUADS)
    
            glColor3f(.5, .5, .5)
            glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
            glVertex3f(0, GRID_LENGTH, 0)
            glVertex3f(0, 0, 0)
            glVertex3f(-GRID_LENGTH, 0, 0)

            # glPushMatrix()

            # # obstacle()

            # glPopMatrix()

            glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
            glVertex3f(0, -GRID_LENGTH, 0)
            glVertex3f(0, 0, 0)
            glVertex3f(GRID_LENGTH, 0, 0)

            # obstacle()


            glColor3f(.2,.2,.2)
            glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
            glVertex3f(-GRID_LENGTH, 0, 0)
            glVertex3f(0, 0, 0)
            glVertex3f(0, -GRID_LENGTH, 0)

            # obstacle()

            glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
            glVertex3f(GRID_LENGTH, 0, 0)
            glVertex3f(0, 0, 0)
            glVertex3f(0, GRID_LENGTH, 0)

            # obstacle()

            glEnd()
        # glTranslatef(-16*GRID_LENGTH, 0, 00) 
    


    glTranslatef(GRID_LENGTH*8,-GRID_LENGTH*8,0)
    glPopMatrix() 

    start = GRID_LENGTH*8,-GRID_LENGTH*8,0
    

    glPushMatrix() 
    # glTranslatef(GRID_LENGTH*8,-GRID_LENGTH*8,0)
    glRotate(90,0,0,0)
    for i in range(13):
        glBegin(GL_QUADS)
        glColor3f(0, 1, 0)
        glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
        glVertex3f(0, GRID_LENGTH, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(-GRID_LENGTH, 0, 0)
        glEnd()
        glTranslatef(0, -GRID_LENGTH, 00)
    # glTranslatef(GRID_LENGTH, GRID_LENGTH, 2*GRID_LENGTH)
    glRotatef(-90, 1, 0, 0)
    glTranslatef(GRID_LENGTH, GRID_LENGTH, 2*GRID_LENGTH)
    glRotatef(90, 0, 0, 1)
    glTranslatef(0,0, 2*GRID_LENGTH)
    for i in range(13):
        glBegin(GL_QUADS)
        glColor3f(0, 0, 1)
        glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
        glVertex3f(0, GRID_LENGTH, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(-GRID_LENGTH, 0, 0)
        glEnd()

        glTranslatef(GRID_LENGTH,0, 0)
    glPopMatrix() 


    # for i in range(16):
    #     # glTranslatef(2*GRID_LENGTH, 0, 00) 
    #     glColor3f(1, 0, 1)
    #     glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    #     glVertex3f(0, GRID_LENGTH, 0)
    #     glVertex3f(0, 0, 0)
    #     glVertex3f(-GRID_LENGTH, 0, 0)
    # # glRotate(-90,1,0,0)
    # glPopMatrix() 

    for i in bullets:
        glColor3f(1,0,0)#???
        # glBegin(GL_POINTS)
        glPushMatrix() 
        # glTranslatef(GRID_LENGTH*8,-GRID_LENGTH*8,0)
        # glTranslatef(i.bix, i.biy,i.biz) 
        
        glutSolidCube(10)
        # glEnd()
        glPopMatrix() 
            

    # glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    # boundary
    
    # glBegin(GL_QUADS)
    
    # glColor3f(.5, 1, .5)

    # glVertex3f(-1300, -1400,0)
    # glVertex3f(2000, -1400,0)
    # glVertex3f(2000, -1400,500)
    # glVertex3f(-1300, -1400,500)
    # # glEnd()
    # # glBegin(GL_QUADS)

    # glColor3f(1, .4, .7)   
    # glVertex3f(-1300, -1400,0)
    # glVertex3f(-1300, 1800,0)
    # glVertex3f(-1300, 1800,500)
    # glVertex3f(-1300, -1400,500)

    # glColor3f(.5, 1, .5)
    # glVertex3f(-1300, 1800,00)
    # glVertex3f(2000, 1800,00)
    # glVertex3f(2000, 1800,500)
    # glVertex3f(-1300, 1800, 500)

    # glColor3f(1, .4, .7) 
    # glVertex3f(2000, 1800,00)
    # glVertex3f(2000, -1400,0)
    # glVertex3f(2000, -1400,500)
    # glVertex3f(2000, 1800,500)
    


    # glVertex3f(-1300, -1400,500)
    
    # glVertex3f(-1400, -1400,500)
    
    # glVertex3f(0, 0, 0)
    # glVertex3f(-GRID_LENGTH, 0, 0)

    # glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    # glVertex3f(0, -GRID_LENGTH, 0)
    # glVertex3f(0, 0, 0)
    # glVertex3f(GRID_LENGTH, 0, 0)
    # glEnd()


    # glColor3f(0.7, 0.5, 0.95)
    # glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    # glVertex3f(-GRID_LENGTH, 0, 0)
    # glVertex3f(0, 0, 0)
    # glVertex3f(0, -GRID_LENGTH, 0)

    # glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    # glVertex3f(GRID_LENGTH, 0, 0)
    # glVertex3f(0, 0, 0)
    # glVertex3f(0, GRID_LENGTH, 0)
    # glEnd()
    # glRotatef(90, 1, 0, 0)
    # glRotatef(90, 0, 1, 0)

    # for i in range(13):
    #     glBegin(GL_QUADS)
    #     glColor3f(0, 0, 1)
    #     glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    #     glVertex3f(0, GRID_LENGTH, 0)
    #     glVertex3f(0, 0, 0)
    #     glVertex3f(-GRID_LENGTH, 0, 0)
    #     glEnd()
    #     glTranslatef(0,-GRID_LENGTH, 00)

   

    draw_player()
    draw_bullet()
    # if len(enemys) <5:
    #     print(len(enemys))
    #     dead_enemy()
    #     print('enemy created')


    # Display game info text at a fixed screen position
    draw_text(10, 770, f"Player life remaining : { plife}")
    draw_text(10, 740, f"Game Score: {score}")
    draw_text(10, 710, f"Player bullet miss: {bmiss}")

    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D bullet frenzy")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
