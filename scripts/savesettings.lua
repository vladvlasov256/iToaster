if file.open("toastingtime.ini", "w") then
	file.writeline(tostring(toastingTime))
	file.close()
end