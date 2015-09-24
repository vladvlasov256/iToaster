if not message then
	return "empty message"
end

local args = dofile("splitstring.lua")
local argc = table.maxn(args)
if argc == 0 then
	return "empty command"
end

if args[1] == "ping" then
	return "ok"
elseif args[1] == "getState" then
	return state
elseif args[1] == "getRemainingTime" then
	if toastingStartTime > 0 then
		return tostring(toastingTime - (tmr.now() - toastingStartTime) / 1000000)
	else
		return "0"
	end
elseif args[1] == "getToastingTime" then
	return tostring(toastingTime)
elseif args[1] == "setToastingTime" then
	if argc > 1 then
		toastingTime = tonumber(args[2])
		dofile('savesettings.lua')
		return "ok"
	else
		return "not enough params"
	end
elseif args[1] == "reset" then
	dofile('resettoasting.lua')
	return "ok"
else
	return "unknown command: "..message
end