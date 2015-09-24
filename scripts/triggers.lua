function debounce (func)
    local last = 0
    local delay = 200000

    return function (...)
        local now = tmr.now()
        if now - last < delay then return end

        last = now
        return func(...)
    end
end

function onTrigger ()
	local newTriggerState = gpio.read(toasting_trig_pin) == gpio.HIGH
	if isTriggerDown ~= newTriggerState then
		isTriggerDown = newTriggerState
		if isTriggerDown then
			dofile('starttoasting.lua')
		else
			dofile('finishtoasting.lua')
		end
	end
end

gpio.mode(reset_btn_pin, gpio.OUTPUT)
gpio.write(reset_btn_pin, gpio.HIGH)

gpio.mode(toasting_trig_pin, gpio.INT)
gpio.trig(toasting_trig_pin, 'both', debounce(onTrigger))