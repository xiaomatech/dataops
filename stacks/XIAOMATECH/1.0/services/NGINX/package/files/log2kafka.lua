local cjson = require "cjson"
local producer = require "resty.kafka.producer"

local broker_list = {
    { host = "127.0.0.1", port = 9092 },
    { host = "127.0.0.1", port = 9092 },
    { host = "127.0.0.1", port = 9092 }
}

local request_id = ngx.var.request_id
local log = {}
log["timestamp"] = ngx.var.time_iso8601
log["time_local"] = ngx.var.time_local
log["upstream_addr"] = ngx.var.upstream_addr
log["upstream_status"] = ngx.var.upstream_status
log["upstream_cache_status"] = ngx.var.upstream_cache_status
log["cookie"] = ngx.var.http_cookie
log["request_id"] = request_id
log["uri"] = ngx.var.uri
log["request_uri"] = ngx.var.request_uri
log["query_string"] = ngx.var.query_string
log["request"]  = ngx.var.request
log["size"] = ngx.var.body_bytes_sent
log["request_length"] = ngx.var.request_length
log["request_method"] = ngx.var.request_method
log["server_addr"] = ngx.var.server_addr
log["args"] = ngx.var.args
log["host"] = ngx.var.host
log["request_body"] = ngx.var.request_body
log["remote_addr"] = ngx.var.remote_addr
log["remote_user"] = ngx.var.remote_user
log["time_local"] = ngx.var.time_local
log["status"] = ngx.var.status
log["body_bytes_sent"] = ngx.var.body_bytes_sent
log["http_referer"] = ngx.var.http_referer
log["http_user_agent"] = ngx.var.http_user_agent
log["http_x_forwarded_for"] = ngx.var.http_x_forwarded_for
log["upstream_response_time"] = ngx.var.upstream_response_time
log["request_time"] = ngx.var.request_time



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
    local success, err, forcible = useragent:set(http_user_agent, ua)
end
log["useragent"] = ua

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
    local success, err, forcible = ip2location:set(remote_addr, ip_data)
end

log["ip_data"] = ip_data



local geoip = ngx.shared.geoip
local geoip_data, flags, stale = geoip:get_stale(remote_addr)
if not geoip_data then
    local geo = geo
    local cjson = cjson
    local geoip_data, err = geo:lookup(remote_addr)
    if not geoip_data then
        geoip_data = {}
    end
    local success, err, forcible = geoip:set(remote_addr, geoip_data)
end

log["geoip_data"] = geoip_data



local ck = ck
local cookie, err = ck:new()
local cookie_fields, err = cookie:get_all()
if not cookie_fields then
    cookie_fields = {}
end

log["cookies"] = cookie_fields



local referer = ngx.var.http_referer
local url = url
log["referers"] = url.parse(referer)

log["headers"] = ngx.req.get_headers()
log["uri_args"] = ngx.req.get_uri_args()
log["raw_reader"] = ngx.req.raw_header()
log["body_data"] = ngx.req.get_body_data()
log["body"] = ngx.req.read_body()

local message = cjson.encode(log)

local bp = producer:new(broker_list, { producer_type = "async", api_version = 2 })
local ok, err = bp:send("access_log", request_id, message)

if not ok then
    ngx.log(ngx.ERR, "kafka send err:", err)
    return
end