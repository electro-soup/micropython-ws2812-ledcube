

import urandom
import time
import math
from machine import Pin
#import neopixel
import neoSPI


SPI_ID = 1 # MOSI - #11 on ESP32-S3
NUM_LEDS = 300
BRIGHTNESS = 0.1
FRAMES = 256  

np = neoSPI.NeoPixel(SPI_ID, NUM_LEDS)



def set_pixel(i, color):
    r, g, b = color
    np[i] = (int(g * BRIGHTNESS), int(r * BRIGHTNESS), int(b * BRIGHTNESS))

def wheel(pos):
    """Zwraca kolor tęczy od 0-255"""
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle(wait=0.02, loops=2):
    for j in range(256 * loops):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS + j) & 255
            set_pixel(i, wheel(rc_index))
        np.write()
        time.sleep(wait)

def theater_chase(color, wait=0.05, cycles=20):
    for j in range(cycles):
        for q in range(3):
            for i in range(0, NUM_LEDS, 3):
                set_pixel((i + q) % NUM_LEDS, color)
            np.write()
            time.sleep(wait)
            for i in range(0, NUM_LEDS, 3):
                set_pixel((i + q) % NUM_LEDS, (0, 0, 0))

def breathing(color, duration=3, steps=100):
    for i in range(steps):
        level = (math.sin(i / steps * math.pi) ** 2)
        for j in range(NUM_LEDS):
            set_pixel(j, tuple(int(c * level) for c in color))
        np.write()
        time.sleep(duration / steps)

def running_light(color, wait=0.05):
    for i in range(NUM_LEDS * 2):
        for j in range(NUM_LEDS):
            brightness = max(0, math.sin((i - j) / 2))
            set_pixel(j, tuple(int(c * brightness) for c in color))
        np.write()
        time.sleep(wait)

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

# --- funkcje pomocnicze ---
def scale_color(color):
    r, g, b = color
    return (int(r * BRIGHTNESS), int(g * BRIGHTNESS), int(b * BRIGHTNESS))

def wheel(pos):
    """Zwraca kolor tęczy od 0-255"""
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)


def random_color():
    return (urandom.randrange(0,10,1), urandom.randrange(0,10,1),urandom.randrange(0,10,1))

def snake(color, num_pixels, time_s):
    np = neopixel.NeoPixel(Pin(LED_PIN), num_pixels)
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
        
        
def wave_horizont_1(time_s, colour):
    for i in range(12):
           clear()
           color = random_color()
           for y in range(42 +i*14, 42+14 +i*14,1):
               np[y] = color
           np.write()
           time.sleep(time_s)
    #return to monke

def wave_horizont_2(time_s, colour):
    for i in range(11, -1, -1):
           clear()
           color = random_color()
           for y in range(42 +i*14, 42+14 +i*14,1):
               np[y] = color
           np.write()
           time.sleep(time_s)
           
def wave_vertical(time_s, colour, n_leds):
    for i in range(n_leds):
           clear()
           color = random_color()
           for y in range(11, -1, -1):
               np[y*14+i] = color
           np.write()
           time.sleep(time_s)
           
def sparkle_v2(duration=3, wait=0.05):
    end_time = time.ticks_add(time.ticks_ms(), int(duration * 1000))
    while time.ticks_diff(end_time, time.ticks_ms()) > 0:
        i = urandom.randint(42, 42+14*12)
        np[i] = (100, 100, 100)
        np.write()
        time.sleep(wait)
        clear()
        
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
     


#6x9x4 demo cube
OFFSET = 24



#very naive function for filling 9x6x4 matrix
def write_3D_data(data):
    start = 24
    end = 0
    line_width = 9
    #  first strand transformation - 6 rows (or vertical columns)
    data_temp = data[0:54]
    for i in range(0,6,2):
        end = start+line_width
        #print(i*line_width,(i+1)*line_width)
        np[start:end] = data_temp[i*line_width:(i+1)*line_width]
        #now reverse order
        start = end + 1 # 1 for empty led
        end = start + line_width
        temp = data_temp[(line_width)*(i+1):(2+i)*line_width]
        #print((line_width)*(i+1),(2+i)*line_width)
        np[start:end] = temp[::-1]
        start = end + 1
    start = end + 3
    #reverse part of array for second 2d slice:
    data_temp = data[54:108]
    data_temp = data_temp[::-1]
    for i in range(0,6,2):
        end = start+line_width
        temp = data_temp[i*line_width:(i+1)*line_width]
        np[start:end]= temp[::-1]
        #now reverse order
        start = end + 1 # 1 for empty led
        end = start + line_width
        np[start:end]= data_temp[(line_width)*(i+1):(2+i)*line_width]
        start = end + 1
        #third slice
    start = end + 3
    data_temp = data[108:162] 
    for i in range(0,6,2):
        end = start+line_width
        np[start:end] = data_temp[i*line_width:(i+1)*line_width]
        #now reverse order
        start = end + 1 # 1 for empty led
        end = start + line_width
        temp = data_temp[(line_width)*(i+1):(2+i)*line_width]
        np[start:end] = temp[::-1]
        start = end + 1
    start = end + 2
    #and the same as #2
    data_temp = data[162:216]
    data_temp = data_temp[::-1]
    for i in range(0,6,2):
        end = start+line_width
        temp = data_temp[i*line_width:(i+1)*line_width]
        np[start:end] = temp[::-1]
        #now reverse order
        start = end + 1 # 1 for empty led
        end = start + line_width
        temp = data_temp[(line_width)*(i+1):(2+i)*line_width]
        #print(len(data_temp), len(temp), start, end)
        np[start:end] = temp
        start = end + 1





color_table = []
color_table[0:54] = [ (i,0,0) for i in range(54)]
color_table[54:(54+54)] = [ (i,i,0) for i in range(54)]
color_table[108:(108+54)] = [ (0,i,0) for i in range(54)]
color_table[164:(164+54)] = [ (0,0,i) for i in range(54)]

    #and back to normal
def wall_down(color, time_s, blank = 1):
    for i in range(9):
        if i == 0:
            color_table = [(0,0,0) for _ in range(4*54)]
        if blank:
            color_table = [(0,0,0) for _ in range(4*54)]
        for y in range(i, len(color_table), 9):
            color_table[y] = color
        if blank:     
            np.viper_blank()
        write_3D_data(color_table)
        np.write()
        time.sleep(time_s)


def wall_back_to_front(color = (0, 4,0), time_s = 0.1, blank = 1):
    for i in range(0, 216,54):
        if i == 0:
            color_table = [(0,0,0) for _ in range(4*54)]
        if blank:
            color_table = [(0,0,0) for _ in range(4*54)]
        color_table[i:(i+54)] = [ color for _ in range(54)]
        if blank:
            np.viper_blank()
        write_3D_data(color_table)
        np.write()
        time.sleep(time_s)

def test_iterate_mv(point):
        data = array.array('B', [0 for i in range(4*54*3)])
        iterate_as_matrix_mv(point, (5,5,5), data)
        write_3D_data_mv(data)
        np.write()

def cascade_wall():
    wall_down((0,4,4), 0.5,0)
    wall_down((4,0,4), 0.3,0)
    wall_down((2,4,3), 0.2,0)
    wall_down((0,0,3), 0.1)
    wall_down((3,0,0), 0.001)
    wall_down((0,1,2), 0.001)
    wall_down((2,1,0), 0.001)
    wall_down((1,1,1), 0.001)
    wall_back_to_front((0,4,4), 0.5)
    wall_back_to_front((4,0,4), 0.3)
    wall_back_to_front((2,4,3), 0.2)
    wall_back_to_front((0,0,3), 0.1)
    wall_back_to_front((3,0,0), 0.001)
    wall_back_to_front((0,1,2), 0.001)
    wall_back_to_front((2,1,0), 0.001)
    wall_back_to_front((1,1,1), 0.001)
    clear()


def wall_side_to_side(color=(0,0,3), time_s = 0.1, blank = 1):
    for x in range(6):
        if x == 0:
            color_table = [(0,0,0) for _ in range(4*54)]
        if blank:
            color_table = [(0,0,0) for _ in range(4*54)]
        for y in range(4):
            start = (x*9)+y*54
            end = (x+1)*9+y*54
            print(start, end)
            color_table[start:end] = [color for _ in range(9)]
        if blank:
            np.viper_blank()
        write_3D_data(color_table)
        np.write()
        time.sleep(time_s)

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
                with MeasureTime('write_3D_data') as iterate:
                    write_3D_data_mv(dd)
                np.write()
    for x in range(8,-1,-1):
       for y in range(5,-1, -1):
           for z in range(3,-1, -1):
            iterate_as_matrix_mv(x,y,z, 0, 0 ,0, dd,0)
            write_3D_data_mv(dd)
            np.write()
        

def last_demo():
    #while True:
        color = random_color()
        wall_down(color, 0.05,0)
        color = random_color()
        wall_side_to_side(color, 0.05,0)
        color = random_color()
        wall_back_to_front(color, 0.05,0)
        color = random_color()
        wall_down(color, 0.05,1)
        color = random_color()
        wall_side_to_side(color, 0.05,1)
        color = random_color()
        wall_back_to_front(color, 0.05,1)
        color = random_color()
        demo_3D()
        clear()


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
            #print(rgb, ' 1 strand', data_it)
            np.viper_set_pixel(rgb, data[data_it], data[data_it+1], data[data_it+2]) 
            data_it +=3
                    #now reverse order
        start = end + 1 # 1 for empty led
        end = start + line_width
        for rgb in range(end-1, start-1, -1):
            #print(rgb, '2 strand', data_it)
            np.viper_set_pixel(rgb, data[data_it], data[data_it+1], data[data_it+2])
            data_it +=3 
        start = end + 1
    #print(f'{start=}')
    return start


def write_2D_slice_mv_2(start, data:memoryview):
    line_width = 9
    data_it = len(data) - 3
    #print(f'entry {start=}')
    for i in range(0,6,2):
        end = start+line_width
        for rgb in range(end-1, start-1, -1):
            #print(rgb, ' 1 strand', data_it)
            np.viper_set_pixel(rgb, data[data_it], data[data_it+1], data[data_it+2]) 
            data_it -=3
                    #now reverse order
        start = end + 1 # 1 for empty led
        end = start + line_width
        for rgb in range(start, end):
            #print(rgb, '2 strand', data_it)
            np.viper_set_pixel(rgb, data[data_it], data[data_it+1], data[data_it+2])
            data_it -=3 
        start = end + 1
    #print(f'{start=}')
    return start

def write_3D_data_mv(data:memoryview):
    start = 24
    end = 0
    line_width = 9
    #  first strand transformation - 6 rows (or vertical columns)
    data_temp = memoryview(data[0:162])
    end = write_2D_slice_mv(start, data_temp)
    start = end + 2
    #reverse part of array for second 2d slice:
    data_temp = memoryview(data[162:324])
    #data_temp = data_temp[::-1]
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
    #data_temp = data_temp[::-1]
    end = write_2D_slice_mv_2(start, data_temp)


class MeasureTime:
    def __init__(self, title ):
        self.title = title
    def __enter__( self ):
        self.t0 = time.ticks_us()
        return self
    def __exit__( self, exc_type, exc_val, exc_traceback ):
        self.time_usec = time.ticks_diff( time.ticks_us(), self.t0 )
        print(f"\tMeasureTime {self.title} {self.time_usec} usec" )

#bytearray version