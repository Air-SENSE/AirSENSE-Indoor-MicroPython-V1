"""
PMS7003 hardware Setup:
    tx - RX2
    rx - TX2
ILI9341 hardware Setup:
    PIN_NUM_MISO 21
    PIN_NUM_MOSI 19
    PIN_NUM_CLK  18
    PIN_TFT_RST     15
    PIN_TFT_LED     14
    PIN_TFT_DC      12
    PIN_TFT_CS      13
"""
#import python library
from time import sleep
import ubinascii
import json
import time
import utime

#import MicroPython library
import machine
from machine import Pin, SoftSPI  # type: ignore
import network
import esp
from umqttsimple import MQTTClient
import micropython
import ntptime


#import file for PMS7003 SENSOR
from pms7003 import Pms7003
from aqi import AQI

#import file for Display ILI9341
from ili9341 import Display, color565


#Wifi declaration
SSID     = "BK Star"
PASSWORD = "bkstar2021"
UTC_OFFSET = 7 * 60 * 60

#MQTT declaration
DeviceID = machine.unique_id()

newMac    = '{:02x}{:02x}{:02x}{:02x}'.format(DeviceID[0], DeviceID[1], DeviceID[2], DeviceID[3])
SERVER    = "103.1.238.175"
CLIENT_ID = newMac
PORT      = "1885"
TOPIC     = "/V3/" + newMac
username  = "test"
password  = 'testadmin'

#PMS declaration
pms = Pms7003(uart=2)

#Display declaration
spi = SoftSPI( baudrate=40000000, sck=Pin(18), mosi=Pin(19), miso=Pin(21))
display = Display(spi, dc=Pin(12), cs=Pin(13), rst=Pin(15))
    
#Wifi connection
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(SSID, PASSWORD)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
ntptime.settime()

#connect MQTT
def connect():
  print('Connecting to MQTT Broker...')
  global CLIENT_ID, SERVER, PORT, username, password
  client = MQTTClient(CLIENT_ID, SERVER, PORT, username, password)
  client.connect()
  print('Connected to %s MQTT broker' % (SERVER))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  sleep(10)
  machine.reset()


def main():
    global newMac, TOPIC
    try:
      client = connect()
    except OSError as e:
      restart_and_reconnect()
    #get center of display
    x_center = display.width // 2
    y_center = display.height // 2
    #Draw some introduce codes 
    display.draw_text8x8(0, 0, 'AirSENSE Education',color565(255, 0, 255), rotate=270)
    display.draw_text8x8(16, 38, 'MicroPython Indoor Version 3.0',color565(255, 255, 0), rotate=270)
    #loop
    while True:
        #pms get data from UART2
        pms_data = pms.read()
        #get the epoch time
        timestamp = 946684800 + utime.time() + UTC_OFFSET
        # split data from pms_data
        pm1 = pms_data['PM1_0_ATM']
        pm10 = pms_data['PM10_0_ATM']
        pm2p5 = pms_data['PM2_5_ATM']
        #make a dictionary for decode to json 
        messageJSON = dict({"station_id": newMac, "Time":timestamp,  "PM2p5":pm2p5, "PM10":pm10,"PM1":pm1})
        #publish mess json to server mqtt
        client.publish(TOPIC, json.dumps(messageJSON))
        print(messageJSON)
        #Draw PM2.5
        display.draw_text8x8(display.width - 150, y_center + 60, "PM2.5: ",
                             color565(255, 255, 255), rotate=270)
        display.draw_text8x8(display.width - 150, y_center + 10 ,str(pm2p5),
                             color565(255, 255, 255), rotate=270)
        display.draw_text8x8(display.width - 150, y_center - 40, "PPM",
                             color565(255, 255, 255), rotate=270)
        #Draw PM10
        display.draw_text8x8(display.width - 100, y_center + 60, " PM10: ",
                             color565(255, 255, 255), rotate=270)
        display.draw_text8x8(display.width - 100, y_center + 10 ,str(pm10),
                             color565(255, 255, 255), rotate=270)
        display.draw_text8x8(display.width - 100, y_center - 40, "PPM",
                             color565(255, 255, 255), rotate=270)
        sleep(3)

#main()
if __name__ == '__main__':
    main()
