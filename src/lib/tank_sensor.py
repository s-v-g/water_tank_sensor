import utime

#water tank dimensions
TANK_HEIGHT = 240#cm
TANK_RADIUS = 165#cm
pi = 3.1415926

# Ultrasonic distance measurment
def distance_measure(trigger, echo):    
    # trigger pulse LOW for 2us (just in case)
    trigger(0)    
    utime.sleep_us(20)
    # trigger HIGH for a 20us pulse
    trigger(1)
    utime.sleep_us(20)
    trigger(0)
    
    reference_time = utime.ticks_us()
    #make sure the echo signal is low - it should be
    #but if it isnt there probably is a problem with the
    #pin - return None if it times out
    while echo() == 0:    
        start = utime.ticks_us()        
        if (start - reference_time) > 20000:
            print('timeout')
            return None
         
    start = utime.ticks_us()
    waiting = start  

    #wait for our echo to go low, or to timeout
    while echo() == 1 or (waiting - start) > 60000:
        waiting = utime.ticks_us()    
        pass

    finish = waiting
    # pause for 20ms to prevent overlapping echos
    utime.sleep_ms(20)

    # calculate distance by using time difference between start and stop
    # speed of sound 340m/s or .034cm/us. Time * .034cm/us = Distance sound travelled there and back
    # divide by two for distance to object detected.
    time_diff = utime.ticks_diff(finish,start) 
    distance = (time_diff * 0.034 / 2) + 3 #3cm fudge/calibration factor
    return distance

def median(lst):
    n = len(lst)
    s = sorted(lst)
    return (sum(s[n//2-1:n//2+1])/2.0, s[n//2])[n % 2] if n else None

def get_median_distance(trigger, echo):
    distances = []
    #take 10 measurements over 1 second, return the median
    for i in range(10):
        distances.append(distance_measure(trigger, echo))
        #print(distances[-1])
        utime.sleep_ms(100)
    return median(distances)

def calculate_water(space_at_top):
    # volume of a cylinder: pi * r^2 * h

    litres = pi * TANK_RADIUS**2 * (TANK_HEIGHT - space_at_top) * 0.001
    return litres