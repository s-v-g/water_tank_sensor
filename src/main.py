import utime
import time
import socket
import pycom
import machine
from machine import Pin
import wifi
import tank_sensor


SERVER_IP = '45.124.55.218'
SERVER_PORT = 51111
addr = (SERVER_IP,SERVER_PORT)

pycom.heartbeat(False)

def send_data(data_string):
    
    MESSAGE = data_string.encode()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr=(SERVER_IP,SERVER_PORT)
    s.sendto(MESSAGE,addr)

def setup_pins():
    trigger = Pin(Pin.exp_board.G24, mode=Pin.OUT, pull=Pin.PULL_DOWN) #P3
    echo = Pin(Pin.exp_board.G11, mode=Pin.IN) # P4    
    trigger(0) # set low
    return trigger, echo

def send_udp(sock, data):
    
    data_string = ",".join(data)    
    message = data_string.encode()
    sock.sendto(message,addr)


def establish_connection():
    while not wifi.connect_wifi():
        time.sleep(1)


def run():
    #wifi.connect_wifi()
    #pycom.rgbled(0xff00)#set green for running
    trigger, echo = setup_pins()

    #create ports so we can send data to grafana
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  

    print("start")
    while True:
        establish_connection()
        print('loop')
        # get water tank readings from ultrasonic distance sensor
        try:
            distance = tank_sensor.get_median_distance(trigger, echo)
            print("distance calculated: {}".format(distance))
            if distance < 0:
                distance = None
        except:
            distance = None
            print('error getting distance')
        
        try:
            litres = tank_sensor.calculate_water(distance)
            print("water calculated: {}L".format(litres))
            if litres < 0 or litres > 45000:
                litres = None
                print('litres out of bounds')
        except:
            litres = None
            print('error getting water')
        

        try:
            send_udp(s, ['TANK', str(distance), str(litres)])        
        except:
            print("problem sending tank data")
        

        time.sleep(30)
        
run()