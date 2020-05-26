local patterns = require("resty.uap.patterns")

local user_agent_parser = {}

local function map(xs, f)
    local rs = {}
    for i = 1, #xs do
        rs[i] = f(xs[i])
    end
    return rs
end

local function compact(xs)
    local rs = {}
    for i = 1, #xs do
        if xs[i] ~= false then rs[i] = xs[i] else rs[i] = "" end
    end
    return rs
end

local function strip(str)
    if type(str) == "string" then
        str = str:match("^%s*(.-)%s*$")
        if str == "" then return nil else return str end
    else
        return str
    end
end

local function esc_percent(x)
    local r, _ = x:gsub("%%", "%%%%")
    return r
end

local function first_pattern_match(patterns_to_match, value)
    for _, pattern in ipairs(patterns_to_match) do
        local match = { pattern.regex_compiled:match(value) }
        if match[1] or match[2] or match[3] then
            return pattern, match
        end
    end

    return nil
end

local function parser_os(user_agent)
    local pattern, match = first_pattern_match(patterns.os_parsers, user_agent)

    if not pattern then
        return {
            family = "Other"
        }
    else
        match = map(compact(match), tostring)

        local family = match[1]
        local major = match[2]
        local minor = match[3]
        local patch = match[4]
        local patch_minor = match[5]

        if pattern.os_replacement then
            family = pattern.os_replacement
            family = family:gsub("$1", match[1])
        end

        if pattern.os_v1_replacement then
            major = pattern.os_v1_replacement

            for i, m in ipairs(match) do
                major = major:gsub("$" .. i, m)
            end
        end

        if pattern.os_v2_replacement then
            minor = pattern.os_v2_replacement
            for i, m in ipairs(match) do
                minor = minor:gsub("$" .. i, m)
            end
        end

        if pattern.os_v3_replacement then
            patch = pattern.os_v3_replacement
            for i, m in ipairs(match) do
                patch = patch:gsub("$" .. i, m)
            end
        end

        if pattern.os_v4_replacement then
            patch_minor = pattern.os_v4_replacement
            for i, m in ipairs(match) do
                patch_minor = patch_minor:gsub("$" .. i, m)
            end
        end

        return {
            family = family,
            major = strip(major),
            minor = strip(minor),
            patch = strip(patch),
            patch_minor = strip(patch_minor),
        }
    end
end

local function parser_device(user_agent)
    local pattern, match = first_pattern_match(patterns.device_parsers, user_agent)

    if not pattern then
        return {
            family = "Other"
        }
    else
        match = map(compact(match), tostring)

        local family = match[1]
        local model
        local brand

        if pattern.regex_compiled:patterninfo()["CAPTURECOUNT"] > 0 then
            model = match[1]
        end

        if pattern.device_replacement then
            family = pattern.device_replacement
            for i, m in ipairs(match) do
                family = family:gsub("$" .. i, esc_percent(m))
            end
        end

        if pattern.model_replacement then
            model = pattern.model_replacement
            for i, m in ipairs(match) do
                model = model:gsub("$" .. i, esc_percent(m))
            end
        end

        if pattern.brand_replacement then
            brand = pattern.brand_replacement
            for i, m in ipairs(match) do
                brand = brand:gsub("$" .. i, esc_percent(m))
            end
        end

        return {
            family = strip(family),
            model = strip(model),
            brand = strip(brand)
        }
    end
end

local function parser_ua(user_agent, os, device)
    local pattern, match = first_pattern_match(patterns.user_agent_parsers, user_agent)
    local family
    local major
    local minor
    local patch

    if pattern then
        match = map(compact(match), tostring)

        family = match[1]
        major = match[2]
        minor = match[3]
        patch = match[4]

        if pattern.family_replacement then
            family = pattern.family_replacement
            family = family:gsub("$1", match[1])
        end

        if pattern.v1_replacement then
            major = pattern.v1_replacement

            for i, m in ipairs(match) do
                major = major:gsub("$" .. i, m)
            end
        end

        if pattern.v2_replacement then
            minor = pattern.v2_replacement
            for i, m in ipairs(match) do
                minor = minor:gsub("$" .. i, m)
            end
        end

        if pattern.v3_replacement then
            patch = pattern.v3_replacement
            for i, m in ipairs(match) do
                patch = patch:gsub("$" .. i, m)
            end
        end
    end

    return {
        string = user_agent,
        ua = {
            family = family or "Other",
            major = strip(major),
            minor = strip(minor),
            patch = strip(patch),
        },
        os = os,
        device = device,
    }
end

function user_agent_parser.parse(user_agent)
    local os = parser_os(user_agent)
    local device = parser_device(user_agent)

    return parser_ua(user_agent, os, device)
end

return user_agent_parser