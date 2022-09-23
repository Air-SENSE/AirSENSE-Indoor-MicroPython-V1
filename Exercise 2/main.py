#import python library
from time import sleep

#import files library for PMS7003 SENSOR
from pms7003 import Pms7003
from aqi import AQI

#PMS declaration
pms = Pms7003(uart=2)

#loop
while True:
    #pms get data from UART2
    pms_data = pms.read()
    # split data from pms_data
    pm2p5 = pms_data['PM2_5_ATM']
    print(pm2p5)
    sleep(3)

