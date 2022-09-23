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
import esp
import micropython

#import file for PMS7003 SENSOR
from pms7003 import Pms7003
from aqi import AQI

#import file for Display ILI9341
from ili9341 import Display, color565


#PMS declaration
pms = Pms7003(uart=2)

#Display declaration
spi = SoftSPI( baudrate=40000000, sck=Pin(18), mosi=Pin(19), miso=Pin(21))
display = Display(spi, dc=Pin(12), cs=Pin(13), rst=Pin(15))
    


def main():
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
