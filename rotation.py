# -*- coding: utf-8 -*-
# OpenGL Projections 
#---------------------------------
from pyglet import window,image
import pyglet
from pyglet.window import key
from pyglet.gl import *
import numpy as np
import scipy.io as sio
from ICP_for_openGL import ICP

def opengl_init():
    glEnable(GL_BLEND)
    glEnable(GL_PROGRAM_POINT_SIZE)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthFunc(GL_LEQUAL)

def your_test_code():
    pass

class camera():
    x,y,z=0,0,512
    rx,ry,rz=30,-45,0
    w,h=640,480
    far=8192
    fov=60
    def __init__(self,mode):
        self.mode = mode
          
    def view1(self,width,height):
        self.w,self.h=width,height
        self.w,self.h=width,height
        glViewport(0, 0, width, height)
        print "Viewport "+str(width)+"x"+str(height)
        if self.mode==2: self.isometric()
        elif self.mode==3: self.perspective()
        else: self.default()
        
    def view2(self,width,height):
        self.w,self.h=width,height
        glViewport(0, 0, width, height)
        print "Viewport "+str(width)+"x"+str(height)
        if self.mode==2: self.isometric()
        elif self.mode==3: self.perspective()
        else: self.default()
            
    def default(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.w/2, self.w/2, -self.h/2, self.h/2, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        
    def isometric(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glScalef(1,1,1)
        glOrtho(-self.w/2.,self.w/2.,-self.h/2.,self.h/2.,0,self.far)
        glMatrixMode(GL_MODELVIEW)
        
    def perspective(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glScalef(1,1,1)
        gluPerspective(self.fov, float(self.w)/self.h, 0.1, self.far)
        glMatrixMode(GL_MODELVIEW)
        
    def key(self, symbol, modifiers):
        if symbol==key.F1:
            self.mode=1
            self.default()
            print "Projection: Pyglet default" 
        elif symbol==key.F2: 
            print "Projection: 3D Isometric" 
            self.mode=2
            self.isometric()
        elif symbol==key.F3:
            print "Projection: 3D Perspective" 
            self.mode=3
            self.perspective()
        elif self.mode==3 and symbol==key.MINUS:
            self.fov-=1
            self.perspective()
        elif self.mode==3 and symbol==key.EQUAL:
            self.fov+=1
            self.perspective()
        else: print "KEY "+key.symbol_string(symbol)
        
    def drag(self, x, y, dx, dy, button, modifiers):
        if button==1:
            self.x-=dx*2
            self.y-=dy*2
        elif button==2:
            self.x-=dx*2
            self.z-=dy*2
        elif button==4:
            self.ry+=dx/4.
            self.rx-=dy/4.
        
    def apply(self):
        glLoadIdentity()
        if self.mode==1: return
        glTranslatef(-self.x,-self.y,-self.z)
        glRotatef(self.rx,1,0,0)
        glRotatef(self.ry,0,1,0)
        glRotatef(self.rz,0,0,1)     

######################### three axis ###############################
def x_array(list):
    return (GLfloat * len(list))(*list)
        
def axis(d=100):
    vertices,colors=[],[]    
    #XZ RED  
    vertices.extend([-d+d, 0,-d+d, d+d, 0,-d+d, d+d, 0, d+d,-d+d, 0, d+d])# traslate distance 'd'
    for i in range (0,4): colors.extend([1,0,0,1])
    #YZ GREEN  
    vertices.extend([ 0,-d+d,-d+d, 0,-d+d, d+d, 0, d+d, d+d, 0, d+d,-d+d])
    for i in range (0,4): colors.extend([0,1,0,1])
    #XY BLUE  
    vertices.extend([-d+d,-d+d, 0, d+d,-d+d, 0, d+d, d+d, 0,-d+d, d+d, 0])
    for i in range (0,4): colors.extend([0,0,1,1])
    return x_array(vertices),x_array(colors)
    
AXIS_VERTICES, AXIS_COLORS=axis()

def box(d,point,color):
    vertices,colors=[],[]  
    #XZ RED  
    print "there are: "+ str(point.shape[0]) + " harris points imported!"
    
    color1 = [0,1,0,0.9] # green window
    color2 = [0,0,1,0.9] # blue window
    
    for i in range(point.shape[0]):
        vertices.extend([point[i][0]-d, point[i][1]-d,point[i][2]-d, point[i][0]+d, point[i][1]-d,point[i][2]-d, point[i][0]+d, point[i][1]-d, point[i][2]+d,point[i][0]-d, point[i][1]-d, point[i][2]+d])# "left plane", traslate distance 'd'
        if color[0][i] == 1:
            for ic in range (0,4): colors.extend(color2) 
        else:
            for ic in range (0,4): colors.extend(color1) 
        
        vertices.extend([point[i][0]-d, point[i][1]+d,point[i][2]-d, point[i][0]+d, point[i][1]+d,point[i][2]-d, point[i][0]+d, point[i][1]+d, point[i][2]+d,point[i][0]-d, point[i][1]+d, point[i][2]+d])# "right plane"
        if color[0][i] == 1:
            for ic in range (0,4): colors.extend(color2)
        else:
            for ic in range (0,4): colors.extend(color1) 
        #YZ GREEN  
        vertices.extend([point[i][0]-d,point[i][1]-d,point[i][2]-d, point[i][0]-d,point[i][1]-d, point[i][2]+d, point[i][0]-d, point[i][1]+d, point[i][2]+d, point[i][0]-d, point[i][1]+d,point[i][2]-d])
        if color[0][i] == 1:
            for ic in range (0,4): colors.extend(color2)
        else:
            for ic in range (0,4): colors.extend(color1)
        vertices.extend([point[i][0]+d,point[i][1]-d,point[i][2]-d, point[i][0]+d,point[i][1]-d, point[i][2]+d, point[i][0]+d, point[i][1]+d, point[i][2]+d, point[i][0]+d, point[i][1]+d,point[i][2]-d])
        if color[0][i] == 1:
            for ic in range (0,4): colors.extend(color2)
        else:
            for ic in range (0,4): colors.extend(color1)
        #XY BLUE  
        vertices.extend([point[i][0]-d,point[i][1]-d, point[i][2]-d, point[i][0]+d,point[i][1]-d,point[i][2]-d, point[i][0]+d, point[i][1]+d, point[i][2]-d,point[i][0]-d, point[i][1]+d, point[i][2]-d])
        if color[0][i] == 1:
            for ic in range (0,4): colors.extend(color2)
        else:
            for ic in range (0,4): colors.extend(color1)
        vertices.extend([point[i][0]-d,point[i][1]-d, point[i][2]+d, point[i][0]+d,point[i][1]-d,point[i][2]+d, point[i][0]+d, point[i][1]+d, point[i][2]+d,point[i][0]-d, point[i][1]+d, point[i][2]+d])
        if color[0][i] == 1:
            for ic in range (0,4): colors.extend(color2)
        else:
            for ic in range (0,4): colors.extend(color1)
    
    return x_array(vertices),x_array(colors)
        
mat_contents = sio.loadmat('/Users/junchaowei/Desktop/OpenGL_Connection/harris_nodes_reshape.mat')
mat_contents0 = sio.loadmat('/Users/junchaowei/Desktop/OpenGL_Connection/harris_nodes_reshape_color.mat')
harris_nodes = mat_contents['p']
harris_nodes_color = mat_contents0['c']
BOX_VERTICES, BOX_COLORS=box(5,harris_nodes,harris_nodes_color)

def draw_vertex_array(vertices,colors,mode=GL_LINES):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glColorPointer(4, GL_FLOAT, 0, colors)
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glDrawArrays(GL_QUADS, 0, len(vertices)/3)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)

def draw_axis():
    glEnable(GL_DEPTH_TEST)
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  
    draw_vertex_array(AXIS_VERTICES,AXIS_COLORS,GL_QUADS)
    #draw_vertex_array(BOX_VERTICES,BOX_COLORS,GL_QUADS) ########## draw the boxes ###########
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) 
    #glDisable(GL_DEPTH_TEST)
    
    
#########################   3D Camera Winodws    ###############################
cam=camera(2)
win = window.Window(1200, 800, resizable=False)
win.set_caption('Isometric View') 
win.on_resize=cam.view1 #overwrite the method in window.
win.on_key_press=cam.key
win.on_mouse_drag=cam.drag

win.set_location(0,0)
opengl_init()

#def input_data(vertices,indices)            
batch = pyglet.graphics.Batch()

import scipy.io as sio
                                              
#mat_contents2 = sio.loadmat('/Users/junchaowei/Desktop/OpenGL Python/elements.mat')
#elements = mat_contents2['elements']
#mat_contents3 = sio.loadmat('/Users/junchaowei/Desktop/OpenGL Python/points.mat')
#points = mat_contents3['points']

mat_contents2 = sio.loadmat('/Users/junchaowei/Desktop/OpenGL_Connection/surface2.mat')
elements = mat_contents2['par1']
mat_contents3 = sio.loadmat('/Users/junchaowei/Desktop/OpenGL_Connection/point.mat')
points = mat_contents3['par1'].T

vertices = list(np.reshape(points.T,np.size(points.T), order='C'))
        #indices = [0,1,2,0,2,3,0,3,1,1,2,3]	   
        
##############################################################################
        
indices = list(np.reshape(elements, np.size(elements), order = 'C')) 

color_array = (255*np.random.rand(points.T.shape[0], 3)).astype(int) 

color_array = np.ones((points.T.shape[0],3))*0
color_array[:,0] = 255

int_color_array = color_array.astype(int)

colors = list(np.reshape(int_color_array, np.size(int_color_array), order = 'C')) 

vertex_list = batch.add_indexed(np.size(vertices)/3, 
                                        GL_TRIANGLES,
                                        None,
                                        indices,
                                        ('v3f/static', vertices),
                                        ('c3B/static', colors))
                                        
#vertex_list = batch.add_indexed(np.size(vertices)/3, 
#                                        GL_POINTS,
#                                        None,
#                                        indices,
#                                        ('v3f/static', vertices),
#                                        ('c3B/static', colors)) 
                                        

#vertex_list = batch.add(np.size(svd2)/3, GL_POINTS, None,
#                                ('v3f/static', svd1),
#                                ('c3B', colors1))  
                                
#vertex_list = batch.add(np.size(svd1)/3, GL_POINTS, None,
#                                ('v3f/static', svd2),
#                                ('c3B', colors2)) 
                                
                                
#vertex_list = batch.add(np.size(svd3)/3, GL_LINES, None,
#                                ('v3f/static', svd3),
#                                ('c3B', colors3))                                                                                                

                                                                                                                                                                                                                                                                                                                                                   
def vec(*args):
    return (GLfloat * len(args))(*args)

def axisArrow(d): 
    glLineWidth(4) # set the line width for axis lines
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    ##### x axis #####
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(d, 0, 0)
    glVertex3f(d, 0, 0)
    glVertex3f(d-10, -10, 0)
    glVertex3f(d-10, -10, 0)
    glVertex3f(d-10, 10, 0)
    glVertex3f(d-10, 10, 0)
    glVertex3f(d, 0, 0)
    ##### y axis #####
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0, d, 0)
    glVertex3f(0, d, 0)
    glVertex3f(0, d-10, -10)
    glVertex3f(0, d-10, -10)
    glVertex3f(0, d-10, 10)
    glVertex3f(0, d-10, 10)
    glVertex3f(0, d, 0)
    ##### z axis #####
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0, 0, d)
    glVertex3f(0, 0, d)
    glVertex3f( -10, 0, d-10)
    glVertex3f( -10, 0, d-10)
    glVertex3f(  10, 0, d-10)
    glVertex3f(  10, 0, d-10)
    glVertex3f(   0, 0, d)
    glColor4f(1.0, 1.0, 1.0, 0.5) # this setup the color for the texture picture also.
    glEnd()   
    glLineWidth(0.1)
    
textures = []
img_dir = "/Users/junchaowei/Desktop/Python_DVC2/UP_Research/WholeRegionRealData/JunchaoFirstRun/M6_OD/M6_OD_125_C-scan/052.tif"
image = pyglet.image.load(img_dir)
            
textures.append(image.get_texture())

glEnable(textures[-1].target)
glBindTexture(textures[-1].target, textures[-1].id)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height,
                         0, GL_RGBA, GL_UNSIGNED_BYTE,
                         image.get_image_data().get_data('RGBA',
                                                         image.width * 4))  
rotation = 0 # global variable for updating the rotation

def update(dt):
    global rotation
    rotation+=1
    
def get_modelview_mat(local_transform):
        mvmat = (GLdouble * 16)()
        glGetDoublev(GL_MODELVIEW_MATRIX, mvmat)
        return mvmat
  
def mouse_to_3d(x, y, z = 1.0, local_transform = False):
        x = float(x)
        y = float(y) #window height = 800
        # The following could work if we were not initially scaling to zoom on
        # the bed
        # if self.orthographic:
        #    return (x - self.width / 2, y - self.height / 2, 0)
        pmat = (GLdouble * 16)()
        mvmat = get_modelview_mat(local_transform)
        viewport = (GLint * 4)()
        px = (GLdouble)()
        py = (GLdouble)()
        pz = (GLdouble)()
        glGetIntegerv(GL_VIEWPORT, viewport)
        glGetDoublev(GL_PROJECTION_MATRIX, pmat)
        glGetDoublev(GL_MODELVIEW_MATRIX, mvmat)
        gluUnProject(x, y, z, mvmat, pmat, viewport, px, py, pz)
        print z,pz
        return (px.value, py.value, pz.value)    
        
def mouse_to_ray(x, y, local_transform = False):
        x = float(x)
        y = float(y)
        pmat = (GLdouble * 16)()
        mvmat = (GLdouble * 16)()
        viewport = (GLint * 4)()
        px = (GLdouble)()
        py = (GLdouble)()
        pz = (GLdouble)()
        glGetIntegerv(GL_VIEWPORT, viewport)
        glGetDoublev(GL_PROJECTION_MATRIX, pmat)
        mvmat = get_modelview_mat(local_transform)
        gluUnProject(x, y, 1, mvmat, pmat, viewport, px, py, pz)
        ray_far = (px.value, py.value, pz.value)
        gluUnProject(x, y, 0., mvmat, pmat, viewport, px, py, pz)
        ray_near = (px.value, py.value, pz.value)
        return ray_near, ray_far
        
def mouse_to_plane(x, y, plane_normal, plane_offset, local_transform = False):
        # Ray/plane intersection
        ray_near, ray_far = mouse_to_ray(x, y, local_transform)
        ray_near = np.array(ray_near)
        ray_far = np.array(ray_far)
        ray_dir = ray_far - ray_near
        ray_dir = ray_dir / np.linalg.norm(ray_dir)
        plane_normal = np.array(plane_normal)
        q = ray_dir.dot(plane_normal)
        #print ray_dir,plane_normal,q
        if q == 0:
            return None
        t = - (ray_near.dot(plane_normal) + plane_offset) / q
        #print t
        #if t < 0:
        #    return None
        return ray_near + t * ray_dir
        
location = (0.0,0.0,0.0)                                                                                                                                                                                                                        
@win.event                                                
def on_draw():                                                                                                                                                                                                                                                                                                                                               
    #win.switch_to()
    #win.dispatch_events()
    #win.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0) 
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST) 
    cam.apply()
    glPointSize(10)
    glLineWidth(2.5)
    glEnable(GL_POINT_SMOOTH)
    draw_axis()
    glBegin(GL_POINTS)
    glColor3f(1.0,0.0,0.0)
    glVertex3f(location[0],location[1],location[2])
    glEnd()
    
    glBegin(GL_TRIANGLES) #start drawing triangles
    glColor3f(1.0,1.0,0.0) # color
    glVertex3f(100.0, 0.0, 0.0) #triangle one first vertex
    glVertex3f(0, 100.0, 0.0)   #triangle one second vertex
    glVertex3f(0, 0.0, 100)     #triangle one third vertex
    glEnd()                      #end drawing of triangles
    
    axisArrow(400)
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) # using the triangle wireframe, default is GL_FILL
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)    
    batch.draw()  # drawing the objects
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)   
    #glRotatef(rotation,0, 0, 1) 
    lightZeroPosition = vec(20.,20.,0, 1) # homogeneous coordinator
    lightZeroColor = vec(0.43,0.72,0.82,1) #green tinged
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.02)
    glEnable(GL_LIGHT0)
    #0.49, 0.49, 0.22
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(0.49, 0.49, 0.22, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 20)
    
    ##############  to put 2D texture in the scene ##########
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D) 
    glLoadIdentity()   
    glActiveTexture(GL_TEXTURE0)                                                                                                                              
    glPushMatrix()
    glTranslatef(300, 200, 0)                  
    glBindTexture(textures[0].target, textures[0].id)
    glBegin(GL_QUADS)
    d = image.height/8
    glTexCoord2f(0.0, 0.0); glVertex3f(-d, -d/2, 0.0)
    glTexCoord2f(1.0, 0.0); glVertex3f( d, -d/2, 0.0)
    glTexCoord2f(1.0, 1.0); glVertex3f( d,  d/2, 0.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-d,  d/2, 0.0)
    glEnd()
    glPopMatrix() 


@win.event      
def on_mouse_press(x, y, button, modifiers):
    global location
    print "mouse location is: "+ str(x) + " " + str(y)
    print "ray0" + str(mouse_to_ray(x,y)[0])
    print "ray1" + str(mouse_to_ray(x,y)[1])
    plane = (0, 0, -1)
    d = 0.0
    location = mouse_to_plane(x,y,plane,d)
    print "plane contact point is: " + str(location)
    I = [] 
    def intersect3D_RayTriangle(ray1,ray0,v0,v1,v2):
        global location
        global I # intersection point
        # Return: -1 = triangle is degenerate (a segment or point)
        #          0 =  disjoint (no intersect)
        #          1 =  intersect in unique point I1
        #          2 =  are in the same plane
        v0 = np.array(v0) # converting the tuple into a numpy array
        v1 = np.array(v1)
        v2 = np.array(v2)
        ray1 = np.array(ray1)
        ray0 = np.array(ray0)
        
        u = v1 - v0 # triangle edge vectors
        v = v2 - v0
        
        n = np.cross(u,v) # plane norm
        if (sum(n)==0):
            return -1 # the triangle is degenerate, zero area.
        
        Dir = ray0 - ray1 # ray direction
        w0 = ray0 - v0
        a = -np.dot(n,w0)
        b = np.dot(n,Dir)
        if (abs(b) < 0.001): # ray is  parallel to triangle plane
            if (a == 0):
                return 2  # ray lies in triangle plane
            else:
                return 0  # ray disjoint from plane
            
        # get intersect point of ray with triangle plane
        r = a / b
        print "the r is:" + str(r)
        if (r < 0.0):  # ray goes away from triangle
            return 0  # => no intersect
            
        I = ray0 + r*Dir   # intersect point of ray and plane
        # is I inside T:
        # references: http://geomalgorithms.com/a06-_intersect-2.html#intersect3D_RayTriangle()
        uu = np.dot(u,u)
        uv = np.dot(u,v)
        vv = np.dot(v,v)
        w = I - v0
        wu = np.dot(w,u)
        wv = np.dot(w,v)
        D = uv*uv - uu*vv
        s = (uv * wv - vv * wu) / D   
        if (s < 0.0 or s > 1.0):  # I is outside T  
            return 0 
        t = (uv * wu - uu * wv) / D
        if (t < 0.0 or (s + t) > 1.0): # I is outside T
            return 0 
        location = I # update the location of point
        print "intersection point: " + str(I)    
        return 1
        
    v0 = (100, 0, 0)
    v1 = (0, 100, 0)
    v2 = (0, 0, 100)
        
    print intersect3D_RayTriangle(mouse_to_ray(x,y)[1], mouse_to_ray(x,y)[0],v0,v1,v2)
    
#pyglet.clock.schedule(update)    
pyglet.app.run()

