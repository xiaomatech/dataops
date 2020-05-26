local useragent = ngx.shared.useragent
local http_user_agent = ngx.var.http_user_agent
local ua, flags, stale = useragent:get_stale(http_user_agent)
if not ua then
    local woothee = woothee
    local cjson = cjson
    local ua = woothee.parse(http_user_agent)
    if not ua then
        ua = {}
    end
    local success, err, forcible = useragent:set(http_user_agent, cjson.encode(ua))
end


local ip2location = ngx.shared.ip2location
local remote_addr = ngx.var.remote_addr
local ip_data, flags, stale = ip2location:get_stale(remote_addr)
if not ip_data then
    local ipipc = ipipc
    local cjson = cjson
    local ip_data, err = ipipc:query_file(remote_addr)
    if not ip_data then
        ip_data = {}
    end
    local success, err, forcible = ip2location:set(remote_addr, cjson.encode(ip_data))
end


local geoip = ngx.shared.geoip
local geoip_data, flags, stale = geoip:get_stale(remote_addr)
if not geoip_data then
    local geo = geo
    local cjson = cjson
    local geoip_data, err = geo:lookup(remote_addr)
    if not geoip_data then
        geoip_data = {}
    end
    local success, err, forcible = geoip:set(remote_addr, cjson.encode(geoip_data))
end


local ck = ck
local cookie, err = ck:new()
local cookie_fields, err = cookie:get_all()
if not cookie_fields then
    cookie_fields = {}
end

local referer = ngx.var.http_referer
local url = url
local referers = url.parse(referer)

ngx.var.useragent = ua
ngx.var.ipip = ip_data
ngx.var.geoip = geoip_data
ngx.var.cookies = cjson.encode(cookie_fields)
ngx.var.referers = cjson.encode(referers)