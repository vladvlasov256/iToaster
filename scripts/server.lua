port = 50007
dispatchMessage = nil
toasterServer = nil

function receiveMessage(conn, message)
	local answer = dispatchMessage(message)
	conn:send(answer)
end

local server = {}
function server.start(dispatchMessageCallback)
	dispatchMessage = dispatchMessageCallback
	toasterServer = net.createServer(net.TCP)
	toasterServer:listen(port, function(conn) conn:on("receive", receiveMessage) end)
end

function server.stop()
	if toasterServer ~= nil then
		toasterServer:close()
		toasterServer = nil
	end
end

return server