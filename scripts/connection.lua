connectionTimerId = 0
connectionInterval = 3000
checkInterval = 10000

state_connection = 0
state_connected = 1

currentState = state_connection

function repeatCheckConnection(wifiConnected, onConnected, onDisconnected)
   local interval = 0
   if wifiConnected then
      interval = checkInterval
   else
      interval = connectionInterval
   end
   tmr.alarm(connectionTimerId, interval, 0, function() checkConnection(onConnected, onDisconnected) end)
end

function checkConnection(onConnected, onDisconnected)
   local wifiConnected = (wifi.sta.status() == 5)

   if currentState == state_connection then
      if wifiConnected then
         currentState = state_connected
         print('\nWiFi has connected as '..wifi.sta.getip())
         onConnected()
      end
   elseif currentState == state_connected then
      if not wifiConnected then
         currentState = state_connection
         print('\nWiFi has disconnected')
         onDisconnected()
         wifi.sta.connect()
      end
   end

   repeatCheckConnection(wifiConnected, onConnected, onDisconnected)
end

local connection = {}
function connection.start(onConnected, onDisconnected)
   wifi.setmode(wifi.STATION)

   -- wifi.sta.config("OneLittleNet","manchesterunited")
   wifi.sta.config("home.net_E0508F", "RCQDJJ3P")
   wifi.sta.connect()

   repeatCheckConnection(false, onConnected, onDisconnected)
end

return connection