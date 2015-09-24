-- ToDo:
-- * when wifi disconnected we should stop server
-- * so we shouldn't dispose connection module


reset_btn_pin = 3 -- GPIO0
toasting_trig_pin = 4 -- GPIO2

isTriggerDown = false
toastingTime = 10
toastingStartTime = 0
updateInterval = 1
toastingTimerId = 2
state = "idle"

servermodule = nil
-- servermodule = require('server')
connectionmodule = require('connection')

message = ""

function onWifiConnected()
	-- connectionmodule = nil
	collectgarbage()

	servermodule = require('server')
	servermodule.start(function(msg) 
			message = msg
			return dofile('dispatcher.lua')
		end)
end

function onWifiDisonnected()
	servermodule.stop()
	servermodule = nil
	collectgarbage()
end

dofile('readsettings.lua')
dofile('triggers.lua')
connectionmodule.start(onWifiConnected, onWifiDisonnected)