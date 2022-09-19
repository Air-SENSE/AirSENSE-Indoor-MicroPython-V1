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


#import MicroPython library
from machine import Pin, SoftSPI  # type: ignore
import network
import esp
from umqttsimple import MQTTClient
import micropython

#import file for PMS7003 SENSOR
from pms7003 import Pms7003
from aqi import AQI

#import file for Display ILI9341
from ili9341 import Display, color565


#Wifi declaration
SSID     = "BK Star"
PASSWORD = "bkstar2021"

#MQTT declaration
newMac    = "DC:4F:22:7E:67:93"
SERVER    = "mqtt.airsense.vn"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
print(CLIENT_ID)
PORT      = "1884"
TOPIC     = "/V3/"
 # + newMac
username  = "sparc"
password  = 'sparcXZAairsenseATU'

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
  time.sleep(10)
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
        messageJSON = dict({"DATA":["Pm1":pms_data['PMS_PM1_0'], "Pm10":pms_data['PMS_PM10_0'], "Pm2p5":pms_data['PM2_5_ATM'], "Time":0, "NodeID":newMac]})
        client.publish(TOPIC, json.domps(messageJSON))

        #Draw PM2.5
        display.draw_text8x8(display.width - 150, y_center + 60, "PM2.5: ",
                             color565(255, 255, 255), rotate=270)
        display.draw_text8x8(display.width - 150, y_center + 10 ,str(pms_data['PM2_5_ATM']),
                             color565(255, 255, 255), rotate=270)
        display.draw_text8x8(display.width - 150, y_center - 40, "PPM",
                             color565(255, 255, 255), rotate=270)
        #Draw PM10
        display.draw_text8x8(display.width - 100, y_center + 60, " PM10: ",
                             color565(255, 255, 255), rotate=270)
        display.draw_text8x8(display.width - 100, y_center + 10 ,str(pms_data['PM10_0_ATM']),
                             color565(255, 255, 255), rotate=270)
        display.draw_text8x8(display.width - 100, y_center - 40, "PPM",
                             color565(255, 255, 255), rotate=270)
        sleep(3)

#main()
if __name__ == '__main__':
    main()
