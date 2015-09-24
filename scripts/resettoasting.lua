gpio.write(reset_btn_pin, gpio.LOW)
tmr.delay(200000)
gpio.write(reset_btn_pin, gpio.HIGH)
dofile('finishtoasting.lua')