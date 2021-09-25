from network import WLAN
import machine
import time

SSID = 'insert_wifi_SSID_here'
PASSPHRASE = 'insert_wifi_password'

def connect_wifi():    
    
    wlan = WLAN(mode=WLAN.STA)
    wlan.ifconfig(config=('192.168.8.3', '255.255.255.0', '192.168.8.1', '192.168.8.2'))    
    try:
        #if not wlan.isconnected():       
        while not wlan.isconnected():        
            print('attempting to connect...')
            wlan.connect(SSID, auth=(3, PASSPHRASE), timeout=5000)
            #while not wlan.isconnected():
            #    machine.idle() # save power while waiting
            
            time.sleep(5)
        print('WLAN is connected.')    
        
    except:
        print("wireless connection problem")
        return False
    

    return wlan.isconnected()