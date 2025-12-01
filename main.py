

import urandom
import time
import math
from machine import Pin
#import neopixel
import neoSPI


SPI_ID = 1 # MOSI - #11 on ESP32-S3
NUM_LEDS = 100
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
    np[i] = (int(r * BRIGHTNESS), int(g * BRIGHTNESS), int(b * BRIGHTNESS))

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

# --- precomputing: tworzymy gotową listę kolorów ---
# print("Generuję ramki tęczy...")
# rainbow_frames = []
# for j in range(FRAMES):
#     frame = []
#     for i in range(NUM_LEDS):
#         rc_index = (i * 256 // NUM_LEDS + j) & 255
#         frame.append(scale_color(wheel(rc_index)))
#     rainbow_frames.append(frame)
# print("Gotowe! Łącznie:", len(rainbow_frames), "ramek.")


def rainbow_cycle_fast_simple(wait=0.01, loops=5):
    for _ in range(loops):
        for frame in rainbow_frames:
            # przypisz piksele po kolei (bez np[:] = frame)
            for i, color in enumerate(frame):
                np[i] = color
            np.write()
            time.sleep(wait)

# przygotowanie: skonwertujemy każdą ramkę do surowych bajtów RGB
def frames_to_bytearrays(frames):
    ba_frames = []
    for frame in frames:
        ba = bytearray(NUM_LEDS * 3)
        # NeoPixel w MicroPythonie zwykle używa RGB w kolejności (r,g,b)
        for i, (r, g, b) in enumerate(frame):
            j = i * 3
            ba[j]   = r
            ba[j+1] = g
            ba[j+2] = b
        ba_frames.append(ba)
    return ba_frames

#rainbow_frames_ba = frames_to_bytearrays(rainbow_frames)

def rainbow_cycle_fast_optimized(wait=0.005, loops=5, num_pixels = 100):
            np = neoSPI.NeoPixel(Pin(LED_PIN), num_pixels)
        # wybieramy nazwę, która istnieje
            buf_obj = getattr(np, 'buf', None) or getattr(np, 'bytearray', None) or None
        

            for _ in range(loops):
                for ba in rainbow_frames_ba:
                    # upewnij się że rozmiary matchują
                    time.sleep(wait)
                    buf_obj[:] = ba
                    np.write() #it looks like starting some process, but working in background
                    
                    
            return
def random_color():
    return (urandom.randrange(0,100,10), urandom.randrange(0,100,10),urandom.randrange(0,100,10))

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
           np.fill((0,0,0))
           color = random_color()
           for y in range(42 +i*14, 42+14 +i*14,1):
               np[y] = color
           np.write()
           time.sleep(time_s)
    #return to monke

def wave_horizont_2(time_s, colour):
    for i in range(11, -1, -1):
           np.fill((0,0,0))
           color = random_color()
           for y in range(42 +i*14, 42+14 +i*14,1):
               np[y] = color
           np.write()
           time.sleep(time_s)
           
def wave_vertical(time_s, colour):
    for i in range(42, 42+14,1):
           np.fill((0,0,0))
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
        np.fill((0,0,0))
        np.write()
    
           
