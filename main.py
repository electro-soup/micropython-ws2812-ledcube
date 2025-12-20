import urandom
import time
import math
from machine import Pin
import neoSPI

SPI_ID = 1 # MOSI - #11 on ESP32-S3
NUM_LEDS = 300
BRIGHTNESS = 0.1
FRAMES = 256  

np = neoSPI.NeoPixel(SPI_ID, NUM_LEDS)




def sparkle(duration=3, wait=0.05):
    end_time = time.ticks_add(time.ticks_ms(), int(duration * 1000))
    while time.ticks_diff(end_time, time.ticks_ms()) > 0:
        i = urandom.getrandbits(16) % NUM_LEDS
        set_pixel(i, (255, 255, 255))
        np.write()
        time.sleep(wait)
        set_pixel(i, (0, 0, 0))
        np.write()

def clear():
    np.viper_blank()
    np.write()

def demo():
    while True:
        rainbow_cycle()
        clear()
        theater_chase((255, 0, 0))
        clear()
        breathing((0, 0, 255))
        clear()
        running_light((0, 255, 0))
        clear()
        sparkle()
        clear()


def random_color():
    return (urandom.randrange(0,10,1), urandom.randrange(0,10,1),urandom.randrange(0,10,1))

def snake(color, num_pixels, time_s):
    for i in range(num_pixels - 20): #time consuming, needs opts if largers arrays
        np.fill((0,0,0))   
        np[i]=color
        np[i + 20] = color
        np.write()
        time.sleep(time_s)
        
    for i in range(num_pixels-1, 20, -1): #time consuming, needs opts if largers arrays
        np.fill((0,0,0))   
        np[i]=color
        np[i - 20] = color
        np.write()
        time.sleep(time_s)

def snake_SPI(color, num_pixels, time_s):
    _data_len =  np.n*12
    for i in range(num_pixels - 20): #time consuming, needs opts if largers arrays
        
        start = time.ticks_ms()
        #np[:num_pixels] = (0,0,0)
        #for j in range(num_pixels*12):
        #    np._data[j] = 136
        np.viper_blank()
        np[i]=color
        np[i + 20] = color
        
        np.write()
        time_msec = time.ticks_diff( time.ticks_ms(), start)
        print(f"MeasureTime {time_msec} msec")
        time.sleep(time_s)
        
    for i in range(num_pixels-1, 20, -1): #time consuming, needs opts if largers arrays
        start = time.ticks_ms()
        np[:num_pixels] = (0,0,0)  
        np[i]=color
        np[i - 20] = color
        np.write()
        time.sleep(time_s)
        time_msec = time.ticks_diff( time.ticks_ms(), start)
        print(f"MeasureTime {time_msec} msec")
        time.sleep(time_s)
        

def snakes_split(time_s, snake_length):
    color_1 = (0,5,5)
    color_2 = (5,5,0)
    color_3 = (5,0,0)
    color_4 = (0,5,0)
    #snake_length = 10
    for pos in range(1000):  
        np[(500 + pos):( 500 +pos+snake_length)] = color_1
        np[(500 - pos - snake_length): (500 - pos)] = color_2
        if (pos + snake_length) > 10:
             np[(500 + pos - 10):( 500 +pos+snake_length - 10)] = color_3
             np[(500 - pos - snake_length + 10): (500 - pos + 10)] = color_4
        if (pos + snake_length) > 25:
             np[(500 + pos - 25):( 500 +pos+snake_length - 25)] = random_color()
             np[(500 - pos - snake_length + 25): (500 - pos + 25)] = random_color()
        np.write()
        time.sleep(time_s)
        np.viper_blank()
     
@micropython.viper
def check_light_strain(time_s = 0.5, additional_lights = 0):
    color_1 = random_color()
    color_2 = random_color()
    color_3 = random_color()
    for i in range(216):
        color_table = [(0,0,0) for _ in range(4*54)]
        color_table[i] = (5,5,5)
        if additional_lights:
            color_table[i+20] = color_1
            color_table[i+40] = color_2
            color_table[i+60] = color_3
        write_3D_data(color_table)
        np.write()
        time.sleep(time_s)
        #print(i)
    clear()

@micropython.viper
def check_light_strain_mv(time_s = 0.5, additional_lights = 0):
    data = array.array('B', [0 for i in range(4*54*3)])
    for i in range(216):
        data = array.array('B', [0 for i in range(4*54*3)])
        data[3*i] = i
        data[3*i+1] = i+1
        data[3*i+2] = 3*i+2
        write_3D_data_mv(data)
        np.write()
        time.sleep(time_s)
        #print(i)
    clear()

def iterate_as_matrix(xyz_coords, color_value, data:memoryview, blank = 0):
    #data = [(0,0,0) for _ in range(4*54)]
    X_ax = 9
    Y_ax = 6
    Z_ax = 4
    x, y, z = xyz_coords
    pos = x + y * X_ax + z * X_ax * Y_ax 
    data[pos] = color_value
    if blank == 1:
        np.viper_blank()

#it need to be faster
@micropython.viper
def iterate_as_matrix_mv(x:int, y:int, z:int, r:int,g:int,b:int, data:ptr8, blank:int):
    #data = [(0,0,0) for _ in range(4*54)]
    data_pos: int = 0
    X_ax = 9
    Y_ax = 6
    Z_ax = 4
    pos = x + y * X_ax + z * X_ax * Y_ax
    data_pos = int(pos) * 3
    data[data_pos] = r
    data[data_pos+1] = g
    data[data_pos+2] = b
    if blank == 1:
        np.viper_blank()
    
def clear_buffer(data):
    data = [(0,0,0) for _ in range(4*54)]

def demo_3D():
    color_table = [(0,0,0) for _ in range(4*54)]
    for x in range(8,-1,-1):
       for y in range(5,-1, -1):
           for z in range(3,-1, -1):
            iterate_as_matrix((x,y,z), (x*y+3, y*y*4+2, y*z*10), color_table)
            write_3D_data(color_table)
            np.write()

import array

def demo_3D_mv():
    data = array.array('B', [0 for i in range(4*54*3)])
    dd = memoryview(data)
    for x in range(8,-1,-1):
       for y in range(5,-1, -1):
           for z in range(3,-1, -1):
                iterate_as_matrix_mv(x,y,z, x*y+3, y*y*4+2, y*z*10, dd,0) #50us
                write_3D_data_mv(dd)
                np.write()
    # for x in range(8,-1,-1):
    #    for y in range(5,-1, -1):
    #        for z in range(3,-1, -1):
    #         iterate_as_matrix_mv(x,y,z, 0, 0 ,0, dd,0)
    #         write_3D_data_mv(dd)
    #         np.write()
        

def demo_viper_fill():
    while True:
        np.fill(0,1,1)
        np.write()
        np.fill(1,0,1)
        np.write()
        np.fill(1,0,0)
        np.write()
        np.fill(0,1,0)
        np.write()
        np.fill(0,0,1)
        np.write()

#very naive function for filling 9x6x4 matrix
#memoryview version
def write_2D_slice_mv(start, data:memoryview):
    line_width = 9
    data_it = 0
    #print(f'entry {start=}')
    for i in range(0,6,2):
        end = start+line_width
        for rgb in range(start, end):
            #print(rgb)
            np.viper_set_pixel(rgb, data[data_it], data[data_it+1], data[data_it+2]) 
            data_it +=3
                    #now reverse order
        start = end + 1 # 1 for empty led
        end = start + line_width
        for rgb in range(end-1, start-1, -1):
            #print(rgb)
            np.viper_set_pixel(rgb, data[data_it], data[data_it+1], data[data_it+2])
            data_it +=3 
        start = end + 1
    #print(f'{start=}')
    return start
#for even slices
def write_2D_slice_mv_2(start:int, data:memoryview):
    line_width = 9
    data_it = len(data) - 3
    #print(f'entry {start=}')
    for i in range(0,6,2):
        end = start+line_width
        for rgb in range(end-1, start-1, -1):
            #print(rgb)
            np.viper_set_pixel(rgb, data[data_it], data[data_it+1], data[data_it+2]) 
            data_it -=3
                    #now reverse order
        start = end + 1 # 1 for empty led
        end = start + line_width
        for rgb in range(start, end):
            #print(rgb)
            np.viper_set_pixel(rgb, data[data_it], data[data_it+1], data[data_it+2])
            data_it -=3 
        start = end + 1
    #print(f'{start=}')
    return start

def write_3D_data_mv(data:memoryview):
    start = 24
    end = 0
    #  first strand transformation - 6 rows (or vertical columns)
    data_temp = memoryview(data[0:162])
    end = write_2D_slice_mv(start, data_temp)
    start = end + 2
    #reverse part of array for second 2d slice:
    data_temp = memoryview(data[162:324])
    #second slice 
    end = write_2D_slice_mv_2(start, data_temp) #2ms
    start = end + 2
    # 3th slice
    data_temp = memoryview(data[324:486])
    end = write_2D_slice_mv(start, data_temp)
    start = end + 1
    #and the same as #2
    # 4th slice
    data_temp = memoryview(data[486:648])
    end = write_2D_slice_mv_2(start, data_temp)

def test_iterate_mv(point):
        data = array.array('B', [0 for i in range(4*54*3)])
        iterate_as_matrix_mv(0,0,0, 5,5,5, data,0)
        write_3D_data_mv(data)
        np.write()


class MeasureTime:
    def __init__(self, title ):
        self.title = title
    def __enter__( self ):
        self.t0 = time.ticks_us()
        return self
    def __exit__( self, exc_type, exc_val, exc_traceback ):
        self.time_usec = time.ticks_diff( time.ticks_us(), self.t0 )
        print(f"\tMeasureTime {self.title} {self.time_usec} usec" )

mapper_data_to_pos = array.array('h', [25, 26, 27, 28, 29, 30, 31, 32, 33, 43, 42, 41, 40, 39, 38, 37, 36, 35, 45, 46, 47, 48, 49, 50, 51, 52, 53, 63, 62, 61, 60, 59, 58, 57, 56, 55, 65, 66, 67, 68, 69, 70, 71, 72, 73, 83, 82, 81, 80, 79, 78, 77, 76, 75, 145, 144, 143, 142, 141, 140, 139, 138, 137, 127, 128, 129, 130, 131, 132, 133, 134, 135, 125, 124, 123, 122, 121, 120, 119, 118, 117, 107, 108, 109, 110, 111, 112, 113, 114, 115, 105, 104, 103, 102, 101, 100, 99, 98, 97, 87, 88, 89, 90, 91, 92, 93, 94, 95, 149, 150, 151, 152, 153, 154, 155, 156, 157, 167, 166, 165, 164, 163, 162, 161, 160, 159, 169, 170, 171, 172, 173, 174, 175, 176, 177, 187, 186, 185, 184, 183, 182, 181, 180, 179, 189, 190, 191, 192, 193, 194, 195, 196, 197, 207, 206, 205, 204, 203, 202, 201, 200, 199, 268, 267, 266, 265, 264, 263, 262, 261, 260, 250, 251, 252, 253, 254, 255, 256, 257, 258, 248, 247, 246, 245, 244, 243, 242, 241, 240, 230, 231, 232, 233, 234, 235, 236, 237, 238, 228, 227, 226, 225, 224, 223, 222, 221, 220, 210, 211, 212, 213, 214, 215, 216, 217, 218])
@micropython.viper
def iterate_as_matrix_viper(x:int, y:int, z:int, r:int,g:int,b:int, np_data:ptr16):
    #first slice
    X_ax = 9
    Y_ax = 6
    Z_ax = 4
    diode_index = 0
    pos = x + y * X_ax + z * X_ax * Y_ax  
    diode_index = np_data[pos]
    np.viper_set_pixel(diode_index, r, g, b) 

@micropython.viper
def demo_3D_viper():
    #data = array.array('B', [0 for i in range(4*54*3)])
    np.fill(0,0,0)
    mapper = ptr16(mapper_data_to_pos)
    for x in range(8,-1,-1):
       for y in range(5,-1, -1):
           for z in range(3,-1, -1):
                iterate_as_matrix_viper(x,y,z,  x*y+3, y*y*4+2, y*z*10, mapper) #50us
                np.write() #it increased time mostly 9ms at 1000 diodes

@micropython.viper
def demo_bouncing_rectangle(time_s, range):
    mapper = ptr16(mapper_data_to_pos)
    while True:
        r = urandom.randrange(0,range,1)
        g = urandom.randrange(0,range,1)
        b = urandom.randrange(0,range,1)
        r2 = urandom.randrange(0,range,1)
        g2 = urandom.randrange(0,range,1)
        b2 = urandom.randrange(0,range,1)
        for x in range(9):
            np.fill(0,0,0)
            for y in range(6):
                iterate_as_matrix_viper(x, y,0, r,g,b, mapper) #6 diodes long side
                iterate_as_matrix_viper(x, y,3,r,g,b,mapper)
                #completely opposite rectangle inside
                if y > 0 and y < 5:
                    iterate_as_matrix_viper(8-x, y,1, r2,g2,b2, mapper) #6 diodes long side
                    iterate_as_matrix_viper(8-x, y,2,r2,g2,b2,mapper)    
            for z in range(4):
                iterate_as_matrix_viper(x,0,z,r,g,b,mapper) #4 diodes along z
                iterate_as_matrix_viper(x, 5, z,r,g,b,mapper)
            np.write()
            time.sleep(time_s)
        for x in range(8, -1, -1):
            np.fill(0,0,0)
            for y in range(5,-1,-1):
                iterate_as_matrix_viper(x, y,0, r,g,b, mapper) #6 diodes long side
                iterate_as_matrix_viper(x, y,3,r,g,b,mapper)
                if y > 0 and y < 5:
                    iterate_as_matrix_viper(8-x, y,1, r2,g2,b2, mapper) #6 diodes long side
                    iterate_as_matrix_viper(8-x, y,2,r2,g2,b2,mapper)
            for z in range(3,-1,-1):
                iterate_as_matrix_viper(x,0,z,r,g,b,mapper) #4 diodes along z
                iterate_as_matrix_viper(x, 5, z,r,g,b,mapper)
            np.write()
            time.sleep(time_s)

def demo_smooth_transition(x,y,z, time_s, steps):
    mapper = memoryview(mapper_data_to_pos)
    for x in range(9):
            for i in range(0,100,steps):
                    for y in range(6):
                        iterate_as_matrix_viper(x,y,0, gamma(100-i), gamma(100 -i), gamma(100-i),mapper)
                        iterate_as_matrix_viper(x+1,y,0, gamma(i), gamma(i), gamma(i),mapper)
                        iterate_as_matrix_viper(x,y,3, gamma(100-i), gamma(100 -i), gamma(100-i),mapper)
                        iterate_as_matrix_viper(x+1,y,3, gamma(i), gamma(i), gamma(i),mapper)
                        np.write()
            time.sleep(time_s)
    np.fill(0,0,0)

def test_3D_viper():
    with MeasureTime('default') as viper:
        demo_3D()
    with MeasureTime('memoryview') as viper:
        demo_3D_mv()
    with MeasureTime('viper') as viper:
        clear()
        demo_3D_viper()

def demo_random_noise(time_s):
    diodes_pos = []
    for i in range(20):
        x = urandom.randrange(0,9,1)
        y = urandom.randrange(0,6,1)
        z = urandom.randrange(0,4,1)
        r = urandom.randrange(0,100,1)
        g = urandom.randrange(0,100,1)
        b = urandom.randrange(0,100,1)
        iterate_as_matrix_viper(x,y,z, r,g,b,memoryview(mapper_data_to_pos))
        np.write()
        time.sleep(time_s)

def demo_simple_fading(step, r,g,b):
    gamma = 2.2
    for i in range(0,50,step):
        r = int((i/255)**gamma * 255)
        g=int((i/255)**gamma * 255)
        b=int((i/255)**gamma * 255)
        fill_cube(r,g,b)
        np.write()
    for i in range(50,-1,-step):
        r = int((i/255)**gamma * 255)
        g=int((i/255)**gamma * 255)
        b=int((i/255)**gamma * 255)
        fill_cube(r,g,b)
        np.write()

def gamma(value, gamma=2.2):
    return int((value / 255) ** gamma * 255)


def fill_cube(r,g,b):
    np.fill(0,0,0)
    mapper = memoryview(mapper_data_to_pos)
    for x in range(8,-1,-1):
       for y in range(5,-1, -1):
           for z in range(3,-1, -1):
                iterate_as_matrix_viper(x,y,z, r, g, b, mapper) #50us


def demo_bouncing_rectangle_smooth(time_s, range):
    mapper = memoryview(mapper_data_to_pos)
    while True:
        np.fill(0,0,0)
        r = urandom.randrange(0,range,1)
        g = urandom.randrange(0,range,1)
        b = urandom.randrange(0,range,1)
        r2 = urandom.randrange(0,range,1)
        g2 = urandom.randrange(0,range,1)
        b2 = urandom.randrange(0,range,1)
        for x in range(9):
            for y in range(6):
                demo_smooth_transition(x,y,0,0.000001,4)
                demo_smooth_transition(x,y,3,0.000001,4)    
            np.write()
            time.sleep(time_s)
        for x in range(8, -1, -1):
            np.fill(0,0,0)
            for y in range(5,-1,-1):
                iterate_as_matrix_viper(x, y,0, r//4,g//4,b//4, mapper) #6 diodes long side
                iterate_as_matrix_viper(x, y,3,r//4,g//4,b//4,mapper)
                iterate_as_matrix_viper(x-1, y,0, r,g,b, mapper) #6 diodes long side
                iterate_as_matrix_viper(x-1, y,3,r,g,b,mapper)
            np.write()
            time.sleep(time_s)

@micropython.viper
def write_buffer_to_strain(data_, mapper_):
    data = ptr8(data_)
    mapper = ptr16(mapper_)
    for z in range(4):
        for y in range(6):
            for x in range(9):
                pos = x + y * 9 + z * 9 * 6  # it is good
                pos = 3 * pos
                iterate_as_matrix_viper(x,y,z, data[pos], data[pos+1], data[pos+2], mapper)
    np.write()


data = array.array('B', [0] * (NUM_LEDS * 3))
def draw_sphere(cx, cy, cz, radius, brightness,data):
    for z in range(DEPTH):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                # Obliczanie dystansu euklidesowego od środka kuli
                dist = math.sqrt((x - cx)**2 + (y - cy)**2 + (z - cz)**2)
                
                if dist <= radius:
                    # Obliczamy indeks w tablicy
                    idx = (z * WIDTH * HEIGHT + y * WIDTH + x) * 3
                    # Ustawiamy kolor czerwony (Format GRB: Green=0, Red=brightness, Blue=0)
                    data[idx] = brightness          # G
                    data[idx + 1] = 0 # R
                    data[idx + 2] = 0      # B


#iterate_as_matrix_viper(0,0,0,1,1,1,memoryview(data), memoryview(mapper_data_to_pos),0) it is allowed to pass memoryview as ptr8
def sphere_demo(time_s, duration):
    start_t = time.ticks_ms()
    while (time.ticks_ms()-start_t)/1000 < duration:
        cx = urandom.randrange(0,9,1)
        cy = urandom.randrange(0,6,1)
        cz = urandom.randrange(0,4,1)
        for i in range(1,4):
            data = array.array('B', [0] * (NUM_LEDS * 3))
            draw_color_radius_sphere(cx,cy,cz,i,0.5,data)
            write_buffer_to_strain(data,mapper_data_to_pos)
            time.sleep(time_s)
        for i in range(3, 0,-1):
            data = array.array('B', [0] * (NUM_LEDS * 3))
            draw_color_radius_sphere(cx,cy,cz,i,0.5,data)
            write_buffer_to_strain(data,mapper_data_to_pos)
            time.sleep(time_s)


def draw_soft_sphere(cx, cy, cz, radius, brightness, feather,data):
    """
    cx, cy, cz - środek kuli (float)
    radius - promień kuli
    brightness - maksymalna jasność (0-255)
    feather - szerokość pasma rozmycia krawędzi (w jednostkach/diodach)
    """
    for z in range(DEPTH):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                # Obliczamy dystans euklidesowy
                dist = math.sqrt((x - cx)**2 + (y - cy)**2 + (z - cz)**2)
                if dist < radius + feather:
                    # Obliczanie współczynnika jasności (linear falloff)
                    if dist <= radius - feather:
                        factor = 1.0
                    else:
                        # Płynne przejście od 1.0 do 0.0
                        factor = (radius + feather - dist) / (2 * feather)
                        factor = max(0, min(1, factor))
                    # Zastosowanie jasności
                    val = int(brightness * factor)
                    # Indeks w buforze
                    idx = (z * WIDTH * HEIGHT + y * WIDTH + x) * 3
                    # Format GRB
                    data[idx]     = 0       # G
                    data[idx + 1] = gamma(val)     # R (Czerwony)
                    data[idx + 2] = 0       # B

# Wywołanie: kula z miękkim przejściem i jasnym jądrem
def draw_gradient_sphere(cx, cy, cz, radius, brightness, feather,buffer):
    for z in range(DEPTH):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                dist = math.sqrt((x - cx)**2 + (y - cy)**2 + (z - cz)**2)
                if dist < radius + feather:
                    # 1. Obliczamy ogólną intensywność (wygaszanie na krawędziach)
                    if dist <= radius - feather:
                        intensity = 1.0
                    else:
                        intensity = (radius + feather - dist) / (2 * feather)
                        intensity = max(0, min(1, intensity))
                    # 2. Obliczamy "białość" (tylko w samym centrum kuli)
                    # core_ratio będzie 1.0 w centrum i spadnie do 0.0 szybko
                    core_ratio = max(0, 1 - (dist / (radius * 0.7))) 
                    # Kolory:
                    # Czerwony jest zawsze mocny (zależny od intensity)
                    r = int(brightness * intensity)
                    # Zielony i Niebieski pojawiają się tylko w środku (tworząc biały)
                    gb = int(brightness * intensity * core_ratio * 0.8)
                    idx = (z * WIDTH * HEIGHT + y * WIDTH + x) * 3
                    # Format GRB
                    buffer[idx]     = gamma(gb)  # G
                    buffer[idx + 1] = gamma(r)   # R
                    buffer[idx + 2] = gamma(gb)  # B

def hsv_to_rgb(h, s, v):
    """Konwertuje kolory HSV (0-360, 0-1, 0-1) na RGB (0-255)"""
    if s == 0.0: return v, v, v
    i = int(h / 60.0)
    f = (h / 60.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    v, p, q, t = int(v * 255), int(p * 255), int(q * 255), int(t * 255)
    i %= 6
    if i == 0: return v, t, p
    if i == 1: return q, v, p
    if i == 2: return p, v, t
    if i == 3: return p, q, v
    if i == 4: return t, p, v
    if i == 5: return v, p, q

def draw_color_radius_sphere(cx, cy, cz, radius, brightness=1.0, buffer = data):
    for z in range(DEPTH):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                dist = math.sqrt((x - cx)**2 + (y - cy)**2 + (z - cz)**2)
                if dist < radius:
                    # n_dist: 0.0 w środku, 1.0 na krawędzi
                    n_dist = dist / radius
                    # --- MAPOWANIE KOLORU ---
                    # Hue: 30 (pomarańczowy) w środku -> 0 (czerwony) na zewnątrz
                    hue = 180 + (n_dist * 60)
                    # Saturation: zawsze 1.0 dla soczystych kolorów
                    sat = 1.0 
                    # Value (Jasność): mocny spadek przy krawędzi dla efektu głębi
                    val = brightness * (1.0 - n_dist**2)
                    r, g, b = hsv_to_rgb(hue, sat, val)
                    idx = (z * WIDTH * HEIGHT + y * WIDTH + x) * 3
                    # Format GRB dla WS2812
                    buffer[idx]     = gamma(g)
                    buffer[idx + 1] = gamma(r)
                    buffer[idx + 2] = gamma(b)

import array
import math
import time

WIDTH = 9
HEIGHT = 6
DEPTH = 4
NUM_LEDS = WIDTH * HEIGHT * DEPTH
buffer = array.array('B', [0] * (NUM_LEDS * 3))

def update_plasma_sphere(t, cx=4.0, cy=2.5, cz=1.5, radius=3.5, use_gamma=False):
    for i in range(len(buffer)): buffer[i] = 0
    for z in range(DEPTH):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                dist = math.sqrt((x - cx)**2 + (y - cy)**2 + (z - cz)**2)
                if dist < radius:
                    # n_dist: 0.0 (środek) do 1.0 (krawędź)
                    n_dist = dist / radius
                    # --- EFEKT PRZEPŁYWU ---
                    # t steruje przesunięciem fazy. 
                    # Mnożnik przy n_dist (np. 2.0) określa ile cykli koloru mieści się w kuli.
                    # Mnożnik przy t określa prędkość.
                    hue = (n_dist * 120 - t * 150) % 360
                    # Jasność zanika przy krawędziach promienia (feathering)
                    val = 0.8 * (1.0 - n_dist**2)
                    r, g, b = hsv_to_rgb(hue, 1.0, val)
                    idx = (z * WIDTH * HEIGHT + y * WIDTH + x) * 3
                    buffer[idx]     = gamma(g) if use_gamma else g
                    buffer[idx + 1] = gamma(r) if use_gamma else r
                    buffer[idx + 2] = gamma(b) if use_gamma else b

def pulsating_gradient(gamma, duration = 1):
    t_start = time.ticks_ms()
    while (time.ticks_ms()-t_start)/1000 < duration:
        elapsed = time.ticks_diff(time.ticks_ms(), t_start) / 1000.0
        update_plasma_sphere(elapsed,use_gamma =gamma)
        write_buffer_to_strain(buffer,mapper_data_to_pos)
        time.sleep(0.02) # ok. 50 FPS

def ultimate_demo():
    sphere_demo(0.061, 5)
    pulsating_gradient(True,10)
    clear()