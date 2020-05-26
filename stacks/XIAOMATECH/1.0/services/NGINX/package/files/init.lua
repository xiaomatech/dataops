local ipip = require "resty.ipip.client"
cjson = require "cjson"
local opts = {
        path = "/usr/local/openresty/nginx/conf/vendor/ip2location.datx",
        token = "your token",
        timeout  = "2000",
}
ipipc = ipip:new(opts)

geo = require 'resty.maxminddb'
if not geo.initted() then
    geo.init("/usr/share/GeoIP/GeoLite2-City.mmdb")
end

woothee = require "resty.woothee"

ck = require "resty.cookie"

url = require 'resty.url'