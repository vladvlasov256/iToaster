res = {}
local q = message:find("?")
if not q then
    res[1] = message
else
    res[1] = message:sub(1, q - 1)
    res[2] = message:sub(q + 1)
end
return res