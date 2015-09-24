print('\nstarting toasting') -- debug !!!
state = "toasting"
toastingStartTime = tmr.now()
tmr.alarm(toastingTimerId, updateInterval * 1000, 1, function()
		print('\nupdate toasting') -- debug !!!
		if state == "toasting" then
			local finishTime = toastingStartTime + toastingTime * 1000000
			if tmr.now() >= finishTime then
				dofile('resettoasting.lua')
			end
		end	
	end)