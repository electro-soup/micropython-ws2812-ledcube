

import urandom
import time
import math
from machine import Pin
#import neopixel
import neoSPI


SPI_ID = 1 # MOSI - #11 on ESP32-S3
NUM_LEDS = 1000
BRIGHTNESS = 0.1
FRAMES = 256  

np = neoSPI.NeoPixel(SPI_ID, NUM_LEDS)

@micropython.viper
def viper_blank(buf, length:int): # naive version of filling all buffer with 0's
    x :int = 0
    wsk = ptr8(buf)
    while x < length:
        wsk[x] = 136
        x = x + 1

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
    viper_blank(np._data, np.n*12)
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
        viper_blank(np._data, _data_len)
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
        viper_blank(np._data, np.n*12)
     


#6x9x4 demo cube
OFFSET = 24


#very naive function for filling 9x6x4 matrix
def write_3D_data(data):
    start = OFFSET
    end = 0
    line_width = 9
    #  first strand transformation - 6 rows (or vertical columns)
    data_temp = data[0:54]
    for i in range(0,6,2):
        end = start+line_width
        print(i*line_width,(i+1)*line_width)
        np[start:end] = data_temp[i*line_width:(i+1)*line_width]
        #now reverse order
        start = end + 1 # 1 for empty led
        end = start + line_width
        temp = data_temp[(line_width)*(i+1):(2+i)*line_width]
        print((line_width)*(i+1),(2+i)*line_width)
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
        print(len(data_temp), len(temp), start, end)
        np[start:end] = temp
        start = end + 1





color_table = []
color_table[0:54] = [ (i,0,0) for i in range(54)]
color_table[54:(54+54)] = [ (i,i,0) for i in range(54)]
color_table[108:(108+54)] = [ (0,i,0) for i in range(54)]
color_table[164:(164+54)] = [ (0,0,i) for i in range(54)]

    #and back to normal
def wall_down(color, time_s):
    for i in range(9):
        color_table = [(0,0,0) for _ in range(4*54)]
        for y in range(i, len(color_table), 9):
            color_table[y] = color
        viper_blank(np._data, np.n*12)
        write_3D_data(color_table)
        np.write()
        time.sleep(time_s)


def wall_back_to_front(color = (0, 4,0), time_s = 0.1):
    for i in range(0, 216,54):
        color_table = [(0,0,0) for _ in range(4*54)]
        color_table[i:(i+54)] = [ color for _ in range(54)]
        viper_blank(np._data, np.n*12)
        write_3D_data(color_table)
        np.write()
        time.sleep(time_s)

        

def cascade_wall():
    wall_down((0,4,4), 0.5)
    wall_down((4,0,4), 0.3)
    wall_down((2,4,3), 0.2)
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


def wall_side_to_side(color=(0,0,3), time_s = 0.1):
    for x in range(6):
        color_table = [(0,0,0) for _ in range(4*54)]
        for y in range(4):
            start = (x*9)+y*54
            end = (x+1)*9+y*54
            print(start, end)
            color_table[start:end] = [color for _ in range(9)]
        viper_blank(np._data, np.n*12)
        write_3D_data(color_table)
        np.write()
        time.sleep(time_s)

def check_light_strain(time_s = 0.5):
    for i in range(216):
        color_table = [(0,0,0) for _ in range(4*54)]
        clear()
        color_table[i] = (5,5,5)
        write_3D_data(color_table)
        np.write()
        time.sleep(time_s)
        print(i)


def iterate_as_matrix(xyz_coords, color_value, data, blank = 0):
    #data = [(0,0,0) for _ in range(4*54)]
    X_ax = 9
    Y_ax = 6
    Z_ax = 4
    x, y, z = xyz_coords
    pos = x + y * X_ax + z * X_ax * Y_ax 
    print(f"{pos=}")
    data[pos] = color_value
    if blank == 1:
        viper_blank(np._data, np.n*12)
    write_3D_data(data)
    np.write()

def clear_buffer(data):
    data = [(0,0,0) for _ in range(4*54)]


