from m5stack import *
from m5stack_ui import *
from uiflow import *
import time
import unit
import urequests
import hashlib
import binascii

rtc.settime('ntp', 
host='cn.pool.ntp.org', tzone=1)
rtc.datetime()
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xd5d5d5)
env3_0 = unit.get(unit.ENV3, unit.PORTA)
temp_flag = 300


passwd = "<THIS_MY_PASS>"
h = hashlib.sha256(passwd)
passwd_hash = binascii.hexlify(h.digest())


Temp = M5Label('Temp:', x=19, y=142, color=0x000, font=FONT_MONT_22, parent=None)
Humidity = M5Label('Humidity:', x=19, y=183, color=0x000, font=FONT_MONT_22, parent=None)
Date = M5Label('Date:', x=19, y=220, color=0x000, font=FONT_MONT_15, parent=None)
Time = M5Label('Time:', x=19, y=250, color=0x000, font=FONT_MONT_15, parent=None)
label0 = M5Label('T', x=163, y=142, color=0x000, font=FONT_MONT_22, parent=None)
label1 = M5Label('H', x=158, y=183, color=0x000, font=FONT_MONT_22, parent=None)
label6 = M5Label('In', x=158, y=103, color=0x000, font=FONT_MONT_18, parent=None)
label7 = M5Label('Out', x=234, y=103, color=0x000, font=FONT_MONT_18, parent=None)
label8 = M5Label('--', x=234, y=142, color=0x000, font=FONT_MONT_22, parent=None) # outdoor temp
label9 = M5Label('--', x=229, y=183, color=0x000, font=FONT_MONT_22, parent=None) # outdoor humidity


while True:
  dt = rtc.datetime()
  Date.set_text('Date: {}-{:02d}-{:02d}'.format(dt[0], dt[1], dt[2]))
  Time.set_text('Time: {:02d}:{:02d}:{:02d}'.format(dt[3], dt[4], dt[5]))
  
  label0.set_text(str(round(env3_0.temperature)))
  label0.set_text_color(0x000000)
  label1.set_text(str(round(env3_0.humidity))+" %")
  label1.set_text_color(0x000000)
  # get temp every 5 minutes
  if temp_flag == 300:
    dt = rtc.datetime()
    data = {
        "passwd": passwd_hash,
        "values": {
            "date": '{}-{:02d}-{:02d}'.format(dt[0], dt[1], dt[2]),
            "time": '{:02d}:{:02d}:{:02d}'.format(dt[3], dt[4], dt[5]),
            "indoor_temp": round(env3_0.temperature),
            "indoor_humidity": round(env3_0.humidity)
        }
    }
    urequests.post("https://weather-station-app-691588068776.europe-west6.run.app/send-to-bigquery", json=data)
    outdoor_data = {"passwd": passwd_hash}
    outdoor_response = urequests.post("https://weather-station-app-691588068776.europe-west6.run.app/get_outdoor_weather", json=outdoor_data)
    outdoor = outdoor_response.json()
    label8.set_text(str(round(outdoor["outdoor_temp"])))
    label9.set_text(str(round(outdoor["outdoor_humidity"])) + " %")
    temp_flag = 0
  temp_flag += 1 # counter for the 300 seconds wait to update the temperature info.
  wait(1)
  wait_ms(2)