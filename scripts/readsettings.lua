if file.open("toastingtime.ini", "r") then
	toastingTime = tonumber(file.readline())
	file.close()
end