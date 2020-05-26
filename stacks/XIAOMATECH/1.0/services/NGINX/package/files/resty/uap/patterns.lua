local lrex = require("rex_pcre2")

return {
    device_parsers = {
        {
            brand_replacement = "Spider",
            device_replacement = "Spider",
            model_replacement = "Smartphone",
            regex = "(?:(?:iPhone|Windows CE|Windows Phone|Android).*(?:(?:Bot|Yeti)-Mobile|YRSpider|BingPreview|bots?/\\d|(?:bot|spider)\\.html)|AdsBot-Google-Mobile.*iPhone)",
            regex_compiled = lrex.new('(?:(?:iPhone|Windows CE|Windows Phone|Android).*(?:(?:Bot|Yeti)-Mobile|YRSpider|BingPreview|bots?/\\d|(?:bot|spider)\\.html)|AdsBot-Google-Mobile.*iPhone)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Spider",
            device_replacement = "Spider",
            model_replacement = "Feature Phone",
            regex = "(?:DoCoMo|\\bMOT\\b|\\bLG\\b|Nokia|Samsung|SonyEricsson).*(?:(?:Bot|Yeti)-Mobile|bots?/\\d|(?:bot|crawler)\\.html|(?:jump|google|Wukong)bot|ichiro/mobile|/spider|YahooSeeker)",
            regex_compiled = lrex.new('(?:DoCoMo|\\bMOT\\b|\\bLG\\b|Nokia|Samsung|SonyEricsson).*(?:(?:Bot|Yeti)-Mobile|bots?/\\d|(?:bot|crawler)\\.html|(?:jump|google|Wukong)bot|ichiro/mobile|/spider|YahooSeeker)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "\\bSmartWatch *\\( *([^;]+) *; *([^;]+) *;",
            regex_compiled = lrex.new('\\bSmartWatch *\\( *([^;]+) *; *([^;]+) *;', 'cf')
        }, {
            brand_replacement = "$1$2",
            device_replacement = "$1 $2",
            model_replacement = "$3",
            regex = "Android Application[^\\-]+ - (Sony) ?(Ericsson)? (.+) \\w+ - ",
            regex_compiled = lrex.new('Android Application[^\\-]+ - (Sony) ?(Ericsson)? (.+) \\w+ - ', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "Android Application[^\\-]+ - (?:HTC|HUAWEI|LGE|LENOVO|MEDION|TCT) (HTC|HUAWEI|LG|LENOVO|MEDION|ALCATEL)[ _\\-](.+) \\w+ - ",
            regex_compiled = lrex.new('Android Application[^\\-]+ - (?:HTC|HUAWEI|LGE|LENOVO|MEDION|TCT) (HTC|HUAWEI|LG|LENOVO|MEDION|ALCATEL)[ _\\-](.+) \\w+ - ', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "Android Application[^\\-]+ - ([^ ]+) (.+) \\w+ - ",
            regex_compiled = lrex.new('Android Application[^\\-]+ - ([^ ]+) (.+) \\w+ - ', 'cf')
        }, {
            brand_replacement = "3Q",
            device_replacement = "3Q $1",
            model_replacement = "$1",
            regex = "; *([BLRQ]C\\d{4}[A-Z]+) +Build/",
            regex_compiled = lrex.new('; *([BLRQ]C\\d{4}[A-Z]+) +Build/', 'cf')
        }, {
            brand_replacement = "3Q",
            device_replacement = "3Q $1",
            model_replacement = "$1",
            regex = "; *(?:3Q_)([^;/]+) +Build",
            regex_compiled = lrex.new('; *(?:3Q_)([^;/]+) +Build', 'cf')
        }, {
            brand_replacement = "Acer",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "Android [34].*; *(A100|A101|A110|A200|A210|A211|A500|A501|A510|A511|A700(?: Lite| 3G)?|A701|B1-A71|A1-\\d{3}|B1-\\d{3}|V360|V370|W500|W500P|W501|W501P|W510|W511|W700|Slider SL101|DA22[^;/]+) Build",
            regex_compiled = lrex.new('Android [34].*; *(A100|A101|A110|A200|A210|A211|A500|A501|A510|A511|A700(?: Lite| 3G)?|A701|B1-A71|A1-\\d{3}|B1-\\d{3}|V360|V370|W500|W500P|W501|W501P|W510|W511|W700|Slider SL101|DA22[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Acer",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *Acer Iconia Tab ([^;/]+) Build",
            regex_compiled = lrex.new('; *Acer Iconia Tab ([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Acer",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(Z1[1235]0|E320[^/]*|S500|S510|Liquid[^;/]*|Iconia A\\d+) Build",
            regex_compiled = lrex.new('; *(Z1[1235]0|E320[^/]*|S500|S510|Liquid[^;/]*|Iconia A\\d+) Build', 'cf')
        }, {
            brand_replacement = "Acer",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(Acer |ACER )([^;/]+) Build",
            regex_compiled = lrex.new('; *(Acer |ACER )([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Advent",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(Advent )?(Vega(?:Bean|Comb)?).* Build",
            regex_compiled = lrex.new('; *(Advent )?(Vega(?:Bean|Comb)?).* Build', 'cf')
        }, {
            brand_replacement = "Ainol",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(Ainol )?((?:NOVO|[Nn]ovo)[^;/]+) Build",
            regex_compiled = lrex.new('; *(Ainol )?((?:NOVO|[Nn]ovo)[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Airis",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *AIRIS[ _\\-]?([^/;\\)]+) *(?:;|\\)|Build)",
            regex_compiled = lrex.new('; *AIRIS[ _\\-]?([^/;\\)]+) *(?:;|\\)|Build)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Airis",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(OnePAD[^;/]+) Build",
            regex_compiled = lrex.new('; *(OnePAD[^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Airpad",
            device_replacement = "Airpad $1",
            model_replacement = "$1",
            regex = "; *Airpad[ \\-]([^;/]+) Build",
            regex_compiled = lrex.new('; *Airpad[ \\-]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Alcatel",
            device_replacement = "Alcatel One Touch $2",
            model_replacement = "One Touch $2",
            regex = "; *(one ?touch) (EVO7|T10|T20) Build",
            regex_compiled = lrex.new('; *(one ?touch) (EVO7|T10|T20) Build', 'cf')
        }, {
            brand_replacement = "Alcatel",
            device_replacement = "Alcatel One Touch $1",
            model_replacement = "One Touch $1",
            regex = "; *(?:alcatel[ _])?(?:(?:one[ _]?touch[ _])|ot[ \\-])([^;/]+);? Build",
            regex_compiled = lrex.new('; *(?:alcatel[ _])?(?:(?:one[ _]?touch[ _])|ot[ \\-])([^;/]+);? Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(TCL)[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *(TCL)[ _]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Alcatel",
            device_replacement = "Alcatel $1",
            model_replacement = "$1",
            regex = "; *(Vodafone Smart II|Optimus_Madrid) Build",
            regex_compiled = lrex.new('; *(Vodafone Smart II|Optimus_Madrid) Build', 'cf')
        }, {
            brand_replacement = "Alcatel",
            device_replacement = "Alcatel One Touch 998",
            model_replacement = "One Touch 998",
            regex = "; *BASE_Lutea_3 Build",
            regex_compiled = lrex.new('; *BASE_Lutea_3 Build', 'cf')
        }, {
            brand_replacement = "Alcatel",
            device_replacement = "Alcatel One Touch 918D",
            model_replacement = "One Touch 918D",
            regex = "; *BASE_Varia Build",
            regex_compiled = lrex.new('; *BASE_Varia Build', 'cf')
        }, {
            brand_replacement = "Allfine",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *((?:FINE|Fine)\\d[^;/]+) Build",
            regex_compiled = lrex.new('; *((?:FINE|Fine)\\d[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Allview",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(ALLVIEW[ _]?|Allview[ _]?)((?:Speed|SPEED).*) Build/",
            regex_compiled = lrex.new('; *(ALLVIEW[ _]?|Allview[ _]?)((?:Speed|SPEED).*) Build/', 'cf')
        }, {
            brand_replacement = "Allview",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(ALLVIEW[ _]?|Allview[ _]?)?(AX1_Shine|AX2_Frenzy) Build",
            regex_compiled = lrex.new('; *(ALLVIEW[ _]?|Allview[ _]?)?(AX1_Shine|AX2_Frenzy) Build', 'cf')
        }, {
            brand_replacement = "Allview",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(ALLVIEW[ _]?|Allview[ _]?)([^;/]*) Build",
            regex_compiled = lrex.new('; *(ALLVIEW[ _]?|Allview[ _]?)([^;/]*) Build', 'cf')
        }, {
            brand_replacement = "Allwinner",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(A13-MID) Build",
            regex_compiled = lrex.new('; *(A13-MID) Build', 'cf')
        }, {
            brand_replacement = "Allwinner",
            device_replacement = "$1 $2",
            model_replacement = "$1",
            regex = "; *(Allwinner)[ _\\-]?([^;/]+) Build",
            regex_compiled = lrex.new('; *(Allwinner)[ _\\-]?([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Amaway",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(A651|A701B?|A702|A703|A705|A706|A707|A711|A712|A713|A717|A722|A785|A801|A802|A803|A901|A902|A1002|A1003|A1006|A1007|A9701|A9703|Q710|Q80) Build",
            regex_compiled = lrex.new('; *(A651|A701B?|A702|A703|A705|A706|A707|A711|A712|A713|A717|A722|A785|A801|A802|A803|A901|A902|A1002|A1003|A1006|A1007|A9701|A9703|Q710|Q80) Build', 'cf')
        }, {
            brand_replacement = "Amoi",
            device_replacement = "Amoi $1",
            model_replacement = "$1",
            regex = "; *(?:AMOI|Amoi)[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *(?:AMOI|Amoi)[ _]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Amoi",
            device_replacement = "Amoi $1",
            model_replacement = "$1",
            regex = "^(?:AMOI|Amoi)[ _]([^;/]+) Linux",
            regex_compiled = lrex.new('^(?:AMOI|Amoi)[ _]([^;/]+) Linux', 'cf')
        }, {
            brand_replacement = "Aoc",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(MW(?:0[789]|10)[^;/]+) Build",
            regex_compiled = lrex.new('; *(MW(?:0[789]|10)[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Aoson",
            device_replacement = "Aoson $1",
            model_replacement = "$1",
            regex = "; *(G7|M1013|M1015G|M11[CG]?|M-?12[B]?|M15|M19[G]?|M30[ACQ]?|M31[GQ]|M32|M33[GQ]|M36|M37|M38|M701T|M710|M712B|M713|M715G|M716G|M71(?:G|GS|T)?|M72[T]?|M73[T]?|M75[GT]?|M77G|M79T|M7L|M7LN|M81|M810|M81T|M82|M92|M92KS|M92S|M717G|M721|M722G|M723|M725G|M739|M785|M791|M92SK|M93D) Build",
            regex_compiled = lrex.new('; *(G7|M1013|M1015G|M11[CG]?|M-?12[B]?|M15|M19[G]?|M30[ACQ]?|M31[GQ]|M32|M33[GQ]|M36|M37|M38|M701T|M710|M712B|M713|M715G|M716G|M71(?:G|GS|T)?|M72[T]?|M73[T]?|M75[GT]?|M77G|M79T|M7L|M7LN|M81|M810|M81T|M82|M92|M92KS|M92S|M717G|M721|M722G|M723|M725G|M739|M785|M791|M92SK|M93D) Build', 'cf')
        }, {
            brand_replacement = "Aoson",
            device_replacement = "Aoson $1",
            model_replacement = "$1",
            regex = "; *Aoson ([^;/]+) Build",
            regex_compiled = lrex.new('; *Aoson ([^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Apanda",
            device_replacement = "Apanda $1",
            model_replacement = "$1",
            regex = "; *[Aa]panda[ _\\-]([^;/]+) Build",
            regex_compiled = lrex.new('; *[Aa]panda[ _\\-]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Archos",
            device_replacement = "Archos $1",
            model_replacement = "$1",
            regex = "; *(?:ARCHOS|Archos) ?(GAMEPAD.*?)(?: Build|[;/\\(\\)\\-])",
            regex_compiled = lrex.new('; *(?:ARCHOS|Archos) ?(GAMEPAD.*?)(?: Build|[;/\\(\\)\\-])', 'cf')
        }, {
            brand_replacement = "Archos",
            device_replacement = "Archos $1",
            model_replacement = "$1",
            regex = "ARCHOS; GOGI; ([^;]+);",
            regex_compiled = lrex.new('ARCHOS; GOGI; ([^;]+);', 'cf')
        }, {
            brand_replacement = "Archos",
            device_replacement = "Archos $1",
            model_replacement = "$1",
            regex = "(?:ARCHOS|Archos)[ _]?(.*?)(?: Build|[;/\\(\\)\\-]|$)",
            regex_compiled = lrex.new('(?:ARCHOS|Archos)[ _]?(.*?)(?: Build|[;/\\(\\)\\-]|$)', 'cf')
        }, {
            brand_replacement = "Archos",
            device_replacement = "Archos $1",
            model_replacement = "$1",
            regex = "; *(AN(?:7|8|9|10|13)[A-Z0-9]{1,4}) Build",
            regex_compiled = lrex.new('; *(AN(?:7|8|9|10|13)[A-Z0-9]{1,4}) Build', 'cf')
        }, {
            brand_replacement = "Archos",
            device_replacement = "Archos $1",
            model_replacement = "$1",
            regex = "; *(A28|A32|A43|A70(?:BHT|CHT|HB|S|X)|A101(?:B|C|IT)|A7EB|A7EB-WK|101G9|80G9) Build",
            regex_compiled = lrex.new('; *(A28|A32|A43|A70(?:BHT|CHT|HB|S|X)|A101(?:B|C|IT)|A7EB|A7EB-WK|101G9|80G9) Build', 'cf')
        }, {
            brand_replacement = "Arival",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(PAD-FMD[^;/]+) Build",
            regex_compiled = lrex.new('; *(PAD-FMD[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Arival",
            device_replacement = "$1 $2",
            model_replacement = "$1 $2",
            regex = "; *(BioniQ) ?([^;/]+) Build",
            regex_compiled = lrex.new('; *(BioniQ) ?([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Arnova",
            device_replacement = "Arnova $1",
            model_replacement = "$1",
            regex = "; *(AN\\d[^;/]+|ARCHM\\d+) Build",
            regex_compiled = lrex.new('; *(AN\\d[^;/]+|ARCHM\\d+) Build', 'cf')
        }, {
            brand_replacement = "Arnova",
            device_replacement = "Arnova $1",
            model_replacement = "$1",
            regex = "; *(?:ARNOVA|Arnova) ?([^;/]+) Build",
            regex_compiled = lrex.new('; *(?:ARNOVA|Arnova) ?([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Assistant",
            device_replacement = "Assistant $1-$2",
            model_replacement = "$1-$2",
            regex = "; *(?:ASSISTANT )?(AP)-?([1789]\\d{2}[A-Z]{0,2}|80104) Build",
            regex_compiled = lrex.new('; *(?:ASSISTANT )?(AP)-?([1789]\\d{2}[A-Z]{0,2}|80104) Build', 'cf')
        }, {
            brand_replacement = "Asus",
            device_replacement = "Asus $1",
            model_replacement = "$1",
            regex = "; *(ME17\\d[^;/]*|ME3\\d{2}[^;/]+|K00[A-Z]|Nexus 10|Nexus 7(?: 2013)?|PadFone[^;/]*|Transformer[^;/]*|TF\\d{3}[^;/]*|eeepc) Build",
            regex_compiled = lrex.new('; *(ME17\\d[^;/]*|ME3\\d{2}[^;/]+|K00[A-Z]|Nexus 10|Nexus 7(?: 2013)?|PadFone[^;/]*|Transformer[^;/]*|TF\\d{3}[^;/]*|eeepc) Build', 'cf')
        }, {
            brand_replacement = "Asus",
            device_replacement = "Asus $1",
            model_replacement = "$1",
            regex = "; *ASUS[ _]*([^;/]+) Build",
            regex_compiled = lrex.new('; *ASUS[ _]*([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Garmin-Asus",
            device_replacement = "Garmin-Asus $1",
            model_replacement = "$1",
            regex = "; *Garmin-Asus ([^;/]+) Build",
            regex_compiled = lrex.new('; *Garmin-Asus ([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Garmin-Asus",
            device_replacement = "Garmin $1",
            model_replacement = "$1",
            regex = "; *(Garminfone) Build",
            regex_compiled = lrex.new('; *(Garminfone) Build', 'cf')
        }, {
            brand_replacement = "Attab",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; (@TAB-[^;/]+) Build",
            regex_compiled = lrex.new('; (@TAB-[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Audiosonic",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(T-(?:07|[^0]\\d)[^;/]+) Build",
            regex_compiled = lrex.new('; *(T-(?:07|[^0]\\d)[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Axioo",
            device_replacement = "Axioo $1$2 $3",
            model_replacement = "$1$2 $3",
            regex = "; *(?:Axioo[ _\\-]([^;/]+)|(picopad)[ _\\-]([^;/]+)) Build",
            regex_compiled = lrex.new('; *(?:Axioo[ _\\-]([^;/]+)|(picopad)[ _\\-]([^;/]+)) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Azend",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(V(?:100|700|800)[^;/]*) Build",
            regex_compiled = lrex.new('; *(V(?:100|700|800)[^;/]*) Build', 'cf')
        }, {
            brand_replacement = "Bak",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(IBAK\\-[^;/]*) Build",
            regex_compiled = lrex.new('; *(IBAK\\-[^;/]*) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Bedove",
            device_replacement = "Bedove $1",
            model_replacement = "$1",
            regex = "; *(HY5001|HY6501|X12|X21|I5) Build",
            regex_compiled = lrex.new('; *(HY5001|HY6501|X12|X21|I5) Build', 'cf')
        }, {
            brand_replacement = "Benss",
            device_replacement = "Benss $1",
            model_replacement = "$1",
            regex = "; *(JC-[^;/]*) Build",
            regex_compiled = lrex.new('; *(JC-[^;/]*) Build', 'cf')
        }, {
            brand_replacement = "Blackberry",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(BB) ([^;/]+) Build",
            regex_compiled = lrex.new('; *(BB) ([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(BlackBird)[ _](I8.*) Build",
            regex_compiled = lrex.new('; *(BlackBird)[ _](I8.*) Build', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(BlackBird)[ _](.*) Build",
            regex_compiled = lrex.new('; *(BlackBird)[ _](.*) Build', 'cf')
        }, {
            brand_replacement = "Blaupunkt",
            device_replacement = "Blaupunkt $1",
            model_replacement = "$1",
            regex = "; *([0-9]+BP[EM][^;/]*|Endeavour[^;/]+) Build",
            regex_compiled = lrex.new('; *([0-9]+BP[EM][^;/]*|Endeavour[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Blu",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *((?:BLU|Blu)[ _\\-])([^;/]+) Build",
            regex_compiled = lrex.new('; *((?:BLU|Blu)[ _\\-])([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Blu",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(?:BMOBILE )?(Blu|BLU|DASH [^;/]+|VIVO 4\\.3|TANK 4\\.5) Build",
            regex_compiled = lrex.new('; *(?:BMOBILE )?(Blu|BLU|DASH [^;/]+|VIVO 4\\.3|TANK 4\\.5) Build', 'cf')
        }, {
            brand_replacement = "Blusens",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(TOUCH\\d[^;/]+) Build",
            regex_compiled = lrex.new('; *(TOUCH\\d[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Bmobile",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(AX5\\d+) Build",
            regex_compiled = lrex.new('; *(AX5\\d+) Build', 'cf')
        }, {
            brand_replacement = "bq",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *([Bb]q) ([^;/]+);? Build",
            regex_compiled = lrex.new('; *([Bb]q) ([^;/]+);? Build', 'cf')
        }, {
            brand_replacement = "bq",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(Maxwell [^;/]+) Build",
            regex_compiled = lrex.new('; *(Maxwell [^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Braun",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *((?:B-Tab|B-TAB) ?\\d[^;/]+) Build",
            regex_compiled = lrex.new('; *((?:B-Tab|B-TAB) ?\\d[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(Broncho) ([^;/]+) Build",
            regex_compiled = lrex.new('; *(Broncho) ([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Captiva",
            device_replacement = "Captiva $1",
            model_replacement = "$1",
            regex = "; *CAPTIVA ([^;/]+) Build",
            regex_compiled = lrex.new('; *CAPTIVA ([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Casio",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(C771|CAL21|IS11CA) Build",
            regex_compiled = lrex.new('; *(C771|CAL21|IS11CA) Build', 'cf')
        }, {
            brand_replacement = "Cat",
            device_replacement = "Cat $1",
            model_replacement = "$1",
            regex = "; *(?:Cat|CAT) ([^;/]+) Build",
            regex_compiled = lrex.new('; *(?:Cat|CAT) ([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Cat",
            device_replacement = "Cat $1",
            model_replacement = "$1",
            regex = "; *(?:Cat)(Nova.*) Build",
            regex_compiled = lrex.new('; *(?:Cat)(Nova.*) Build', 'cf')
        }, {
            brand_replacement = "Cat",
            device_replacement = "$1",
            model_replacement = "Tablet PHOENIX 8.1J0",
            regex = "; *(INM8002KP|ADM8000KP_[AB]) Build",
            regex_compiled = lrex.new('; *(INM8002KP|ADM8000KP_[AB]) Build', 'cf')
        }, {
            brand_replacement = "Celkon",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(?:[Cc]elkon[ _\\*]|CELKON[ _\\*])([^;/\\)]+) ?(?:Build|;|\\))",
            regex_compiled = lrex.new('; *(?:[Cc]elkon[ _\\*]|CELKON[ _\\*])([^;/\\)]+) ?(?:Build|;|\\))', 'cf')
        }, {
            brand_replacement = "Celkon",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "Build/(?:[Cc]elkon)+_?([^;/_\\)]+)",
            regex_compiled = lrex.new('Build/(?:[Cc]elkon)+_?([^;/_\\)]+)', 'cf')
        }, {
            brand_replacement = "Celkon",
            device_replacement = "$1$2",
            model_replacement = "$1$2",
            regex = "; *(CT)-?(\\d+) Build",
            regex_compiled = lrex.new('; *(CT)-?(\\d+) Build', 'cf')
        }, {
            brand_replacement = "Celkon",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(A19|A19Q|A105|A107[^;/\\)]*) ?(?:Build|;|\\))",
            regex_compiled = lrex.new('; *(A19|A19Q|A105|A107[^;/\\)]*) ?(?:Build|;|\\))', 'cf')
        }, {
            brand_replacement = "ChangJia",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(TPC[0-9]{4,5}) Build",
            regex_compiled = lrex.new('; *(TPC[0-9]{4,5}) Build', 'cf')
        }, {
            brand_replacement = "Cloudfone",
            device_replacement = "$1 $2 $3",
            model_replacement = "$1 $2 $3",
            regex = "; *(Cloudfone)[ _](Excite)([^ ][^;/]+) Build",
            regex_compiled = lrex.new('; *(Cloudfone)[ _](Excite)([^ ][^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Cloudfone",
            device_replacement = "Cloudfone $1 $2",
            model_replacement = "Cloudfone $1 $2",
            regex = "; *(Excite|ICE)[ _](\\d+[^;/]+) Build",
            regex_compiled = lrex.new('; *(Excite|ICE)[ _](\\d+[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Cloudfone",
            device_replacement = "$1 $2",
            model_replacement = "$1 $2",
            regex = "; *(Cloudfone|CloudPad)[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *(Cloudfone|CloudPad)[ _]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Cmx",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *((?:Aquila|Clanga|Rapax)[^;/]+) Build",
            regex_compiled = lrex.new('; *((?:Aquila|Clanga|Rapax)[^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "CobyKyros",
            device_replacement = "CobyKyros $1$2",
            model_replacement = "$1$2",
            regex = "; *(?:CFW-|Kyros )?(MID[0-9]{4}(?:[ABC]|SR|TV)?)(\\(3G\\)-4G| GB 8K| 3G| 8K| GB)? *(?:Build|[;\\)])",
            regex_compiled = lrex.new('; *(?:CFW-|Kyros )?(MID[0-9]{4}(?:[ABC]|SR|TV)?)(\\(3G\\)-4G| GB 8K| 3G| 8K| GB)? *(?:Build|[;\\)])', 'cf')
        }, {
            brand_replacement = "Coolpad",
            device_replacement = "$1$2",
            model_replacement = "$1$2",
            regex = "; *([^;/]*)Coolpad[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *([^;/]*)Coolpad[ _]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Cube",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(CUBE[ _])?([KU][0-9]+ ?GT.*|A5300) Build",
            regex_compiled = lrex.new('; *(CUBE[ _])?([KU][0-9]+ ?GT.*|A5300) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Cubot",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *CUBOT ([^;/]+) Build",
            regex_compiled = lrex.new('; *CUBOT ([^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Cubot",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(BOBBY) Build",
            regex_compiled = lrex.new('; *(BOBBY) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Danew",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(Dslide [^;/]+) Build",
            regex_compiled = lrex.new('; *(Dslide [^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Dell",
            device_replacement = "Dell $1$2",
            model_replacement = "$1$2",
            regex = "; *(XCD)[ _]?(28|35) Build",
            regex_compiled = lrex.new('; *(XCD)[ _]?(28|35) Build', 'cf')
        }, {
            brand_replacement = "Dell",
            device_replacement = "Dell $1",
            model_replacement = "Streak",
            regex = "; *(001DL) Build",
            regex_compiled = lrex.new('; *(001DL) Build', 'cf')
        }, {
            brand_replacement = "Dell",
            device_replacement = "Dell $1",
            model_replacement = "Streak",
            regex = "; *(?:Dell|DELL) (Streak) Build",
            regex_compiled = lrex.new('; *(?:Dell|DELL) (Streak) Build', 'cf')
        }, {
            brand_replacement = "Dell",
            device_replacement = "Dell $1",
            model_replacement = "Streak Pro",
            regex = "; *(101DL|GS01|Streak Pro[^;/]*) Build",
            regex_compiled = lrex.new('; *(101DL|GS01|Streak Pro[^;/]*) Build', 'cf')
        }, {
            brand_replacement = "Dell",
            device_replacement = "Dell $1",
            model_replacement = "Streak 7",
            regex = "; *([Ss]treak ?7) Build",
            regex_compiled = lrex.new('; *([Ss]treak ?7) Build', 'cf')
        }, {
            brand_replacement = "Dell",
            device_replacement = "Dell $1",
            model_replacement = "$1",
            regex = "; *(Mini-3iX) Build",
            regex_compiled = lrex.new('; *(Mini-3iX) Build', 'cf')
        }, {
            brand_replacement = "Dell",
            device_replacement = "Dell $1",
            model_replacement = "$1",
            regex = "; *(?:Dell|DELL)[ _](Aero|Venue|Thunder|Mini.*|Streak[ _]Pro) Build",
            regex_compiled = lrex.new('; *(?:Dell|DELL)[ _](Aero|Venue|Thunder|Mini.*|Streak[ _]Pro) Build', 'cf')
        }, {
            brand_replacement = "Dell",
            device_replacement = "Dell $1",
            model_replacement = "$1",
            regex = "; *Dell[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *Dell[ _]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Dell",
            device_replacement = "Dell $1",
            model_replacement = "$1",
            regex = "; *Dell ([^;/]+) Build",
            regex_compiled = lrex.new('; *Dell ([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Denver",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(TA[CD]-\\d+[^;/]*) Build",
            regex_compiled = lrex.new('; *(TA[CD]-\\d+[^;/]*) Build', 'cf')
        }, {
            brand_replacement = "Dex",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(iP[789]\\d{2}(?:-3G)?|IP10\\d{2}(?:-8GB)?) Build",
            regex_compiled = lrex.new('; *(iP[789]\\d{2}(?:-3G)?|IP10\\d{2}(?:-8GB)?) Build', 'cf')
        }, {
            brand_replacement = "DNS",
            device_replacement = "$1 $2",
            model_replacement = "$1 $2",
            regex = "; *(AirTab)[ _\\-]([^;/]+) Build",
            regex_compiled = lrex.new('; *(AirTab)[ _\\-]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Fujitsu",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(F\\-\\d[^;/]+) Build",
            regex_compiled = lrex.new('; *(F\\-\\d[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "$1",
            model_replacement = "Magic",
            regex = "; *(HT-03A) Build",
            regex_compiled = lrex.new('; *(HT-03A) Build', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(HT\\-\\d[^;/]+) Build",
            regex_compiled = lrex.new('; *(HT\\-\\d[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "LG",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(L\\-\\d[^;/]+) Build",
            regex_compiled = lrex.new('; *(L\\-\\d[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Nec",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(N\\-\\d[^;/]+) Build",
            regex_compiled = lrex.new('; *(N\\-\\d[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Panasonic",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(P\\-\\d[^;/]+) Build",
            regex_compiled = lrex.new('; *(P\\-\\d[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(SC\\-\\d[^;/]+) Build",
            regex_compiled = lrex.new('; *(SC\\-\\d[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Sharp",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(SH\\-\\d[^;/]+) Build",
            regex_compiled = lrex.new('; *(SH\\-\\d[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "SonyEricsson",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(SO\\-\\d[^;/]+) Build",
            regex_compiled = lrex.new('; *(SO\\-\\d[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Toshiba",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(T\\-0[12][^;/]+) Build",
            regex_compiled = lrex.new('; *(T\\-0[12][^;/]+) Build', 'cf')
        }, {
            brand_replacement = "DOOV",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(DOOV)[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *(DOOV)[ _]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Enot",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(Enot|ENOT)[ -]?([^;/]+) Build",
            regex_compiled = lrex.new('; *(Enot|ENOT)[ -]?([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Evercoss",
            device_replacement = "CROSS $1",
            model_replacement = "Cross $1",
            regex = "; *[^;/]+ Build/(?:CROSS|Cross)+[ _\\-]([^\\)]+)",
            regex_compiled = lrex.new('; *[^;/]+ Build/(?:CROSS|Cross)+[ _\\-]([^\\)]+)', 'cf')
        }, {
            brand_replacement = "Evercoss",
            device_replacement = "$1 $2",
            model_replacement = "Cross $2",
            regex = "; *(CROSS|Cross)[ _\\-]([^;/]+) Build",
            regex_compiled = lrex.new('; *(CROSS|Cross)[ _\\-]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Explay",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *Explay[_ ](.+?)(?:[\\)]| Build)",
            regex_compiled = lrex.new('; *Explay[_ ](.+?)(?:[\\)]| Build)', 'cf')
        }, {
            brand_replacement = "Fly",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(IQ.*) Build",
            regex_compiled = lrex.new('; *(IQ.*) Build', 'cf')
        }, {
            brand_replacement = "Fly",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(Fly|FLY)[ _](IQ[^;]+|F[34]\\d+[^;]*);? Build",
            regex_compiled = lrex.new('; *(Fly|FLY)[ _](IQ[^;]+|F[34]\\d+[^;]*);? Build', 'cf')
        }, {
            brand_replacement = "Fujitsu",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(M532|Q572|FJL21) Build/",
            regex_compiled = lrex.new('; *(M532|Q572|FJL21) Build/', 'cf')
        }, {
            brand_replacement = "Galapad",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(G1) Build",
            regex_compiled = lrex.new('; *(G1) Build', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(Geeksphone) ([^;/]+) Build",
            regex_compiled = lrex.new('; *(Geeksphone) ([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Gfive",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(G[^F]?FIVE) ([^;/]+) Build",
            regex_compiled = lrex.new('; *(G[^F]?FIVE) ([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Gionee",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(Gionee)[ _\\-]([^;/]+)(?:/[^;/]+)? Build",
            regex_compiled = lrex.new('; *(Gionee)[ _\\-]([^;/]+)(?:/[^;/]+)? Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Gionee",
            device_replacement = "Gionee $1",
            model_replacement = "$1",
            regex = "; *(GN\\d+[A-Z]?|INFINITY_PASSION|Ctrl_V1) Build",
            regex_compiled = lrex.new('; *(GN\\d+[A-Z]?|INFINITY_PASSION|Ctrl_V1) Build', 'cf')
        }, {
            brand_replacement = "Gionee",
            device_replacement = "Gionee $1",
            model_replacement = "$1",
            regex = "; *(E3) Build/JOP40D",
            regex_compiled = lrex.new('; *(E3) Build/JOP40D', 'cf')
        }, {
            brand_replacement = "Gionee",
            device_replacement = "Gionee $1",
            model_replacement = "$1",
            regex = "\\sGIONEE[-\\s_](\\w*)",
            regex_compiled = lrex.new('\\sGIONEE[-\\s_](\\w*)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "GoClever",
            device_replacement = "GoClever $1",
            model_replacement = "$1",
            regex = "; *((?:FONE|QUANTUM|INSIGNIA) \\d+[^;/]*|PLAYTAB) Build",
            regex_compiled = lrex.new('; *((?:FONE|QUANTUM|INSIGNIA) \\d+[^;/]*|PLAYTAB) Build', 'cf')
        }, {
            brand_replacement = "GoClever",
            device_replacement = "GoClever $1",
            model_replacement = "$1",
            regex = "; *GOCLEVER ([^;/]+) Build",
            regex_compiled = lrex.new('; *GOCLEVER ([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Google",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(Glass \\d+) Build",
            regex_compiled = lrex.new('; *(Glass \\d+) Build', 'cf')
        }, {
            brand_replacement = "Google",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(Pixel \\w+) Build",
            regex_compiled = lrex.new('; *(Pixel \\w+) Build', 'cf')
        }, {
            brand_replacement = "Gigabyte",
            device_replacement = "$1 $2",
            model_replacement = "$1 $2",
            regex = "; *(GSmart)[ -]([^/]+) Build",
            regex_compiled = lrex.new('; *(GSmart)[ -]([^/]+) Build', 'cf')
        }, {
            brand_replacement = "Freescale",
            device_replacement = "Freescale $1",
            model_replacement = "$1",
            regex = "; *(imx5[13]_[^/]+) Build",
            regex_compiled = lrex.new('; *(imx5[13]_[^/]+) Build', 'cf')
        }, {
            brand_replacement = "Haier",
            device_replacement = "Haier $1",
            model_replacement = "$1",
            regex = "; *Haier[ _\\-]([^/]+) Build",
            regex_compiled = lrex.new('; *Haier[ _\\-]([^/]+) Build', 'cf')
        }, {
            brand_replacement = "Haipad",
            device_replacement = "Haipad $1",
            model_replacement = "$1",
            regex = "; *(PAD1016) Build",
            regex_compiled = lrex.new('; *(PAD1016) Build', 'cf')
        }, {
            brand_replacement = "Haipad",
            device_replacement = "Haipad $1",
            model_replacement = "$1",
            regex = "; *(M701|M7|M8|M9) Build",
            regex_compiled = lrex.new('; *(M701|M7|M8|M9) Build', 'cf')
        }, {
            brand_replacement = "Hannspree",
            device_replacement = "Hannspree $1",
            model_replacement = "$1",
            regex = "; *(SN\\d+T[^;\\)/]*)(?: Build|[;\\)])",
            regex_compiled = lrex.new('; *(SN\\d+T[^;\\)/]*)(?: Build|[;\\)])', 'cf')
        }, {
            brand_replacement = "HCLme",
            device_replacement = "HCLme $1",
            model_replacement = "$1",
            regex = "Build/HCL ME Tablet ([^;\\)]+)[\\);]",
            regex_compiled = lrex.new('Build/HCL ME Tablet ([^;\\)]+)[\\);]', 'cf')
        }, {
            brand_replacement = "HCLme",
            device_replacement = "HCLme $1",
            model_replacement = "$1",
            regex = "; *([^;\\/]+) Build/HCL",
            regex_compiled = lrex.new('; *([^;\\/]+) Build/HCL', 'cf')
        }, {
            brand_replacement = "Hena",
            device_replacement = "Hena $1",
            model_replacement = "$1",
            regex = "; *(MID-?\\d{4}C[EM]) Build",
            regex_compiled = lrex.new('; *(MID-?\\d{4}C[EM]) Build', 'cf')
        }, {
            brand_replacement = "Hisense",
            device_replacement = "Hisense $1",
            model_replacement = "$1",
            regex = "; *(EG\\d{2,}|HS-[^;/]+|MIRA[^;/]+) Build",
            regex_compiled = lrex.new('; *(EG\\d{2,}|HS-[^;/]+|MIRA[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Hisense",
            device_replacement = "Hisense $1",
            model_replacement = "$1",
            regex = "; *(andromax[^;/]+) Build",
            regex_compiled = lrex.new('; *(andromax[^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "hitech",
            device_replacement = "AMAZE $1$2",
            model_replacement = "AMAZE $1$2",
            regex = "; *(?:AMAZE[ _](S\\d+)|(S\\d+)[ _]AMAZE) Build",
            regex_compiled = lrex.new('; *(?:AMAZE[ _](S\\d+)|(S\\d+)[ _]AMAZE) Build', 'cf')
        }, {
            brand_replacement = "HP",
            device_replacement = "HP $1",
            model_replacement = "$1",
            regex = "; *(PlayBook) Build",
            regex_compiled = lrex.new('; *(PlayBook) Build', 'cf')
        }, {
            brand_replacement = "HP",
            device_replacement = "HP $1",
            model_replacement = "$1",
            regex = "; *HP ([^/]+) Build",
            regex_compiled = lrex.new('; *HP ([^/]+) Build', 'cf')
        }, {
            brand_replacement = "HP",
            device_replacement = "HP TouchPad",
            model_replacement = "TouchPad",
            regex = "; *([^/]+_tenderloin) Build",
            regex_compiled = lrex.new('; *([^/]+_tenderloin) Build', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(HUAWEI |Huawei-)?([UY][^;/]+) Build/(?:Huawei|HUAWEI)([UY][^\\);]+)\\)",
            regex_compiled = lrex.new('; *(HUAWEI |Huawei-)?([UY][^;/]+) Build/(?:Huawei|HUAWEI)([UY][^\\);]+)\\)', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "$1",
            model_replacement = "$2",
            regex = "; *([^;/]+) Build[/ ]Huawei(MT1-U06|[A-Z]+\\d+[^\\);]+)[^\\);]*\\)",
            regex_compiled = lrex.new('; *([^;/]+) Build[/ ]Huawei(MT1-U06|[A-Z]+\\d+[^\\);]+)[^\\);]*\\)', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(S7|M860) Build",
            regex_compiled = lrex.new('; *(S7|M860) Build', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *((?:HUAWEI|Huawei)[ \\-]?)(MediaPad) Build",
            regex_compiled = lrex.new('; *((?:HUAWEI|Huawei)[ \\-]?)(MediaPad) Build', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *((?:HUAWEI[ _]?|Huawei[ _])?Ascend[ _])([^;/]+) Build",
            regex_compiled = lrex.new('; *((?:HUAWEI[ _]?|Huawei[ _])?Ascend[ _])([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *((?:HUAWEI|Huawei)[ _\\-]?)((?:G700-|MT-)[^;/]+) Build",
            regex_compiled = lrex.new('; *((?:HUAWEI|Huawei)[ _\\-]?)((?:G700-|MT-)[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *((?:HUAWEI|Huawei)[ _\\-]?)([^;/]+) Build",
            regex_compiled = lrex.new('; *((?:HUAWEI|Huawei)[ _\\-]?)([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(MediaPad[^;]+|SpringBoard) Build/Huawei",
            regex_compiled = lrex.new('; *(MediaPad[^;]+|SpringBoard) Build/Huawei', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *([^;]+) Build/(?:Huawei|HUAWEI)",
            regex_compiled = lrex.new('; *([^;]+) Build/(?:Huawei|HUAWEI)', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "$1$2",
            model_replacement = "U$2",
            regex = "; *([Uu])([89]\\d{3}) Build",
            regex_compiled = lrex.new('; *([Uu])([89]\\d{3}) Build', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "Huawei Ideos$1",
            model_replacement = "Ideos$1",
            regex = "; *(?:Ideos |IDEOS )(S7) Build",
            regex_compiled = lrex.new('; *(?:Ideos |IDEOS )(S7) Build', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "Huawei Ideos$1",
            model_replacement = "Ideos$1",
            regex = "; *(?:Ideos |IDEOS )([^;/]+\\s*|\\s*)Build",
            regex_compiled = lrex.new('; *(?:Ideos |IDEOS )([^;/]+\\s*|\\s*)Build', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "Huawei $1",
            model_replacement = "$1",
            regex = "; *(Orange Daytona|Pulse|Pulse Mini|Vodafone 858|C8500|C8600|C8650|C8660|Nexus 6P|ATH-.+?) Build[/ ]",
            regex_compiled = lrex.new('; *(Orange Daytona|Pulse|Pulse Mini|Vodafone 858|C8500|C8600|C8650|C8660|Nexus 6P|ATH-.+?) Build[/ ]', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1",
            model_replacement = "$1",
            regex = "; *HTC[ _]([^;]+); Windows Phone",
            regex_compiled = lrex.new('; *HTC[ _]([^;]+); Windows Phone', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1",
            model_replacement = "$1",
            regex = "; *(?:HTC[ _/])+([^ _/]+)(?:[/\\\\]1\\.0 | V|/| +)\\d+\\.\\d[\\d\\.]*(?: *Build|\\))",
            regex_compiled = lrex.new('; *(?:HTC[ _/])+([^ _/]+)(?:[/\\\\]1\\.0 | V|/| +)\\d+\\.\\d[\\d\\.]*(?: *Build|\\))', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1 $2",
            model_replacement = "$1 $2",
            regex = "; *(?:HTC[ _/])+([^ _/]+)(?:[ _/]([^ _/]+))?(?:[/\\\\]1\\.0 | V|/| +)\\d+\\.\\d[\\d\\.]*(?: *Build|\\))",
            regex_compiled = lrex.new('; *(?:HTC[ _/])+([^ _/]+)(?:[ _/]([^ _/]+))?(?:[/\\\\]1\\.0 | V|/| +)\\d+\\.\\d[\\d\\.]*(?: *Build|\\))', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1 $2 $3",
            model_replacement = "$1 $2 $3",
            regex = "; *(?:HTC[ _/])+([^ _/]+)(?:[ _/]([^ _/]+)(?:[ _/]([^ _/]+))?)?(?:[/\\\\]1\\.0 | V|/| +)\\d+\\.\\d[\\d\\.]*(?: *Build|\\))",
            regex_compiled = lrex.new('; *(?:HTC[ _/])+([^ _/]+)(?:[ _/]([^ _/]+)(?:[ _/]([^ _/]+))?)?(?:[/\\\\]1\\.0 | V|/| +)\\d+\\.\\d[\\d\\.]*(?: *Build|\\))', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1 $2 $3 $4",
            model_replacement = "$1 $2 $3 $4",
            regex = "; *(?:HTC[ _/])+([^ _/]+)(?:[ _/]([^ _/]+)(?:[ _/]([^ _/]+)(?:[ _/]([^ _/]+))?)?)?(?:[/\\\\]1\\.0 | V|/| +)\\d+\\.\\d[\\d\\.]*(?: *Build|\\))",
            regex_compiled = lrex.new('; *(?:HTC[ _/])+([^ _/]+)(?:[ _/]([^ _/]+)(?:[ _/]([^ _/]+)(?:[ _/]([^ _/]+))?)?)?(?:[/\\\\]1\\.0 | V|/| +)\\d+\\.\\d[\\d\\.]*(?: *Build|\\))', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1",
            model_replacement = "$1",
            regex = "; *(?:(?:HTC|htc)(?:_blocked)*[ _/])+([^ _/;]+)(?: *Build|[;\\)]| - )",
            regex_compiled = lrex.new('; *(?:(?:HTC|htc)(?:_blocked)*[ _/])+([^ _/;]+)(?: *Build|[;\\)]| - )', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1 $2",
            model_replacement = "$1 $2",
            regex = "; *(?:(?:HTC|htc)(?:_blocked)*[ _/])+([^ _/]+)(?:[ _/]([^ _/;\\)]+))?(?: *Build|[;\\)]| - )",
            regex_compiled = lrex.new('; *(?:(?:HTC|htc)(?:_blocked)*[ _/])+([^ _/]+)(?:[ _/]([^ _/;\\)]+))?(?: *Build|[;\\)]| - )', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1 $2 $3",
            model_replacement = "$1 $2 $3",
            regex = "; *(?:(?:HTC|htc)(?:_blocked)*[ _/])+([^ _/]+)(?:[ _/]([^ _/]+)(?:[ _/]([^ _/;\\)]+))?)?(?: *Build|[;\\)]| - )",
            regex_compiled = lrex.new('; *(?:(?:HTC|htc)(?:_blocked)*[ _/])+([^ _/]+)(?:[ _/]([^ _/]+)(?:[ _/]([^ _/;\\)]+))?)?(?: *Build|[;\\)]| - )', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1 $2 $3 $4",
            model_replacement = "$1 $2 $3 $4",
            regex = "; *(?:(?:HTC|htc)(?:_blocked)*[ _/])+([^ _/]+)(?:[ _/]([^ _/]+)(?:[ _/]([^ _/]+)(?:[ _/]([^ /;]+))?)?)?(?: *Build|[;\\)]| - )",
            regex_compiled = lrex.new('; *(?:(?:HTC|htc)(?:_blocked)*[ _/])+([^ _/]+)(?:[ _/]([^ _/]+)(?:[ _/]([^ _/]+)(?:[ _/]([^ /;]+))?)?)?(?: *Build|[;\\)]| - )', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1",
            model_replacement = "$1",
            regex = "HTC Streaming Player [^\\/]*/[^\\/]*/ htc_([^/]+) /",
            regex_compiled = lrex.new('HTC Streaming Player [^\\/]*/[^\\/]*/ htc_([^/]+) /', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1",
            model_replacement = "$1",
            regex = "(?:[;,] *|^)(?:htccn_chs-)?HTC[ _-]?([^;]+?)(?: *Build|clay|Android|-?Mozilla| Opera| Profile| UNTRUSTED|[;/\\(\\)]|$)",
            regex_compiled = lrex.new('(?:[;,] *|^)(?:htccn_chs-)?HTC[ _-]?([^;]+?)(?: *Build|clay|Android|-?Mozilla| Opera| Profile| UNTRUSTED|[;/\\(\\)]|$)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1",
            model_replacement = "$1",
            regex = "; *(A6277|ADR6200|ADR6300|ADR6350|ADR6400[A-Z]*|ADR6425[A-Z]*|APX515CKT|ARIA|Desire[^_ ]*|Dream|EndeavorU|Eris|Evo|Flyer|HD2|Hero|HERO200|Hero CDMA|HTL21|Incredible|Inspire[A-Z0-9]*|Legend|Liberty|Nexus ?(?:One|HD2)|One|One S C2|One[ _]?(?:S|V|X\\+?)\\w*|PC36100|PG06100|PG86100|S31HT|Sensation|Wildfire)(?: Build|[/;\\(\\)])",
            regex_compiled = lrex.new('; *(A6277|ADR6200|ADR6300|ADR6350|ADR6400[A-Z]*|ADR6425[A-Z]*|APX515CKT|ARIA|Desire[^_ ]*|Dream|EndeavorU|Eris|Evo|Flyer|HD2|Hero|HERO200|Hero CDMA|HTL21|Incredible|Inspire[A-Z0-9]*|Legend|Liberty|Nexus ?(?:One|HD2)|One|One S C2|One[ _]?(?:S|V|X\\+?)\\w*|PC36100|PG06100|PG86100|S31HT|Sensation|Wildfire)(?: Build|[/;\\(\\)])', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1 $2",
            model_replacement = "$1 $2",
            regex = "; *(ADR6200|ADR6400L|ADR6425LVW|Amaze|DesireS?|EndeavorU|Eris|EVO|Evo\\d[A-Z]+|HD2|IncredibleS?|Inspire[A-Z0-9]*|Inspire[A-Z0-9]*|Sensation[A-Z0-9]*|Wildfire)[ _-](.+?)(?:[/;\\)]|Build|MIUI|1\\.0)",
            regex_compiled = lrex.new('; *(ADR6200|ADR6400L|ADR6425LVW|Amaze|DesireS?|EndeavorU|Eris|EVO|Evo\\d[A-Z]+|HD2|IncredibleS?|Inspire[A-Z0-9]*|Inspire[A-Z0-9]*|Sensation[A-Z0-9]*|Wildfire)[ _-](.+?)(?:[/;\\)]|Build|MIUI|1\\.0)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Hyundai",
            device_replacement = "Hyundai $1",
            model_replacement = "$1",
            regex = "; *HYUNDAI (T\\d[^/]*) Build",
            regex_compiled = lrex.new('; *HYUNDAI (T\\d[^/]*) Build', 'cf')
        }, {
            brand_replacement = "Hyundai",
            device_replacement = "Hyundai $1",
            model_replacement = "$1",
            regex = "; *HYUNDAI ([^;/]+) Build",
            regex_compiled = lrex.new('; *HYUNDAI ([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Hyundai",
            device_replacement = "Hyundai $1",
            model_replacement = "$1",
            regex = "; *(X700|Hold X|MB-6900) Build",
            regex_compiled = lrex.new('; *(X700|Hold X|MB-6900) Build', 'cf')
        }, {
            brand_replacement = "iBall",
            device_replacement = "$1 $2",
            model_replacement = "$1 $2",
            regex = "; *(?:iBall[ _\\-])?(Andi)[ _]?(\\d[^;/]*) Build",
            regex_compiled = lrex.new('; *(?:iBall[ _\\-])?(Andi)[ _]?(\\d[^;/]*) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "iBall",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(IBall)(?:[ _]([^;/]+))? Build",
            regex_compiled = lrex.new('; *(IBall)(?:[ _]([^;/]+))? Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "IconBIT",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(NT-\\d+[^ ;/]*|Net[Tt]AB [^;/]+|Mercury [A-Z]+|iconBIT)(?: S/N:[^;/]+)? Build",
            regex_compiled = lrex.new('; *(NT-\\d+[^ ;/]*|Net[Tt]AB [^;/]+|Mercury [A-Z]+|iconBIT)(?: S/N:[^;/]+)? Build', 'cf')
        }, {
            brand_replacement = "IMO",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(IMO)[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *(IMO)[ _]([^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "imobile",
            device_replacement = "i-mobile $1",
            model_replacement = "$1",
            regex = "; *i-?mobile[ _]([^/]+) Build/",
            regex_compiled = lrex.new('; *i-?mobile[ _]([^/]+) Build/', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "imobile",
            device_replacement = "i-mobile $1",
            model_replacement = "$1",
            regex = "; *(i-(?:style|note)[^/]*) Build/",
            regex_compiled = lrex.new('; *(i-(?:style|note)[^/]*) Build/', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Impression",
            device_replacement = "$1 $2",
            model_replacement = "$1 $2",
            regex = "; *(ImPAD) ?(\\d+(?:.)*) Build",
            regex_compiled = lrex.new('; *(ImPAD) ?(\\d+(?:.)*) Build', 'cf')
        }, {
            brand_replacement = "Infinix",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(Infinix)[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *(Infinix)[ _]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Informer",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(Informer)[ \\-]([^;/]+) Build",
            regex_compiled = lrex.new('; *(Informer)[ \\-]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Intenso",
            device_replacement = "Intenso $1",
            model_replacement = "$1 $2",
            regex = "; *(TAB) ?([78][12]4) Build",
            regex_compiled = lrex.new('; *(TAB) ?([78][12]4) Build', 'cf')
        }, {
            brand_replacement = "Intex",
            device_replacement = "$1$2$3",
            model_replacement = "$1 $3",
            regex = "; *(?:Intex[ _])?(AQUA|Aqua)([ _\\.\\-])([^;/]+) *(?:Build|;)",
            regex_compiled = lrex.new('; *(?:Intex[ _])?(AQUA|Aqua)([ _\\.\\-])([^;/]+) *(?:Build|;)', 'cf')
        }, {
            brand_replacement = "Intex",
            device_replacement = "$1 $2",
            model_replacement = "$1 $2",
            regex = "; *(?:INTEX|Intex)(?:[_ ]([^\\ _;/]+))(?:[_ ]([^\\ _;/]+))? *(?:Build|;)",
            regex_compiled = lrex.new('; *(?:INTEX|Intex)(?:[_ ]([^\\ _;/]+))(?:[_ ]([^\\ _;/]+))? *(?:Build|;)', 'cf')
        }, {
            brand_replacement = "Intex",
            device_replacement = "$1 $2 $3",
            model_replacement = "iBuddy $2 $3",
            regex = "; *([iI]Buddy)[ _]?(Connect)(?:_|\\?_| )?([^;/]*) *(?:Build|;)",
            regex_compiled = lrex.new('; *([iI]Buddy)[ _]?(Connect)(?:_|\\?_| )?([^;/]*) *(?:Build|;)', 'cf')
        }, {
            brand_replacement = "Intex",
            device_replacement = "$1 $2",
            model_replacement = "iBuddy $2",
            regex = "; *(I-Buddy)[ _]([^;/]+) *(?:Build|;)",
            regex_compiled = lrex.new('; *(I-Buddy)[ _]([^;/]+) *(?:Build|;)', 'cf')
        }, {
            brand_replacement = "iOCEAN",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(iOCEAN) ([^/]+) Build",
            regex_compiled = lrex.new('; *(iOCEAN) ([^/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "ionik",
            device_replacement = "ionik $1",
            model_replacement = "$1",
            regex = "; *(TP\\d+(?:\\.\\d+)?\\-\\d[^;/]+) Build",
            regex_compiled = lrex.new('; *(TP\\d+(?:\\.\\d+)?\\-\\d[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Iru",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(M702pro) Build",
            regex_compiled = lrex.new('; *(M702pro) Build', 'cf')
        }, {
            brand_replacement = "Ivio",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(DE88Plus|MD70) Build",
            regex_compiled = lrex.new('; *(DE88Plus|MD70) Build', 'cf')
        }, {
            brand_replacement = "Ivio",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *IVIO[_\\-]([^;/]+) Build",
            regex_compiled = lrex.new('; *IVIO[_\\-]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Jaytech",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(TPC-\\d+|JAY-TECH) Build",
            regex_compiled = lrex.new('; *(TPC-\\d+|JAY-TECH) Build', 'cf')
        }, {
            brand_replacement = "Jiayu",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(JY-[^;/]+|G[234]S?) Build",
            regex_compiled = lrex.new('; *(JY-[^;/]+|G[234]S?) Build', 'cf')
        }, {
            brand_replacement = "JXD",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(JXD)[ _\\-]([^;/]+) Build",
            regex_compiled = lrex.new('; *(JXD)[ _\\-]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Karbonn",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *Karbonn[ _]?([^;/]+) *(?:Build|;)",
            regex_compiled = lrex.new('; *Karbonn[ _]?([^;/]+) *(?:Build|;)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Karbonn",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *([^;]+) Build/Karbonn",
            regex_compiled = lrex.new('; *([^;]+) Build/Karbonn', 'cf')
        }, {
            brand_replacement = "Karbonn",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(A11|A39|A37|A34|ST8|ST10|ST7|Smart Tab3|Smart Tab2|Titanium S\\d) +Build",
            regex_compiled = lrex.new('; *(A11|A39|A37|A34|ST8|ST10|ST7|Smart Tab3|Smart Tab2|Titanium S\\d) +Build', 'cf')
        }, {
            brand_replacement = "Sharp",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(IS01|IS03|IS05|IS\\d{2}SH) Build",
            regex_compiled = lrex.new('; *(IS01|IS03|IS05|IS\\d{2}SH) Build', 'cf')
        }, {
            brand_replacement = "Regza",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(IS04) Build",
            regex_compiled = lrex.new('; *(IS04) Build', 'cf')
        }, {
            brand_replacement = "Pantech",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(IS06|IS\\d{2}PT) Build",
            regex_compiled = lrex.new('; *(IS06|IS\\d{2}PT) Build', 'cf')
        }, {
            brand_replacement = "SonyEricsson",
            device_replacement = "$1",
            model_replacement = "Xperia Acro",
            regex = "; *(IS11S) Build",
            regex_compiled = lrex.new('; *(IS11S) Build', 'cf')
        }, {
            brand_replacement = "Casio",
            device_replacement = "$1",
            model_replacement = "GzOne $1",
            regex = "; *(IS11CA) Build",
            regex_compiled = lrex.new('; *(IS11CA) Build', 'cf')
        }, {
            brand_replacement = "LG",
            device_replacement = "$1",
            model_replacement = "Optimus X",
            regex = "; *(IS11LG) Build",
            regex_compiled = lrex.new('; *(IS11LG) Build', 'cf')
        }, {
            brand_replacement = "Medias",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(IS11N) Build",
            regex_compiled = lrex.new('; *(IS11N) Build', 'cf')
        }, {
            brand_replacement = "Pantech",
            device_replacement = "$1",
            model_replacement = "MIRACH",
            regex = "; *(IS11PT) Build",
            regex_compiled = lrex.new('; *(IS11PT) Build', 'cf')
        }, {
            brand_replacement = "Fujitsu",
            device_replacement = "$1",
            model_replacement = "Arrows ES",
            regex = "; *(IS12F) Build",
            regex_compiled = lrex.new('; *(IS12F) Build', 'cf')
        }, {
            brand_replacement = "Motorola",
            device_replacement = "$1",
            model_replacement = "XT909",
            regex = "; *(IS12M) Build",
            regex_compiled = lrex.new('; *(IS12M) Build', 'cf')
        }, {
            brand_replacement = "SonyEricsson",
            device_replacement = "$1",
            model_replacement = "Xperia Acro HD",
            regex = "; *(IS12S) Build",
            regex_compiled = lrex.new('; *(IS12S) Build', 'cf')
        }, {
            brand_replacement = "Fujitsu",
            device_replacement = "$1",
            model_replacement = "Arrowz Z",
            regex = "; *(ISW11F) Build",
            regex_compiled = lrex.new('; *(ISW11F) Build', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "$1",
            model_replacement = "EVO",
            regex = "; *(ISW11HT) Build",
            regex_compiled = lrex.new('; *(ISW11HT) Build', 'cf')
        }, {
            brand_replacement = "Kyocera",
            device_replacement = "$1",
            model_replacement = "DIGNO",
            regex = "; *(ISW11K) Build",
            regex_compiled = lrex.new('; *(ISW11K) Build', 'cf')
        }, {
            brand_replacement = "Motorola",
            device_replacement = "$1",
            model_replacement = "Photon",
            regex = "; *(ISW11M) Build",
            regex_compiled = lrex.new('; *(ISW11M) Build', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "$1",
            model_replacement = "GALAXY S II WiMAX",
            regex = "; *(ISW11SC) Build",
            regex_compiled = lrex.new('; *(ISW11SC) Build', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "$1",
            model_replacement = "EVO 3D",
            regex = "; *(ISW12HT) Build",
            regex_compiled = lrex.new('; *(ISW12HT) Build', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "$1",
            model_replacement = "J",
            regex = "; *(ISW13HT) Build",
            regex_compiled = lrex.new('; *(ISW13HT) Build', 'cf')
        }, {
            brand_replacement = "KDDI",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(ISW?[0-9]{2}[A-Z]{0,2}) Build",
            regex_compiled = lrex.new('; *(ISW?[0-9]{2}[A-Z]{0,2}) Build', 'cf')
        }, {
            brand_replacement = "KDDI",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(INFOBAR [^;/]+) Build",
            regex_compiled = lrex.new('; *(INFOBAR [^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Kingcom",
            device_replacement = "$1 $2",
            model_replacement = "$1 $2",
            regex = "; *(JOYPAD|Joypad)[ _]([^;/]+) Build/",
            regex_compiled = lrex.new('; *(JOYPAD|Joypad)[ _]([^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Kobo",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(Vox|VOX|Arc|K080) Build/",
            regex_compiled = lrex.new('; *(Vox|VOX|Arc|K080) Build/', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Kobo",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "\\b(Kobo Touch)\\b",
            regex_compiled = lrex.new('\\b(Kobo Touch)\\b', 'cf')
        }, {
            brand_replacement = "Ktouch",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(K-Touch)[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *(K-Touch)[ _]([^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "KTtech",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *((?:EV|KM)-S\\d+[A-Z]?) Build",
            regex_compiled = lrex.new('; *((?:EV|KM)-S\\d+[A-Z]?) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Kyocera",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(Zio|Hydro|Torque|Event|EVENT|Echo|Milano|Rise|URBANO PROGRESSO|WX04K|WX06K|WX10K|KYL21|101K|C5[12]\\d{2}) Build/",
            regex_compiled = lrex.new('; *(Zio|Hydro|Torque|Event|EVENT|Echo|Milano|Rise|URBANO PROGRESSO|WX04K|WX06K|WX10K|KYL21|101K|C5[12]\\d{2}) Build/', 'cf')
        }, {
            brand_replacement = "Lava",
            device_replacement = "Iris $1",
            model_replacement = "Iris $1",
            regex = "; *(?:LAVA[ _])?IRIS[ _\\-]?([^/;\\)]+) *(?:;|\\)|Build)",
            regex_compiled = lrex.new('; *(?:LAVA[ _])?IRIS[ _\\-]?([^/;\\)]+) *(?:;|\\)|Build)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Lava",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *LAVA[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *LAVA[ _]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Lemon",
            device_replacement = "Lemon $1$2",
            model_replacement = "$1$2",
            regex = "; *(?:(Aspire A1)|(?:LEMON|Lemon)[ _]([^;/]+))_? Build",
            regex_compiled = lrex.new('; *(?:(Aspire A1)|(?:LEMON|Lemon)[ _]([^;/]+))_? Build', 'cf')
        }, {
            brand_replacement = "Lenco",
            device_replacement = "Lenco $1",
            model_replacement = "$1",
            regex = "; *(TAB-1012) Build/",
            regex_compiled = lrex.new('; *(TAB-1012) Build/', 'cf')
        }, {
            brand_replacement = "Lenco",
            device_replacement = "Lenco $1",
            model_replacement = "$1",
            regex = "; Lenco ([^;/]+) Build/",
            regex_compiled = lrex.new('; Lenco ([^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Lenovo",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(A1_07|A2107A-H|S2005A-H|S1-37AH0) Build",
            regex_compiled = lrex.new('; *(A1_07|A2107A-H|S2005A-H|S1-37AH0) Build', 'cf')
        }, {
            brand_replacement = "Lenovo",
            device_replacement = "Lenovo $1 $2",
            model_replacement = "$1 $2",
            regex = "; *(Idea[Tp]ab)[ _]([^;/]+);? Build",
            regex_compiled = lrex.new('; *(Idea[Tp]ab)[ _]([^;/]+);? Build', 'cf')
        }, {
            brand_replacement = "Lenovo",
            device_replacement = "Lenovo $1 $2",
            model_replacement = "$1 $2",
            regex = "; *(Idea(?:Tab|pad)) ?([^;/]+) Build",
            regex_compiled = lrex.new('; *(Idea(?:Tab|pad)) ?([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Lenovo",
            device_replacement = "Lenovo $1 $2",
            model_replacement = "$1 $2",
            regex = "; *(ThinkPad) ?(Tablet) Build/",
            regex_compiled = lrex.new('; *(ThinkPad) ?(Tablet) Build/', 'cf')
        }, {
            brand_replacement = "Lenovo",
            device_replacement = "Lenovo $1",
            model_replacement = "$1",
            regex = "; *(?:LNV-)?(?:=?[Ll]enovo[ _\\-]?|LENOVO[ _])+(.+?)(?:Build|[;/\\)])",
            regex_compiled = lrex.new('; *(?:LNV-)?(?:=?[Ll]enovo[ _\\-]?|LENOVO[ _])+(.+?)(?:Build|[;/\\)])', 'cf')
        }, {
            brand_replacement = "Lenovo",
            device_replacement = "Lenovo $1 $2 $3",
            model_replacement = "$1 $2 $3",
            regex = "[;,] (?:Vodafone )?(SmartTab) ?(II) ?(\\d+) Build/",
            regex_compiled = lrex.new('[;,] (?:Vodafone )?(SmartTab) ?(II) ?(\\d+) Build/', 'cf')
        }, {
            brand_replacement = "Lenovo",
            device_replacement = "Lenovo Ideapad K1",
            model_replacement = "Ideapad K1",
            regex = "; *(?:Ideapad )?K1 Build/",
            regex_compiled = lrex.new('; *(?:Ideapad )?K1 Build/', 'cf')
        }, {
            brand_replacement = "Lenovo",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(3GC101|3GW10[01]|A390) Build/",
            regex_compiled = lrex.new('; *(3GC101|3GW10[01]|A390) Build/', 'cf')
        }, {
            brand_replacement = "Lenovo",
            device_replacement = "Lenovo $1",
            model_replacement = "$1",
            regex = "\\b(?:Lenovo|LENOVO)+[ _\\-]?([^,;:/ ]+)",
            regex_compiled = lrex.new('\\b(?:Lenovo|LENOVO)+[ _\\-]?([^,;:/ ]+)', 'cf')
        }, {
            brand_replacement = "Lexibook",
            device_replacement = "$1$2",
            model_replacement = "$1$2",
            regex = "; *(MFC\\d+)[A-Z]{2}([^;,/]*),? Build",
            regex_compiled = lrex.new('; *(MFC\\d+)[A-Z]{2}([^;,/]*),? Build', 'cf')
        }, {
            brand_replacement = "LG",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(E[34][0-9]{2}|LS[6-8][0-9]{2}|VS[6-9][0-9]+[^;/]+|Nexus 4|Nexus 5X?|GT540f?|Optimus (?:2X|G|4X HD)|OptimusX4HD) *(?:Build|;)",
            regex_compiled = lrex.new('; *(E[34][0-9]{2}|LS[6-8][0-9]{2}|VS[6-9][0-9]+[^;/]+|Nexus 4|Nexus 5X?|GT540f?|Optimus (?:2X|G|4X HD)|OptimusX4HD) *(?:Build|;)', 'cf')
        }, {
            brand_replacement = "LG",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "[;:] *(L-\\d+[A-Z]|LGL\\d+[A-Z]?)(?:/V\\d+)? *(?:Build|[;\\)])",
            regex_compiled = lrex.new('[;:] *(L-\\d+[A-Z]|LGL\\d+[A-Z]?)(?:/V\\d+)? *(?:Build|[;\\)])', 'cf')
        }, {
            brand_replacement = "LG",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(LG-)([A-Z]{1,2}\\d{2,}[^,;/\\)\\(]*?)(?:Build| V\\d+|[,;/\\)\\(]|$)",
            regex_compiled = lrex.new('; *(LG-)([A-Z]{1,2}\\d{2,}[^,;/\\)\\(]*?)(?:Build| V\\d+|[,;/\\)\\(]|$)', 'cf')
        }, {
            brand_replacement = "LG",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(LG[ \\-]|LG)([^;/]+)[;/]? Build",
            regex_compiled = lrex.new('; *(LG[ \\-]|LG)([^;/]+)[;/]? Build', 'cf')
        }, {
            brand_replacement = "LG",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "^(LG)-([^;/]+)/ Mozilla/.*; Android",
            regex_compiled = lrex.new('^(LG)-([^;/]+)/ Mozilla/.*; Android', 'cf')
        }, {
            brand_replacement = "LG",
            device_replacement = "LG $1 $2",
            model_replacement = "$1 $2",
            regex = "(Web0S); Linux/(SmartTV)",
            regex_compiled = lrex.new('(Web0S); Linux/(SmartTV)', 'cf')
        }, {
            brand_replacement = "Malata",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *((?:SMB|smb)[^;/]+) Build/",
            regex_compiled = lrex.new('; *((?:SMB|smb)[^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Malata",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(?:Malata|MALATA) ([^;/]+) Build/",
            regex_compiled = lrex.new('; *(?:Malata|MALATA) ([^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Manta",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(MS[45][0-9]{3}|MID0[568][NS]?|MID[1-9]|MID[78]0[1-9]|MID970[1-9]|MID100[1-9]) Build/",
            regex_compiled = lrex.new('; *(MS[45][0-9]{3}|MID0[568][NS]?|MID[1-9]|MID[78]0[1-9]|MID970[1-9]|MID100[1-9]) Build/', 'cf')
        }, {
            brand_replacement = "Match",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(M1052|M806|M9000|M9100|M9701|MID100|MID120|MID125|MID130|MID135|MID140|MID701|MID710|MID713|MID727|MID728|MID731|MID732|MID733|MID735|MID736|MID737|MID760|MID800|MID810|MID820|MID830|MID833|MID835|MID860|MID900|MID930|MID933|MID960|MID980) Build/",
            regex_compiled = lrex.new('; *(M1052|M806|M9000|M9100|M9701|MID100|MID120|MID125|MID130|MID135|MID140|MID701|MID710|MID713|MID727|MID728|MID731|MID732|MID733|MID735|MID736|MID737|MID760|MID800|MID810|MID820|MID830|MID833|MID835|MID860|MID900|MID930|MID933|MID960|MID980) Build/', 'cf')
        }, {
            brand_replacement = "Maxx",
            device_replacement = "Maxx $1",
            model_replacement = "$1",
            regex = "; *(GenxDroid7|MSD7.*|AX\\d.*|Tab 701|Tab 722) Build/",
            regex_compiled = lrex.new('; *(GenxDroid7|MSD7.*|AX\\d.*|Tab 701|Tab 722) Build/', 'cf')
        }, {
            brand_replacement = "Mediacom",
            device_replacement = "Mediacom $1",
            model_replacement = "$1",
            regex = "; *(M-PP[^;/]+|PhonePad ?\\d{2,}[^;/]+) Build",
            regex_compiled = lrex.new('; *(M-PP[^;/]+|PhonePad ?\\d{2,}[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Mediacom",
            device_replacement = "Mediacom $1",
            model_replacement = "$1",
            regex = "; *(M-MP[^;/]+|SmartPad ?\\d{2,}[^;/]+) Build",
            regex_compiled = lrex.new('; *(M-MP[^;/]+|SmartPad ?\\d{2,}[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Medion",
            device_replacement = "Medion Lifetab $1",
            model_replacement = "Lifetab $1",
            regex = "; *(?:MD_)?LIFETAB[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *(?:MD_)?LIFETAB[ _]([^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Medion",
            device_replacement = "Medion $1",
            model_replacement = "$1",
            regex = "; *MEDION ([^;/]+) Build",
            regex_compiled = lrex.new('; *MEDION ([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Meizu",
            device_replacement = "Meizu $1",
            model_replacement = "$1",
            regex = "; *(M030|M031|M035|M040|M065|m9) Build",
            regex_compiled = lrex.new('; *(M030|M031|M035|M040|M065|m9) Build', 'cf')
        }, {
            brand_replacement = "Meizu",
            device_replacement = "Meizu $1",
            model_replacement = "$1",
            regex = "; *(?:meizu_|MEIZU )(.+?) *(?:Build|[;\\)])",
            regex_compiled = lrex.new('; *(?:meizu_|MEIZU )(.+?) *(?:Build|[;\\)])', 'cf')
        }, {
            brand_replacement = "Micromax",
            device_replacement = "Micromax $1$2",
            model_replacement = "$1$2",
            regex = "; *(?:Micromax[ _](A111|A240)|(A111|A240)) Build",
            regex_compiled = lrex.new('; *(?:Micromax[ _](A111|A240)|(A111|A240)) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Micromax",
            device_replacement = "Micromax $1",
            model_replacement = "$1",
            regex = "; *Micromax[ _](A\\d{2,3}[^;/]*) Build",
            regex_compiled = lrex.new('; *Micromax[ _](A\\d{2,3}[^;/]*) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Micromax",
            device_replacement = "Micromax $1",
            model_replacement = "$1",
            regex = "; *(A\\d{2}|A[12]\\d{2}|A90S|A110Q) Build",
            regex_compiled = lrex.new('; *(A\\d{2}|A[12]\\d{2}|A90S|A110Q) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Micromax",
            device_replacement = "Micromax $1",
            model_replacement = "$1",
            regex = "; *Micromax[ _](P\\d{3}[^;/]*) Build",
            regex_compiled = lrex.new('; *Micromax[ _](P\\d{3}[^;/]*) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Micromax",
            device_replacement = "Micromax $1",
            model_replacement = "$1",
            regex = "; *(P\\d{3}|P\\d{3}\\(Funbook\\)) Build",
            regex_compiled = lrex.new('; *(P\\d{3}|P\\d{3}\\(Funbook\\)) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Mito",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(MITO)[ _\\-]?([^;/]+) Build",
            regex_compiled = lrex.new('; *(MITO)[ _\\-]?([^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Mobistel",
            device_replacement = "$1 $2",
            model_replacement = "$1 $2",
            regex = "; *(Cynus)[ _](F5|T\\d|.+?) *(?:Build|[;/\\)])",
            regex_compiled = lrex.new('; *(Cynus)[ _](F5|T\\d|.+?) *(?:Build|[;/\\)])', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Modecom",
            device_replacement = "$1$2 $3",
            model_replacement = "$2 $3",
            regex = "; *(MODECOM )?(FreeTab) ?([^;/]+) Build",
            regex_compiled = lrex.new('; *(MODECOM )?(FreeTab) ?([^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Modecom",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(MODECOM )([^;/]+) Build",
            regex_compiled = lrex.new('; *(MODECOM )([^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Motorola",
            device_replacement = "Motorola $1",
            model_replacement = "$1",
            regex = "; *(MZ\\d{3}\\+?|MZ\\d{3} 4G|Xoom|XOOM[^;/]*) Build",
            regex_compiled = lrex.new('; *(MZ\\d{3}\\+?|MZ\\d{3} 4G|Xoom|XOOM[^;/]*) Build', 'cf')
        }, {
            brand_replacement = "Motorola",
            device_replacement = "Motorola $1$2",
            model_replacement = "$2",
            regex = "; *(Milestone )(XT[^;/]*) Build",
            regex_compiled = lrex.new('; *(Milestone )(XT[^;/]*) Build', 'cf')
        }, {
            brand_replacement = "Motorola",
            device_replacement = "Motorola $1",
            model_replacement = "DROID X",
            regex = "; *(Motoroi ?x|Droid X|DROIDX) Build",
            regex_compiled = lrex.new('; *(Motoroi ?x|Droid X|DROIDX) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Motorola",
            device_replacement = "Motorola $1",
            model_replacement = "$1",
            regex = "; *(Droid[^;/]*|DROID[^;/]*|Milestone[^;/]*|Photon|Triumph|Devour|Titanium) Build",
            regex_compiled = lrex.new('; *(Droid[^;/]*|DROID[^;/]*|Milestone[^;/]*|Photon|Triumph|Devour|Titanium) Build', 'cf')
        }, {
            brand_replacement = "Motorola",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(A555|A85[34][^;/]*|A95[356]|ME[58]\\d{2}\\+?|ME600|ME632|ME722|MB\\d{3}\\+?|MT680|MT710|MT870|MT887|MT917|WX435|WX453|WX44[25]|XT\\d{3,4}[A-Z\\+]*|CL[iI]Q|CL[iI]Q XT) Build",
            regex_compiled = lrex.new('; *(A555|A85[34][^;/]*|A95[356]|ME[58]\\d{2}\\+?|ME600|ME632|ME722|MB\\d{3}\\+?|MT680|MT710|MT870|MT887|MT917|WX435|WX453|WX44[25]|XT\\d{3,4}[A-Z\\+]*|CL[iI]Q|CL[iI]Q XT) Build', 'cf')
        }, {
            brand_replacement = "Motorola",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(Motorola MOT-|Motorola[ _\\-]|MOT\\-?)([^;/]+) Build",
            regex_compiled = lrex.new('; *(Motorola MOT-|Motorola[ _\\-]|MOT\\-?)([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Motorola",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(Moto[_ ]?|MOT\\-)([^;/]+) Build",
            regex_compiled = lrex.new('; *(Moto[_ ]?|MOT\\-)([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Mpman",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *((?:MP[DQ]C|MPG\\d{1,4}|MP\\d{3,4}|MID(?:(?:10[234]|114|43|7[247]|8[24]|7)C|8[01]1))[^;/]*) Build",
            regex_compiled = lrex.new('; *((?:MP[DQ]C|MPG\\d{1,4}|MP\\d{3,4}|MID(?:(?:10[234]|114|43|7[247]|8[24]|7)C|8[01]1))[^;/]*) Build', 'cf')
        }, {
            brand_replacement = "Msi",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(?:MSI[ _])?(Primo\\d+|Enjoy[ _\\-][^;/]+) Build",
            regex_compiled = lrex.new('; *(?:MSI[ _])?(Primo\\d+|Enjoy[ _\\-][^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Multilaser",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *Multilaser[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *Multilaser[ _]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "MyPhone",
            device_replacement = "$1$2 $3",
            model_replacement = "$1$2 $3",
            regex = "; *(My)[_]?(Pad)[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *(My)[_]?(Pad)[ _]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "MyPhone",
            device_replacement = "$1$2 $3",
            model_replacement = "$3",
            regex = "; *(My)\\|?(Phone)[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *(My)\\|?(Phone)[ _]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "MyPhone",
            device_replacement = "$1 $2",
            model_replacement = "$1 $2",
            regex = "; *(A\\d+)[ _](Duo)? Build",
            regex_compiled = lrex.new('; *(A\\d+)[ _](Duo)? Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Mytab",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(myTab[^;/]*) Build",
            regex_compiled = lrex.new('; *(myTab[^;/]*) Build', 'cf')
        }, {
            brand_replacement = "Nabi",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(NABI2?-)([^;/]+) Build/",
            regex_compiled = lrex.new('; *(NABI2?-)([^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Nec",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(N-\\d+[CDE]) Build/",
            regex_compiled = lrex.new('; *(N-\\d+[CDE]) Build/', 'cf')
        }, {
            brand_replacement = "Nec",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; ?(NEC-)(.*) Build/",
            regex_compiled = lrex.new('; ?(NEC-)(.*) Build/', 'cf')
        }, {
            brand_replacement = "Nec",
            device_replacement = "$1",
            model_replacement = "Lifetouch Note",
            regex = "; *(LT-NA7) Build/",
            regex_compiled = lrex.new('; *(LT-NA7) Build/', 'cf')
        }, {
            brand_replacement = "Nextbook",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(NXM\\d+[A-z0-9_]*|Next\\d[A-z0-9_ \\-]*|NEXT\\d[A-z0-9_ \\-]*|Nextbook [A-z0-9_ ]*|DATAM803HC|M805)(?: Build|[\\);])",
            regex_compiled = lrex.new('; *(NXM\\d+[A-z0-9_]*|Next\\d[A-z0-9_ \\-]*|NEXT\\d[A-z0-9_ \\-]*|Nextbook [A-z0-9_ ]*|DATAM803HC|M805)(?: Build|[\\);])', 'cf')
        }, {
            brand_replacement = "Nokia",
            device_replacement = "$1$2$3",
            model_replacement = "$3",
            regex = "; *(Nokia)([ _\\-]*)([^;/]*) Build",
            regex_compiled = lrex.new('; *(Nokia)([ _\\-]*)([^;/]*) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Nook",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(Nook ?|Barnes & Noble Nook |BN )([^;/]+) Build",
            regex_compiled = lrex.new('; *(Nook ?|Barnes & Noble Nook |BN )([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Nook",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(NOOK )?(BNRV200|BNRV200A|BNTV250|BNTV250A|BNTV400|BNTV600|LogicPD Zoom2) Build",
            regex_compiled = lrex.new('; *(NOOK )?(BNRV200|BNRV200A|BNTV250|BNTV250A|BNTV400|BNTV600|LogicPD Zoom2) Build', 'cf')
        }, {
            brand_replacement = "Nook",
            device_replacement = "$1",
            model_replacement = "Tablet",
            regex = "; Build/(Nook)",
            regex_compiled = lrex.new('; Build/(Nook)', 'cf')
        }, {
            brand_replacement = "Olivetti",
            device_replacement = "Olivetti $1",
            model_replacement = "$1",
            regex = "; *(OP110|OliPad[^;/]+) Build",
            regex_compiled = lrex.new('; *(OP110|OliPad[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Omega",
            device_replacement = "Omega $1",
            model_replacement = "$1",
            regex = "; *OMEGA[ _\\-](MID[^;/]+) Build",
            regex_compiled = lrex.new('; *OMEGA[ _\\-](MID[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Omega",
            device_replacement = "Omega $1",
            model_replacement = "$1",
            regex = "^(MID7500|MID\\d+) Mozilla/5\\.0 \\(iPad;",
            regex_compiled = lrex.new('^(MID7500|MID\\d+) Mozilla/5\\.0 \\(iPad;', 'cf')
        }, {
            brand_replacement = "Openpeak",
            device_replacement = "Openpeak $1",
            model_replacement = "$1",
            regex = "; *((?:CIUS|cius)[^;/]*) Build",
            regex_compiled = lrex.new('; *((?:CIUS|cius)[^;/]*) Build', 'cf')
        }, {
            brand_replacement = "Oppo",
            device_replacement = "Oppo $1",
            model_replacement = "$1",
            regex = "; *(Find ?(?:5|7a)|R8[012]\\d{1,2}|T703\\d{0,1}|U70\\d{1,2}T?|X90\\d{1,2}) Build",
            regex_compiled = lrex.new('; *(Find ?(?:5|7a)|R8[012]\\d{1,2}|T703\\d{0,1}|U70\\d{1,2}T?|X90\\d{1,2}) Build', 'cf')
        }, {
            brand_replacement = "Oppo",
            device_replacement = "Oppo $1",
            model_replacement = "$1",
            regex = "; *OPPO ?([^;/]+) Build/",
            regex_compiled = lrex.new('; *OPPO ?([^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Odys",
            device_replacement = "Odys $1",
            model_replacement = "$1",
            regex = "; *(?:Odys\\-|ODYS\\-|ODYS )([^;/]+) Build",
            regex_compiled = lrex.new('; *(?:Odys\\-|ODYS\\-|ODYS )([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Odys",
            device_replacement = "Odys $1 $2",
            model_replacement = "$1 $2",
            regex = "; *(SELECT) ?(7) Build",
            regex_compiled = lrex.new('; *(SELECT) ?(7) Build', 'cf')
        }, {
            brand_replacement = "Odys",
            device_replacement = "Odys $1 $2 $3",
            model_replacement = "$1 $2 $3",
            regex = "; *(PEDI)_(PLUS)_(W) Build",
            regex_compiled = lrex.new('; *(PEDI)_(PLUS)_(W) Build', 'cf')
        }, {
            brand_replacement = "Odys",
            device_replacement = "Odys $1",
            model_replacement = "$1",
            regex = "; *(AEON|BRAVIO|FUSION|FUSION2IN1|Genio|EOS10|IEOS[^;/]*|IRON|Loox|LOOX|LOOX Plus|Motion|NOON|NOON_PRO|NEXT|OPOS|PEDI[^;/]*|PRIME[^;/]*|STUDYTAB|TABLO|Tablet-PC-4|UNO_X8|XELIO[^;/]*|Xelio ?\\d+ ?[Pp]ro|XENO10|XPRESS PRO) Build",
            regex_compiled = lrex.new('; *(AEON|BRAVIO|FUSION|FUSION2IN1|Genio|EOS10|IEOS[^;/]*|IRON|Loox|LOOX|LOOX Plus|Motion|NOON|NOON_PRO|NEXT|OPOS|PEDI[^;/]*|PRIME[^;/]*|STUDYTAB|TABLO|Tablet-PC-4|UNO_X8|XELIO[^;/]*|Xelio ?\\d+ ?[Pp]ro|XENO10|XPRESS PRO) Build', 'cf')
        }, {
            brand_replacement = "OnePlus",
            device_replacement = "OnePlus $1",
            model_replacement = "$1",
            regex = "; (ONE [a-zA-Z]\\d+) Build/",
            regex_compiled = lrex.new('; (ONE [a-zA-Z]\\d+) Build/', 'cf')
        }, {
            brand_replacement = "OnePlus",
            device_replacement = "OnePlus $1",
            model_replacement = "$1",
            regex = "; (ONEPLUS [a-zA-Z]\\d+) Build/",
            regex_compiled = lrex.new('; (ONEPLUS [a-zA-Z]\\d+) Build/', 'cf')
        }, {
            brand_replacement = "Orion",
            device_replacement = "Orion $1",
            model_replacement = "$1",
            regex = "; *(TP-\\d+) Build/",
            regex_compiled = lrex.new('; *(TP-\\d+) Build/', 'cf')
        }, {
            brand_replacement = "PackardBell",
            device_replacement = "PackardBell $1",
            model_replacement = "$1",
            regex = "; *(G100W?) Build/",
            regex_compiled = lrex.new('; *(G100W?) Build/', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(Panasonic)[_ ]([^;/]+) Build",
            regex_compiled = lrex.new('; *(Panasonic)[_ ]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Panasonic",
            device_replacement = "Panasonic $1",
            model_replacement = "$1",
            regex = "; *(FZ-A1B|JT-B1) Build",
            regex_compiled = lrex.new('; *(FZ-A1B|JT-B1) Build', 'cf')
        }, {
            brand_replacement = "Panasonic",
            device_replacement = "Panasonic $1",
            model_replacement = "$1",
            regex = "; *(dL1|DL1) Build",
            regex_compiled = lrex.new('; *(dL1|DL1) Build', 'cf')
        }, {
            brand_replacement = "Pantech",
            device_replacement = "Pantech $1$2",
            model_replacement = "$1$2",
            regex = "; *(SKY[ _])?(IM\\-[AT]\\d{3}[^;/]+).* Build/",
            regex_compiled = lrex.new('; *(SKY[ _])?(IM\\-[AT]\\d{3}[^;/]+).* Build/', 'cf')
        }, {
            brand_replacement = "Pantech",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *((?:ADR8995|ADR910L|ADR930L|ADR930VW|PTL21|P8000)(?: 4G)?) Build/",
            regex_compiled = lrex.new('; *((?:ADR8995|ADR910L|ADR930L|ADR930VW|PTL21|P8000)(?: 4G)?) Build/', 'cf')
        }, {
            brand_replacement = "Pantech",
            device_replacement = "Pantech $1",
            model_replacement = "$1",
            regex = "; *Pantech([^;/]+).* Build/",
            regex_compiled = lrex.new('; *Pantech([^;/]+).* Build/', 'cf')
        }, {
            brand_replacement = "Papyre",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(papyre)[ _\\-]([^;/]+) Build/",
            regex_compiled = lrex.new('; *(papyre)[ _\\-]([^;/]+) Build/', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Pearl",
            device_replacement = "Pearl $1",
            model_replacement = "$1",
            regex = "; *(?:Touchlet )?(X10\\.[^;/]+) Build/",
            regex_compiled = lrex.new('; *(?:Touchlet )?(X10\\.[^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Phicomm",
            device_replacement = "Phicomm $1",
            model_replacement = "$1",
            regex = "; PHICOMM (i800) Build/",
            regex_compiled = lrex.new('; PHICOMM (i800) Build/', 'cf')
        }, {
            brand_replacement = "Phicomm",
            device_replacement = "Phicomm $1",
            model_replacement = "$1",
            regex = "; PHICOMM ([^;/]+) Build/",
            regex_compiled = lrex.new('; PHICOMM ([^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Phicomm",
            device_replacement = "Phicomm $1",
            model_replacement = "$1",
            regex = "; *(FWS\\d{3}[^;/]+) Build/",
            regex_compiled = lrex.new('; *(FWS\\d{3}[^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Philips",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(D633|D822|D833|T539|T939|V726|W335|W336|W337|W3568|W536|W5510|W626|W632|W6350|W6360|W6500|W732|W736|W737|W7376|W820|W832|W8355|W8500|W8510|W930) Build",
            regex_compiled = lrex.new('; *(D633|D822|D833|T539|T939|V726|W335|W336|W337|W3568|W536|W5510|W626|W632|W6350|W6360|W6500|W732|W736|W737|W7376|W820|W832|W8355|W8500|W8510|W930) Build', 'cf')
        }, {
            brand_replacement = "Philips",
            device_replacement = "Philips $1",
            model_replacement = "$1",
            regex = "; *(?:Philips|PHILIPS)[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *(?:Philips|PHILIPS)[ _]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Pipo",
            device_replacement = "Pipo $1$2",
            model_replacement = "$1$2",
            regex = "Android 4\\..*; *(M[12356789]|U[12368]|S[123])\\ ?(pro)? Build",
            regex_compiled = lrex.new('Android 4\\..*; *(M[12356789]|U[12368]|S[123])\\ ?(pro)? Build', 'cf')
        }, {
            brand_replacement = "Ployer",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(MOMO[^;/]+) Build",
            regex_compiled = lrex.new('; *(MOMO[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Polaroid",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(?:Polaroid[ _])?((?:MIDC\\d{3,}|PMID\\d{2,}|PTAB\\d{3,})[^;/]*)(\\/[^;/]*)? Build/",
            regex_compiled = lrex.new('; *(?:Polaroid[ _])?((?:MIDC\\d{3,}|PMID\\d{2,}|PTAB\\d{3,})[^;/]*)(\\/[^;/]*)? Build/', 'cf')
        }, {
            brand_replacement = "Polaroid",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(?:Polaroid )(Tablet) Build/",
            regex_compiled = lrex.new('; *(?:Polaroid )(Tablet) Build/', 'cf')
        }, {
            brand_replacement = "Pomp",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(POMP)[ _\\-](.+?) *(?:Build|[;/\\)])",
            regex_compiled = lrex.new('; *(POMP)[ _\\-](.+?) *(?:Build|[;/\\)])', 'cf')
        }, {
            brand_replacement = "Positivo",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(TB07STA|TB10STA|TB07FTA|TB10FTA) Build/",
            regex_compiled = lrex.new('; *(TB07STA|TB10STA|TB07FTA|TB10FTA) Build/', 'cf')
        }, {
            brand_replacement = "Positivo",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(?:Positivo )?((?:YPY|Ypy)[^;/]+) Build/",
            regex_compiled = lrex.new('; *(?:Positivo )?((?:YPY|Ypy)[^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "POV",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(MOB-[^;/]+) Build/",
            regex_compiled = lrex.new('; *(MOB-[^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "POV",
            device_replacement = "POV $1",
            model_replacement = "$1",
            regex = "; *POV[ _\\-]([^;/]+) Build/",
            regex_compiled = lrex.new('; *POV[ _\\-]([^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "POV",
            device_replacement = "POV $1",
            model_replacement = "$1",
            regex = "; *((?:TAB-PLAYTAB|TAB-PROTAB|PROTAB|PlayTabPro|Mobii[ _\\-]|TAB-P)[^;/]*) Build/",
            regex_compiled = lrex.new('; *((?:TAB-PLAYTAB|TAB-PROTAB|PROTAB|PlayTabPro|Mobii[ _\\-]|TAB-P)[^;/]*) Build/', 'cf')
        }, {
            brand_replacement = "Prestigio",
            device_replacement = "Prestigio $1",
            model_replacement = "$1",
            regex = "; *(?:Prestigio )?((?:PAP|PMP)\\d[^;/]+) Build/",
            regex_compiled = lrex.new('; *(?:Prestigio )?((?:PAP|PMP)\\d[^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Proscan",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(PLT[0-9]{4}.*) Build/",
            regex_compiled = lrex.new('; *(PLT[0-9]{4}.*) Build/', 'cf')
        }, {
            brand_replacement = "Qmobile",
            device_replacement = "$1 $2",
            model_replacement = "$1 $2",
            regex = "; *(A2|A5|A8|A900)_?(Classic)? Build",
            regex_compiled = lrex.new('; *(A2|A5|A8|A900)_?(Classic)? Build', 'cf')
        }, {
            brand_replacement = "Qmobile",
            device_replacement = "Qmobile $2 $3",
            model_replacement = "$2 $3",
            regex = "; *(Q[Mm]obile)_([^_]+)_([^_]+) Build",
            regex_compiled = lrex.new('; *(Q[Mm]obile)_([^_]+)_([^_]+) Build', 'cf')
        }, {
            brand_replacement = "Qmobile",
            device_replacement = "Qmobile $2",
            model_replacement = "$2",
            regex = "; *(Q\\-?[Mm]obile)[_ ](A[^;/]+) Build",
            regex_compiled = lrex.new('; *(Q\\-?[Mm]obile)[_ ](A[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Qmobilevn",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(Q\\-Smart)[ _]([^;/]+) Build/",
            regex_compiled = lrex.new('; *(Q\\-Smart)[ _]([^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Qmobilevn",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(Q\\-?[Mm]obile)[ _\\-](S[^;/]+) Build/",
            regex_compiled = lrex.new('; *(Q\\-?[Mm]obile)[ _\\-](S[^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Quanta",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(TA1013) Build",
            regex_compiled = lrex.new('; *(TA1013) Build', 'cf')
        }, {
            brand_replacement = "RCA",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; (RCT\\w+) Build/",
            regex_compiled = lrex.new('; (RCT\\w+) Build/', 'cf')
        }, {
            brand_replacement = "RCA",
            device_replacement = "RCA $1",
            model_replacement = "$1",
            regex = "; RCA (\\w+) Build/",
            regex_compiled = lrex.new('; RCA (\\w+) Build/', 'cf')
        }, {
            brand_replacement = "Rockchip",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(RK\\d+),? Build/",
            regex_compiled = lrex.new('; *(RK\\d+),? Build/', 'cf')
        }, {
            brand_replacement = "Rockchip",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = " Build/(RK\\d+)",
            regex_compiled = lrex.new(' Build/(RK\\d+)', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $1$2",
            model_replacement = "$2",
            regex = "; *(SAMSUNG |Samsung )?((?:Galaxy (?:Note II|S\\d)|GT-I9082|GT-I9205|GT-N7\\d{3}|SM-N9005)[^;/]*)\\/?[^;/]* Build/",
            regex_compiled = lrex.new('; *(SAMSUNG |Samsung )?((?:Galaxy (?:Note II|S\\d)|GT-I9082|GT-I9205|GT-N7\\d{3}|SM-N9005)[^;/]*)\\/?[^;/]* Build/', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $1$2",
            model_replacement = "$2",
            regex = "; *(Google )?(Nexus [Ss](?: 4G)?) Build/",
            regex_compiled = lrex.new('; *(Google )?(Nexus [Ss](?: 4G)?) Build/', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $2",
            model_replacement = "$2",
            regex = "; *(SAMSUNG |Samsung )([^\\/]*)\\/[^ ]* Build/",
            regex_compiled = lrex.new('; *(SAMSUNG |Samsung )([^\\/]*)\\/[^ ]* Build/', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $1",
            model_replacement = "$1",
            regex = "; *(Galaxy(?: Ace| Nexus| S ?II+|Nexus S| with MCR 1.2| Mini Plus 4G)?) Build/",
            regex_compiled = lrex.new('; *(Galaxy(?: Ace| Nexus| S ?II+|Nexus S| with MCR 1.2| Mini Plus 4G)?) Build/', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $2",
            model_replacement = "$2",
            regex = "; *(SAMSUNG[ _\\-] *)+([^;/]+) Build",
            regex_compiled = lrex.new('; *(SAMSUNG[ _\\-] *)+([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $1$2$3",
            model_replacement = "$2",
            regex = "; *(SAMSUNG-)?(GT\\-[BINPS]\\d{4}[^\\/]*)(\\/[^ ]*) Build",
            regex_compiled = lrex.new('; *(SAMSUNG-)?(GT\\-[BINPS]\\d{4}[^\\/]*)(\\/[^ ]*) Build', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $1",
            model_replacement = "$1",
            regex = "(?:; *|^)((?:GT\\-[BIiNPS]\\d{4}|I9\\d{2}0[A-Za-z\\+]?\\b)[^;/\\)]*?)(?:Build|Linux|MIUI|[;/\\)])",
            regex_compiled = lrex.new('(?:; *|^)((?:GT\\-[BIiNPS]\\d{4}|I9\\d{2}0[A-Za-z\\+]?\\b)[^;/\\)]*?)(?:Build|Linux|MIUI|[;/\\)])', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $1$2",
            model_replacement = "$2",
            regex = "; (SAMSUNG-)([A-Za-z0-9\\-]+).* Build/",
            regex_compiled = lrex.new('; (SAMSUNG-)([A-Za-z0-9\\-]+).* Build/', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $1",
            model_replacement = "$1",
            regex = "; *((?:SCH|SGH|SHV|SHW|SPH|SC|SM)\\-[A-Za-z0-9 ]+)(/?[^ ]*)? Build",
            regex_compiled = lrex.new('; *((?:SCH|SGH|SHV|SHW|SPH|SC|SM)\\-[A-Za-z0-9 ]+)(/?[^ ]*)? Build', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $1",
            model_replacement = "$1",
            regex = " ((?:SCH)\\-[A-Za-z0-9 ]+)(/?[^ ]*)? Build",
            regex_compiled = lrex.new(' ((?:SCH)\\-[A-Za-z0-9 ]+)(/?[^ ]*)? Build', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $1",
            model_replacement = "$1",
            regex = "; *(Behold ?(?:2|II)|YP\\-G[^;/]+|EK-GC100|SCL21|I9300) Build",
            regex_compiled = lrex.new('; *(Behold ?(?:2|II)|YP\\-G[^;/]+|EK-GC100|SCL21|I9300) Build', 'cf')
        }, {
            brand_replacement = "Sharp",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(SH\\-?\\d\\d[^;/]+|SBM\\d[^;/]+) Build",
            regex_compiled = lrex.new('; *(SH\\-?\\d\\d[^;/]+|SBM\\d[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Sharp",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(SHARP[ -])([^;/]+) Build",
            regex_compiled = lrex.new('; *(SHARP[ -])([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Simvalley",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(SPX[_\\-]\\d[^;/]*) Build/",
            regex_compiled = lrex.new('; *(SPX[_\\-]\\d[^;/]*) Build/', 'cf')
        }, {
            brand_replacement = "Simvalley",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(SX7\\-PEARL\\.GmbH) Build/",
            regex_compiled = lrex.new('; *(SX7\\-PEARL\\.GmbH) Build/', 'cf')
        }, {
            brand_replacement = "Simvalley",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(SP[T]?\\-\\d{2}[^;/]*) Build/",
            regex_compiled = lrex.new('; *(SP[T]?\\-\\d{2}[^;/]*) Build/', 'cf')
        }, {
            brand_replacement = "SKtelesys",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(SK\\-.*) Build/",
            regex_compiled = lrex.new('; *(SK\\-.*) Build/', 'cf')
        }, {
            brand_replacement = "Skytex",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(?:SKYTEX|SX)-([^;/]+) Build",
            regex_compiled = lrex.new('; *(?:SKYTEX|SX)-([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Skytex",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(IMAGINE [^;/]+) Build",
            regex_compiled = lrex.new('; *(IMAGINE [^;/]+) Build', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(SmartQ) ?([^;/]+) Build/",
            regex_compiled = lrex.new('; *(SmartQ) ?([^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Smartbitt",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(WF7C|WF10C|SBT[^;/]+) Build",
            regex_compiled = lrex.new('; *(WF7C|WF10C|SBT[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Sharp",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(SBM(?:003SH|005SH|006SH|007SH|102SH)) Build",
            regex_compiled = lrex.new('; *(SBM(?:003SH|005SH|006SH|007SH|102SH)) Build', 'cf')
        }, {
            brand_replacement = "Panasonic",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(003P|101P|101P11C|102P) Build",
            regex_compiled = lrex.new('; *(003P|101P|101P11C|102P) Build', 'cf')
        }, {
            brand_replacement = "ZTE",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(00\\dZ) Build/",
            regex_compiled = lrex.new('; *(00\\dZ) Build/', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; HTC(X06HT) Build",
            regex_compiled = lrex.new('; HTC(X06HT) Build', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(001HT|X06HT) Build",
            regex_compiled = lrex.new('; *(001HT|X06HT) Build', 'cf')
        }, {
            brand_replacement = "Motorola",
            device_replacement = "$1",
            model_replacement = "XT902",
            regex = "; *(201M) Build",
            regex_compiled = lrex.new('; *(201M) Build', 'cf')
        }, {
            brand_replacement = "Trekstor",
            device_replacement = "Trekstor $1",
            model_replacement = "$1",
            regex = "; *(ST\\d{4}.*)Build/ST",
            regex_compiled = lrex.new('; *(ST\\d{4}.*)Build/ST', 'cf')
        }, {
            brand_replacement = "Trekstor",
            device_replacement = "Trekstor $1",
            model_replacement = "$1",
            regex = "; *(ST\\d{4}.*) Build/",
            regex_compiled = lrex.new('; *(ST\\d{4}.*) Build/', 'cf')
        }, {
            brand_replacement = "SonyEricsson",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(Sony ?Ericsson ?)([^;/]+) Build",
            regex_compiled = lrex.new('; *(Sony ?Ericsson ?)([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "SonyEricsson",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *((?:SK|ST|E|X|LT|MK|MT|WT)\\d{2}[a-z0-9]*(?:-o)?|R800i|U20i) Build",
            regex_compiled = lrex.new('; *((?:SK|ST|E|X|LT|MK|MT|WT)\\d{2}[a-z0-9]*(?:-o)?|R800i|U20i) Build', 'cf')
        }, {
            brand_replacement = "SonyEricsson",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(Xperia (?:A8|Arc|Acro|Active|Live with Walkman|Mini|Neo|Play|Pro|Ray|X\\d+)[^;/]*) Build",
            regex_compiled = lrex.new('; *(Xperia (?:A8|Arc|Acro|Active|Live with Walkman|Mini|Neo|Play|Pro|Ray|X\\d+)[^;/]*) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Sony",
            device_replacement = "Sony $1",
            model_replacement = "$1",
            regex = "; Sony (Tablet[^;/]+) Build",
            regex_compiled = lrex.new('; Sony (Tablet[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Sony",
            device_replacement = "Sony $1",
            model_replacement = "$1",
            regex = "; Sony ([^;/]+) Build",
            regex_compiled = lrex.new('; Sony ([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(Sony)([A-Za-z0-9\\-]+) Build",
            regex_compiled = lrex.new('; *(Sony)([A-Za-z0-9\\-]+) Build', 'cf')
        }, {
            brand_replacement = "Sony",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(Xperia [^;/]+) Build",
            regex_compiled = lrex.new('; *(Xperia [^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Sony",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(C(?:1[0-9]|2[0-9]|53|55|6[0-9])[0-9]{2}|D[25]\\d{3}|D6[56]\\d{2}) Build",
            regex_compiled = lrex.new('; *(C(?:1[0-9]|2[0-9]|53|55|6[0-9])[0-9]{2}|D[25]\\d{3}|D6[56]\\d{2}) Build', 'cf')
        }, {
            brand_replacement = "Sony",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(SGP\\d{3}|SGPT\\d{2}) Build",
            regex_compiled = lrex.new('; *(SGP\\d{3}|SGPT\\d{2}) Build', 'cf')
        }, {
            brand_replacement = "Sony",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(NW-Z1000Series) Build",
            regex_compiled = lrex.new('; *(NW-Z1000Series) Build', 'cf')
        }, {
            brand_replacement = "Sony",
            device_replacement = "PlayStation 3",
            model_replacement = "PlayStation 3",
            regex = "PLAYSTATION 3",
            regex_compiled = lrex.new('PLAYSTATION 3', 'cf')
        }, {
            brand_replacement = "Sony",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "(PlayStation (?:Portable|Vita|\\d+))",
            regex_compiled = lrex.new('(PlayStation (?:Portable|Vita|\\d+))', 'cf')
        }, {
            brand_replacement = "Spice",
            device_replacement = "$1$2$3$4",
            model_replacement = "Mi$4",
            regex = "; *((?:CSL_Spice|Spice|SPICE|CSL)[ _\\-]?)?([Mm][Ii])([ _\\-])?(\\d{3}[^;/]*) Build/",
            regex_compiled = lrex.new('; *((?:CSL_Spice|Spice|SPICE|CSL)[ _\\-]?)?([Mm][Ii])([ _\\-])?(\\d{3}[^;/]*) Build/', 'cf')
        }, {
            brand_replacement = "Sprint",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(Sprint )(.+?) *(?:Build|[;/])",
            regex_compiled = lrex.new('; *(Sprint )(.+?) *(?:Build|[;/])', 'cf')
        }, {
            brand_replacement = "Sprint",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "\\b(Sprint)[: ]([^;,/ ]+)",
            regex_compiled = lrex.new('\\b(Sprint)[: ]([^;,/ ]+)', 'cf')
        }, {
            brand_replacement = "Tagi",
            device_replacement = "$1$2$3",
            model_replacement = "$2$3",
            regex = "; *(TAGI[ ]?)(MID) ?([^;/]+) Build/",
            regex_compiled = lrex.new('; *(TAGI[ ]?)(MID) ?([^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Tecmobile",
            device_replacement = "Tecmobile $1",
            model_replacement = "$1",
            regex = "; *(Oyster500|Opal 800) Build",
            regex_compiled = lrex.new('; *(Oyster500|Opal 800) Build', 'cf')
        }, {
            brand_replacement = "Tecno",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(TECNO[ _])([^;/]+) Build/",
            regex_compiled = lrex.new('; *(TECNO[ _])([^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *Android for (Telechips|Techvision) ([^ ]+) ",
            regex_compiled = lrex.new('; *Android for (Telechips|Techvision) ([^ ]+) ', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Telstra",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(T-Hub2) Build/",
            regex_compiled = lrex.new('; *(T-Hub2) Build/', 'cf')
        }, {
            brand_replacement = "Terra",
            device_replacement = "Terra $1$2",
            model_replacement = "$1$2",
            regex = "; *(PAD) ?(100[12]) Build/",
            regex_compiled = lrex.new('; *(PAD) ?(100[12]) Build/', 'cf')
        }, {
            brand_replacement = "Texet",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(T[BM]-\\d{3}[^;/]+) Build/",
            regex_compiled = lrex.new('; *(T[BM]-\\d{3}[^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Thalia",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(tolino [^;/]+) Build",
            regex_compiled = lrex.new('; *(tolino [^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Thalia",
            device_replacement = "$1",
            model_replacement = "Tolino Shine",
            regex = "; *Build/.* (TOLINO_BROWSER)",
            regex_compiled = lrex.new('; *Build/.* (TOLINO_BROWSER)', 'cf')
        }, {
            brand_replacement = "Thl",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(?:CJ[ -])?(ThL|THL)[ -]([^;/]+) Build/",
            regex_compiled = lrex.new('; *(?:CJ[ -])?(ThL|THL)[ -]([^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Thl",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(T100|T200|T5|W100|W200|W8s) Build/",
            regex_compiled = lrex.new('; *(T100|T200|T5|W100|W200|W8s) Build/', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "$1",
            model_replacement = "Hero",
            regex = "; *(T-Mobile[ _]G2[ _]Touch) Build",
            regex_compiled = lrex.new('; *(T-Mobile[ _]G2[ _]Touch) Build', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "$1",
            model_replacement = "Desire Z",
            regex = "; *(T-Mobile[ _]G2) Build",
            regex_compiled = lrex.new('; *(T-Mobile[ _]G2) Build', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "$1",
            model_replacement = "U8730",
            regex = "; *(T-Mobile myTouch Q) Build",
            regex_compiled = lrex.new('; *(T-Mobile myTouch Q) Build', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "$1",
            model_replacement = "U8680",
            regex = "; *(T-Mobile myTouch) Build",
            regex_compiled = lrex.new('; *(T-Mobile myTouch) Build', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "$1",
            model_replacement = "Espresso",
            regex = "; *(T-Mobile_Espresso) Build",
            regex_compiled = lrex.new('; *(T-Mobile_Espresso) Build', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "$1",
            model_replacement = "Dream",
            regex = "; *(T-Mobile G1) Build",
            regex_compiled = lrex.new('; *(T-Mobile G1) Build', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "$1$2 $3 $4",
            model_replacement = "$2 $3 $4",
            regex = "\\b(T-Mobile ?)?(myTouch)[ _]?([34]G)[ _]?([^\\/]*) (?:Mozilla|Build)",
            regex_compiled = lrex.new('\\b(T-Mobile ?)?(myTouch)[ _]?([34]G)[ _]?([^\\/]*) (?:Mozilla|Build)', 'cf')
        }, {
            brand_replacement = "Tmobile",
            device_replacement = "$1 $2 $3",
            model_replacement = "$2 $3",
            regex = "\\b(T-Mobile)_([^_]+)_(.*) Build",
            regex_compiled = lrex.new('\\b(T-Mobile)_([^_]+)_(.*) Build', 'cf')
        }, {
            brand_replacement = "Tmobile",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "\\b(T-Mobile)[_ ]?(.*?)Build",
            regex_compiled = lrex.new('\\b(T-Mobile)[_ ]?(.*?)Build', 'cf')
        }, {
            brand_replacement = "Tomtec",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = " (ATP[0-9]{4}) Build",
            regex_compiled = lrex.new(' (ATP[0-9]{4}) Build', 'cf')
        }, {
            brand_replacement = "Tooky",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = " *(TOOKY)[ _\\-]([^;/]+) ?(?:Build|;)",
            regex_compiled = lrex.new(' *(TOOKY)[ _\\-]([^;/]+) ?(?:Build|;)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Toshiba",
            device_replacement = "$1",
            model_replacement = "Folio 100",
            regex = "\\b(TOSHIBA_AC_AND_AZ|TOSHIBA_FOLIO_AND_A|FOLIO_AND_A)",
            regex_compiled = lrex.new('\\b(TOSHIBA_AC_AND_AZ|TOSHIBA_FOLIO_AND_A|FOLIO_AND_A)', 'cf')
        }, {
            brand_replacement = "Toshiba",
            device_replacement = "$1",
            model_replacement = "Folio 100",
            regex = "; *([Ff]olio ?100) Build/",
            regex_compiled = lrex.new('; *([Ff]olio ?100) Build/', 'cf')
        }, {
            brand_replacement = "Toshiba",
            device_replacement = "Toshiba $1",
            model_replacement = "$1",
            regex = "; *(AT[0-9]{2,3}(?:\\-A|LE\\-A|PE\\-A|SE|a)?|AT7-A|AT1S0|Hikari-iFrame/WDPF-[^;/]+|THRiVE|Thrive) Build/",
            regex_compiled = lrex.new('; *(AT[0-9]{2,3}(?:\\-A|LE\\-A|PE\\-A|SE|a)?|AT7-A|AT1S0|Hikari-iFrame/WDPF-[^;/]+|THRiVE|Thrive) Build/', 'cf')
        }, {
            brand_replacement = "Touchmate",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(TM-MID\\d+[^;/]+|TOUCHMATE|MID-750) Build",
            regex_compiled = lrex.new('; *(TM-MID\\d+[^;/]+|TOUCHMATE|MID-750) Build', 'cf')
        }, {
            brand_replacement = "Touchmate",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(TM-SM\\d+[^;/]+) Build",
            regex_compiled = lrex.new('; *(TM-SM\\d+[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Treq",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(A10 [Bb]asic2?) Build/",
            regex_compiled = lrex.new('; *(A10 [Bb]asic2?) Build/', 'cf')
        }, {
            brand_replacement = "Treq",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(TREQ[ _\\-])([^;/]+) Build",
            regex_compiled = lrex.new('; *(TREQ[ _\\-])([^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Umeox",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(X-?5|X-?3) Build/",
            regex_compiled = lrex.new('; *(X-?5|X-?3) Build/', 'cf')
        }, {
            brand_replacement = "Umeox",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(A502\\+?|A936|A603|X1|X2) Build/",
            regex_compiled = lrex.new('; *(A502\\+?|A936|A603|X1|X2) Build/', 'cf')
        }, {
            brand_replacement = "Versus",
            device_replacement = "Versus $1",
            model_replacement = "$1",
            regex = "(TOUCH(?:TAB|PAD).+?) Build/",
            regex_compiled = lrex.new('(TOUCH(?:TAB|PAD).+?) Build/', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Vertu",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "(VERTU) ([^;/]+) Build/",
            regex_compiled = lrex.new('(VERTU) ([^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Videocon",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(Videocon)[ _\\-]([^;/]+) *(?:Build|;)",
            regex_compiled = lrex.new('; *(Videocon)[ _\\-]([^;/]+) *(?:Build|;)', 'cf')
        }, {
            brand_replacement = "Videocon",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = " (VT\\d{2}[A-Za-z]*) Build",
            regex_compiled = lrex.new(' (VT\\d{2}[A-Za-z]*) Build', 'cf')
        }, {
            brand_replacement = "Viewsonic",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *((?:ViewPad|ViewPhone|VSD)[^;/]+) Build/",
            regex_compiled = lrex.new('; *((?:ViewPad|ViewPhone|VSD)[^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Viewsonic",
            device_replacement = "$1$2",
            model_replacement = "$2",
            regex = "; *(ViewSonic-)([^;/]+) Build/",
            regex_compiled = lrex.new('; *(ViewSonic-)([^;/]+) Build/', 'cf')
        }, {
            brand_replacement = "Viewsonic",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(GTablet.*) Build/",
            regex_compiled = lrex.new('; *(GTablet.*) Build/', 'cf')
        }, {
            brand_replacement = "vivo",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *([Vv]ivo)[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *([Vv]ivo)[ _]([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "(Vodafone) (.*) Build/",
            regex_compiled = lrex.new('(Vodafone) (.*) Build/', 'cf')
        }, {
            brand_replacement = "Walton",
            device_replacement = "Walton $1",
            model_replacement = "$1",
            regex = "; *(?:Walton[ _\\-])?(Primo[ _\\-][^;/]+) Build",
            regex_compiled = lrex.new('; *(?:Walton[ _\\-])?(Primo[ _\\-][^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Wiko",
            device_replacement = "Wiko $1",
            model_replacement = "$1",
            regex = "; *(?:WIKO[ \\-])?(CINK\\+?|BARRY|BLOOM|DARKFULL|DARKMOON|DARKNIGHT|DARKSIDE|FIZZ|HIGHWAY|IGGY|OZZY|RAINBOW|STAIRWAY|SUBLIM|WAX|CINK [^;/]+) Build/",
            regex_compiled = lrex.new('; *(?:WIKO[ \\-])?(CINK\\+?|BARRY|BLOOM|DARKFULL|DARKMOON|DARKNIGHT|DARKSIDE|FIZZ|HIGHWAY|IGGY|OZZY|RAINBOW|STAIRWAY|SUBLIM|WAX|CINK [^;/]+) Build/', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Wellcom",
            device_replacement = "Wellcom $1",
            model_replacement = "$1",
            regex = "; *WellcoM-([^;/]+) Build",
            regex_compiled = lrex.new('; *WellcoM-([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "WeTab",
            device_replacement = "$1",
            model_replacement = "WeTab",
            regex = "(?:(WeTab)-Browser|; (wetab) Build)",
            regex_compiled = lrex.new('(?:(WeTab)-Browser|; (wetab) Build)', 'cf')
        }, {
            brand_replacement = "Wolfgang",
            device_replacement = "Wolfgang $1",
            model_replacement = "$1",
            regex = "; *(AT-AS[^;/]+) Build",
            regex_compiled = lrex.new('; *(AT-AS[^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Woxter",
            device_replacement = "Woxter $1",
            model_replacement = "$1",
            regex = "; *(?:Woxter|Wxt) ([^;/]+) Build",
            regex_compiled = lrex.new('; *(?:Woxter|Wxt) ([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "Yarvik",
            device_replacement = "Yarvik $1",
            model_replacement = "$1",
            regex = "; *(?:Xenta |Luna )?(TAB[234][0-9]{2}|TAB0[78]-\\d{3}|TAB0?9-\\d{3}|TAB1[03]-\\d{3}|SMP\\d{2}-\\d{3}) Build/",
            regex_compiled = lrex.new('; *(?:Xenta |Luna )?(TAB[234][0-9]{2}|TAB0[78]-\\d{3}|TAB0?9-\\d{3}|TAB1[03]-\\d{3}|SMP\\d{2}-\\d{3}) Build/', 'cf')
        }, {
            brand_replacement = "Yifang",
            device_replacement = "Yifang $1$2$3",
            model_replacement = "$2",
            regex = "; *([A-Z]{2,4})(M\\d{3,}[A-Z]{2})([^;\\)\\/]*)(?: Build|[;\\)])",
            regex_compiled = lrex.new('; *([A-Z]{2,4})(M\\d{3,}[A-Z]{2})([^;\\)\\/]*)(?: Build|[;\\)])', 'cf')
        }, {
            brand_replacement = "XiaoMi",
            device_replacement = "XiaoMi $1",
            model_replacement = "$1",
            regex = "; *((MI|HM|MI-ONE|Redmi)[ -](NOTE |Note )?[^;/]*) (Build|MIUI)/",
            regex_compiled = lrex.new('; *((MI|HM|MI-ONE|Redmi)[ -](NOTE |Note )?[^;/]*) (Build|MIUI)/', 'cf')
        }, {
            brand_replacement = "Xolo",
            device_replacement = "Xolo $1",
            model_replacement = "$1",
            regex = "; *XOLO[ _]([^;/]*tab.*) Build",
            regex_compiled = lrex.new('; *XOLO[ _]([^;/]*tab.*) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Xolo",
            device_replacement = "Xolo $1",
            model_replacement = "$1",
            regex = "; *XOLO[ _]([^;/]+) Build",
            regex_compiled = lrex.new('; *XOLO[ _]([^;/]+) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Xolo",
            device_replacement = "Xolo $1",
            model_replacement = "$1",
            regex = "; *(q\\d0{2,3}[a-z]?) Build",
            regex_compiled = lrex.new('; *(q\\d0{2,3}[a-z]?) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Xoro",
            device_replacement = "Xoro $1",
            model_replacement = "$1",
            regex = "; *(PAD ?[79]\\d+[^;/]*|TelePAD\\d+[^;/]) Build",
            regex_compiled = lrex.new('; *(PAD ?[79]\\d+[^;/]*|TelePAD\\d+[^;/]) Build', 'cf')
        }, {
            brand_replacement = "Zopo",
            device_replacement = "$1$2$3",
            model_replacement = "$1$2$3",
            regex = "; *(?:(?:ZOPO|Zopo)[ _]([^;/]+)|(ZP ?(?:\\d{2}[^;/]+|C2))|(C[2379])) Build",
            regex_compiled = lrex.new('; *(?:(?:ZOPO|Zopo)[ _]([^;/]+)|(ZP ?(?:\\d{2}[^;/]+|C2))|(C[2379])) Build', 'cf')
        }, {
            brand_replacement = "ZiiLabs",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(ZiiLABS) (Zii[^;/]*) Build",
            regex_compiled = lrex.new('; *(ZiiLABS) (Zii[^;/]*) Build', 'cf')
        }, {
            brand_replacement = "ZiiLabs",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "; *(Zii)_([^;/]*) Build",
            regex_compiled = lrex.new('; *(Zii)_([^;/]*) Build', 'cf')
        }, {
            brand_replacement = "ZTE",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(ARIZONA|(?:ATLAS|Atlas) W|D930|Grand (?:[SX][^;]*|Era|Memo[^;]*)|JOE|(?:Kis|KIS)\\b[^;]*|Libra|Light [^;]*|N8[056][01]|N850L|N8000|N9[15]\\d{2}|N9810|NX501|Optik|(?:Vip )Racer[^;]*|RacerII|RACERII|San Francisco[^;]*|V9[AC]|V55|V881|Z[679][0-9]{2}[A-z]?) Build",
            regex_compiled = lrex.new('; *(ARIZONA|(?:ATLAS|Atlas) W|D930|Grand (?:[SX][^;]*|Era|Memo[^;]*)|JOE|(?:Kis|KIS)\\b[^;]*|Libra|Light [^;]*|N8[056][01]|N850L|N8000|N9[15]\\d{2}|N9810|NX501|Optik|(?:Vip )Racer[^;]*|RacerII|RACERII|San Francisco[^;]*|V9[AC]|V55|V881|Z[679][0-9]{2}[A-z]?) Build', 'cf')
        }, {
            brand_replacement = "ZTE",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *([A-Z]\\d+)_USA_[^;]* Build",
            regex_compiled = lrex.new('; *([A-Z]\\d+)_USA_[^;]* Build', 'cf')
        }, {
            brand_replacement = "ZTE",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(SmartTab\\d+)[^;]* Build",
            regex_compiled = lrex.new('; *(SmartTab\\d+)[^;]* Build', 'cf')
        }, {
            brand_replacement = "ZTE",
            device_replacement = "ZTE Blade$1",
            model_replacement = "Blade$1",
            regex = "; *(?:Blade|BLADE|ZTE-BLADE)([^;/]*) Build",
            regex_compiled = lrex.new('; *(?:Blade|BLADE|ZTE-BLADE)([^;/]*) Build', 'cf')
        }, {
            brand_replacement = "ZTE",
            device_replacement = "ZTE Skate$1",
            model_replacement = "Skate$1",
            regex = "; *(?:Skate|SKATE|ZTE-SKATE)([^;/]*) Build",
            regex_compiled = lrex.new('; *(?:Skate|SKATE|ZTE-SKATE)([^;/]*) Build', 'cf')
        }, {
            brand_replacement = "ZTE",
            device_replacement = "$1$2",
            model_replacement = "$1$2",
            regex = "; *(Orange |Optimus )(Monte Carlo|San Francisco) Build",
            regex_compiled = lrex.new('; *(Orange |Optimus )(Monte Carlo|San Francisco) Build', 'cf')
        }, {
            brand_replacement = "ZTE",
            device_replacement = "ZTE $1",
            model_replacement = "$1",
            regex = "; *(?:ZXY-ZTE_|ZTE\\-U |ZTE[\\- _]|ZTE-C[_ ])([^;/]+) Build",
            regex_compiled = lrex.new('; *(?:ZXY-ZTE_|ZTE\\-U |ZTE[\\- _]|ZTE-C[_ ])([^;/]+) Build', 'cf')
        }, {
            brand_replacement = "ZTE",
            device_replacement = "$1 $2",
            model_replacement = "$1 $2",
            regex = "; (BASE) (lutea|Lutea 2|Tab[^;]*) Build",
            regex_compiled = lrex.new('; (BASE) (lutea|Lutea 2|Tab[^;]*) Build', 'cf')
        }, {
            brand_replacement = "ZTE",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; (Avea inTouch 2|soft stone|tmn smart a7|Movistar[ _]Link) Build",
            regex_compiled = lrex.new('; (Avea inTouch 2|soft stone|tmn smart a7|Movistar[ _]Link) Build', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "ZTE",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(vp9plus)\\)",
            regex_compiled = lrex.new('; *(vp9plus)\\)', 'cf')
        }, {
            brand_replacement = "Zync",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; ?(Cloud[ _]Z5|z1000|Z99 2G|z99|z930|z999|z990|z909|Z919|z900) Build/",
            regex_compiled = lrex.new('; ?(Cloud[ _]Z5|z1000|Z99 2G|z99|z930|z999|z990|z909|Z919|z900) Build/', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = "Kindle Fire",
            model_replacement = "Kindle Fire",
            regex = "; ?(KFOT|Kindle Fire) Build\\b",
            regex_compiled = lrex.new('; ?(KFOT|Kindle Fire) Build\\b', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = "Kindle Fire 2",
            model_replacement = "Kindle Fire 2",
            regex = "; ?(KFOTE|Amazon Kindle Fire2) Build\\b",
            regex_compiled = lrex.new('; ?(KFOTE|Amazon Kindle Fire2) Build\\b', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = "Kindle Fire HD",
            model_replacement = 'Kindle Fire HD 7"',
            regex = "; ?(KFTT) Build\\b",
            regex_compiled = lrex.new('; ?(KFTT) Build\\b', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = 'Kindle Fire HD 8.9" WiFi',
            model_replacement = 'Kindle Fire HD 8.9" WiFi',
            regex = "; ?(KFJWI) Build\\b",
            regex_compiled = lrex.new('; ?(KFJWI) Build\\b', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = 'Kindle Fire HD 8.9" 4G',
            model_replacement = 'Kindle Fire HD 8.9" 4G',
            regex = "; ?(KFJWA) Build\\b",
            regex_compiled = lrex.new('; ?(KFJWA) Build\\b', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = 'Kindle Fire HD 7" WiFi',
            model_replacement = 'Kindle Fire HD 7" WiFi',
            regex = "; ?(KFSOWI) Build\\b",
            regex_compiled = lrex.new('; ?(KFSOWI) Build\\b', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = 'Kindle Fire HDX 7" WiFi',
            model_replacement = 'Kindle Fire HDX 7" WiFi',
            regex = "; ?(KFTHWI) Build\\b",
            regex_compiled = lrex.new('; ?(KFTHWI) Build\\b', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = 'Kindle Fire HDX 7" 4G',
            model_replacement = 'Kindle Fire HDX 7" 4G',
            regex = "; ?(KFTHWA) Build\\b",
            regex_compiled = lrex.new('; ?(KFTHWA) Build\\b', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = 'Kindle Fire HDX 8.9" WiFi',
            model_replacement = 'Kindle Fire HDX 8.9" WiFi',
            regex = "; ?(KFAPWI) Build\\b",
            regex_compiled = lrex.new('; ?(KFAPWI) Build\\b', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = 'Kindle Fire HDX 8.9" 4G',
            model_replacement = 'Kindle Fire HDX 8.9" 4G',
            regex = "; ?(KFAPWA) Build\\b",
            regex_compiled = lrex.new('; ?(KFAPWA) Build\\b', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; ?Amazon ([^;/]+) Build\\b",
            regex_compiled = lrex.new('; ?Amazon ([^;/]+) Build\\b', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = "Kindle",
            model_replacement = "Kindle",
            regex = "; ?(Kindle) Build\\b",
            regex_compiled = lrex.new('; ?(Kindle) Build\\b', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = "Kindle Fire",
            model_replacement = "Kindle Fire$2",
            regex = "; ?(Silk)/(\\d+)\\.(\\d+)(?:\\.([0-9\\-]+))? Build\\b",
            regex_compiled = lrex.new('; ?(Silk)/(\\d+)\\.(\\d+)(?:\\.([0-9\\-]+))? Build\\b', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = "Kindle",
            model_replacement = "$1 $2",
            regex = " (Kindle)/(\\d+\\.\\d+)",
            regex_compiled = lrex.new(' (Kindle)/(\\d+\\.\\d+)', 'cf')
        }, {
            brand_replacement = "Amazon",
            device_replacement = "Kindle",
            model_replacement = "Kindle",
            regex = " (Silk|Kindle)/(\\d+)\\.",
            regex_compiled = lrex.new(' (Silk|Kindle)/(\\d+)\\.', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "(sprd)\\-([^/]+)/",
            regex_compiled = lrex.new('(sprd)\\-([^/]+)/', 'cf')
        }, {
            brand_replacement = "Hero",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "; *(H\\d{2}00\\+?) Build",
            regex_compiled = lrex.new('; *(H\\d{2}00\\+?) Build', 'cf')
        }, {
            brand_replacement = "Xianghe",
            device_replacement = "Xianghe $1",
            model_replacement = "$1",
            regex = "; *(iphone|iPhone5) Build/",
            regex_compiled = lrex.new('; *(iphone|iPhone5) Build/', 'cf')
        }, {
            brand_replacement = "Xianghe",
            device_replacement = "Xianghe $1",
            model_replacement = "$1",
            regex = "; *(e\\d{4}[a-z]?_?v\\d+|v89_[^;/]+)[^;/]+ Build/",
            regex_compiled = lrex.new('; *(e\\d{4}[a-z]?_?v\\d+|v89_[^;/]+)[^;/]+ Build/', 'cf')
        }, {
            brand_replacement = "Cellular",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "\\bUSCC[_\\-]?([^ ;/\\)]+)",
            regex_compiled = lrex.new('\\bUSCC[_\\-]?([^ ;/\\)]+)', 'cf')
        }, {
            brand_replacement = "Alcatel",
            device_replacement = "Alcatel $1",
            model_replacement = "$1",
            regex = "Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?)?(?:ALCATEL)[^;]*; *([^;,\\)]+)",
            regex_compiled = lrex.new('Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?)?(?:ALCATEL)[^;]*; *([^;,\\)]+)', 'cf')
        }, {
            brand_replacement = "Asus",
            device_replacement = "Asus $1",
            model_replacement = "$1",
            regex = "Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?|WpsLondonTest; ?)?(?:ASUS|Asus)[^;]*; *([^;,\\)]+)",
            regex_compiled = lrex.new('Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?|WpsLondonTest; ?)?(?:ASUS|Asus)[^;]*; *([^;,\\)]+)', 'cf')
        }, {
            brand_replacement = "Dell",
            device_replacement = "Dell $1",
            model_replacement = "$1",
            regex = "Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?)?(?:DELL|Dell)[^;]*; *([^;,\\)]+)",
            regex_compiled = lrex.new('Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?)?(?:DELL|Dell)[^;]*; *([^;,\\)]+)', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1",
            model_replacement = "$1",
            regex = "Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?|WpsLondonTest; ?)?(?:HTC|Htc|HTC_blocked[^;]*)[^;]*; *(?:HTC)?([^;,\\)]+)",
            regex_compiled = lrex.new('Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?|WpsLondonTest; ?)?(?:HTC|Htc|HTC_blocked[^;]*)[^;]*; *(?:HTC)?([^;,\\)]+)', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "Huawei $1",
            model_replacement = "$1",
            regex = "Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?)?(?:HUAWEI)[^;]*; *(?:HUAWEI )?([^;,\\)]+)",
            regex_compiled = lrex.new('Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?)?(?:HUAWEI)[^;]*; *(?:HUAWEI )?([^;,\\)]+)', 'cf')
        }, {
            brand_replacement = "LG",
            device_replacement = "LG $1",
            model_replacement = "$1",
            regex = "Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?)?(?:LG|Lg)[^;]*; *(?:LG[ \\-])?([^;,\\)]+)",
            regex_compiled = lrex.new('Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?)?(?:LG|Lg)[^;]*; *(?:LG[ \\-])?([^;,\\)]+)', 'cf')
        }, {
            brand_replacement = "Nokia",
            device_replacement = "Lumia $1",
            model_replacement = "Lumia $1",
            regex = "Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?)?(?:rv:11; )?(?:NOKIA|Nokia)[^;]*; *(?:NOKIA ?|Nokia ?|LUMIA ?|[Ll]umia ?)*(\\d{3,}[^;\\)]*)",
            regex_compiled = lrex.new('Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?)?(?:rv:11; )?(?:NOKIA|Nokia)[^;]*; *(?:NOKIA ?|Nokia ?|LUMIA ?|[Ll]umia ?)*(\\d{3,}[^;\\)]*)', 'cf')
        }, {
            brand_replacement = "Nokia",
            device_replacement = "Nokia $1",
            model_replacement = "$1",
            regex = "Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?)?(?:NOKIA|Nokia)[^;]*; *(RM-\\d{3,})",
            regex_compiled = lrex.new('Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?)?(?:NOKIA|Nokia)[^;]*; *(RM-\\d{3,})', 'cf')
        }, {
            brand_replacement = "Nokia",
            device_replacement = "Nokia $1",
            model_replacement = "$1",
            regex = "(?:Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)]|WPDesktop;) ?(?:ARM; ?Touch; ?|Touch; ?)?(?:NOKIA|Nokia)[^;]*; *(?:NOKIA ?|Nokia ?|LUMIA ?|[Ll]umia ?)*([^;\\)]+)",
            regex_compiled = lrex.new('(?:Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)]|WPDesktop;) ?(?:ARM; ?Touch; ?|Touch; ?)?(?:NOKIA|Nokia)[^;]*; *(?:NOKIA ?|Nokia ?|LUMIA ?|[Ll]umia ?)*([^;\\)]+)', 'cf')
        }, {
            brand_replacement = "Microsoft",
            device_replacement = "Microsoft $1",
            model_replacement = "$1",
            regex = "Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?)?(?:Microsoft(?: Corporation)?)[^;]*; *([^;,\\)]+)",
            regex_compiled = lrex.new('Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?)?(?:Microsoft(?: Corporation)?)[^;]*; *([^;,\\)]+)', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $1",
            model_replacement = "$1",
            regex = "Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?|WpsLondonTest; ?)?(?:SAMSUNG)[^;]*; *(?:SAMSUNG )?([^;,\\.\\)]+)",
            regex_compiled = lrex.new('Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?|WpsLondonTest; ?)?(?:SAMSUNG)[^;]*; *(?:SAMSUNG )?([^;,\\.\\)]+)', 'cf')
        }, {
            brand_replacement = "Toshiba",
            device_replacement = "Toshiba $1",
            model_replacement = "$1",
            regex = "Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?|WpsLondonTest; ?)?(?:TOSHIBA|FujitsuToshibaMobileCommun)[^;]*; *([^;,\\)]+)",
            regex_compiled = lrex.new('Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?|WpsLondonTest; ?)?(?:TOSHIBA|FujitsuToshibaMobileCommun)[^;]*; *([^;,\\)]+)', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?|WpsLondonTest; ?)?([^;]+); *([^;,\\)]+)",
            regex_compiled = lrex.new('Windows Phone [^;]+; .*?IEMobile/[^;\\)]+[;\\)] ?(?:ARM; ?Touch; ?|Touch; ?|WpsLondonTest; ?)?([^;]+); *([^;,\\)]+)', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $1",
            model_replacement = "$1",
            regex = "(?:^|; )SAMSUNG\\-([A-Za-z0-9\\-]+).* Bada/",
            regex_compiled = lrex.new('(?:^|; )SAMSUNG\\-([A-Za-z0-9\\-]+).* Bada/', 'cf')
        }, {
            brand_replacement = "Alcatel",
            device_replacement = "Alcatel $1 $2 $3",
            model_replacement = "One Touch $3",
            regex = "\\(Mobile; ALCATEL ?(One|ONE) ?(Touch|TOUCH) ?([^;/]+)(?:/[^;]+)?; rv:[^\\)]+\\) Gecko/[^\\/]+ Firefox/",
            regex_compiled = lrex.new('\\(Mobile; ALCATEL ?(One|ONE) ?(Touch|TOUCH) ?([^;/]+)(?:/[^;]+)?; rv:[^\\)]+\\) Gecko/[^\\/]+ Firefox/', 'cf')
        }, {
            brand_replacement = "ZTE",
            device_replacement = "ZTE $1$2",
            model_replacement = "$1$2",
            regex = "\\(Mobile; (?:ZTE([^;]+)|(OpenC)); rv:[^\\)]+\\) Gecko/[^\\/]+ Firefox/",
            regex_compiled = lrex.new('\\(Mobile; (?:ZTE([^;]+)|(OpenC)); rv:[^\\)]+\\) Gecko/[^\\/]+ Firefox/', 'cf')
        }, {
            brand_replacement = "Nokia",
            device_replacement = "Nokia $1",
            model_replacement = "$1$2",
            regex = "Nokia(N[0-9]+)([A-z_\\-][A-z0-9_\\-]*)",
            regex_compiled = lrex.new('Nokia(N[0-9]+)([A-z_\\-][A-z0-9_\\-]*)', 'cf')
        }, {
            brand_replacement = "Nokia",
            device_replacement = "Nokia $1$2$3",
            model_replacement = "$1$2$3",
            regex = "(?:NOKIA|Nokia)(?:\\-| *)(?:([A-Za-z0-9]+)\\-[0-9a-f]{32}|([A-Za-z0-9\\-]+)(?:UCBrowser)|([A-Za-z0-9\\-]+))",
            regex_compiled = lrex.new('(?:NOKIA|Nokia)(?:\\-| *)(?:([A-Za-z0-9]+)\\-[0-9a-f]{32}|([A-Za-z0-9\\-]+)(?:UCBrowser)|([A-Za-z0-9\\-]+))', 'cf')
        }, {
            brand_replacement = "Nokia",
            device_replacement = "Lumia $1",
            model_replacement = "Lumia $1",
            regex = "Lumia ([A-Za-z0-9\\-]+)",
            regex_compiled = lrex.new('Lumia ([A-Za-z0-9\\-]+)', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "\\(Symbian; U; S60 V5; [A-z]{2}\\-[A-z]{2}; (SonyEricsson|Samsung|Nokia|LG)([^;/]+)\\)",
            regex_compiled = lrex.new('\\(Symbian; U; S60 V5; [A-z]{2}\\-[A-z]{2}; (SonyEricsson|Samsung|Nokia|LG)([^;/]+)\\)', 'cf')
        }, {
            brand_replacement = "Nokia",
            device_replacement = "Nokia $1",
            model_replacement = "$1",
            regex = "\\(Symbian(?:/3)?; U; ([^;]+);",
            regex_compiled = lrex.new('\\(Symbian(?:/3)?; U; ([^;]+);', 'cf')
        }, {
            brand_replacement = "BlackBerry",
            device_replacement = "BlackBerry $1",
            model_replacement = "$1",
            regex = "BB10; ([A-Za-z0-9\\- ]+)\\)",
            regex_compiled = lrex.new('BB10; ([A-Za-z0-9\\- ]+)\\)', 'cf')
        }, {
            brand_replacement = "BlackBerry",
            device_replacement = "BlackBerry Playbook",
            model_replacement = "Playbook",
            regex = "Play[Bb]ook.+RIM Tablet OS",
            regex_compiled = lrex.new('Play[Bb]ook.+RIM Tablet OS', 'cf')
        }, {
            brand_replacement = "BlackBerry",
            device_replacement = "BlackBerry $1",
            model_replacement = "$1",
            regex = "Black[Bb]erry ([0-9]+);",
            regex_compiled = lrex.new('Black[Bb]erry ([0-9]+);', 'cf')
        }, {
            brand_replacement = "BlackBerry",
            device_replacement = "BlackBerry $1",
            model_replacement = "$1",
            regex = "Black[Bb]erry([0-9]+)",
            regex_compiled = lrex.new('Black[Bb]erry([0-9]+)', 'cf')
        }, {
            brand_replacement = "BlackBerry",
            device_replacement = "BlackBerry",
            regex = "Black[Bb]erry;",
            regex_compiled = lrex.new('Black[Bb]erry;', 'cf')
        }, {
            brand_replacement = "Palm",
            device_replacement = "Palm $1",
            model_replacement = "$1",
            regex = "(Pre|Pixi)/\\d+\\.\\d+",
            regex_compiled = lrex.new('(Pre|Pixi)/\\d+\\.\\d+', 'cf')
        }, {
            brand_replacement = "Palm",
            device_replacement = "Palm $1",
            model_replacement = "$1",
            regex = "Palm([0-9]+)",
            regex_compiled = lrex.new('Palm([0-9]+)', 'cf')
        }, {
            brand_replacement = "Palm",
            device_replacement = "Palm Treo $1",
            model_replacement = "Treo $1",
            regex = "Treo([A-Za-z0-9]+)",
            regex_compiled = lrex.new('Treo([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "HP",
            device_replacement = "HP Veer",
            model_replacement = "Veer",
            regex = "webOS.*(P160U(?:NA)?)/(\\d+).(\\d+)",
            regex_compiled = lrex.new('webOS.*(P160U(?:NA)?)/(\\d+).(\\d+)', 'cf')
        }, {
            brand_replacement = "HP",
            device_replacement = "HP TouchPad",
            model_replacement = "TouchPad",
            regex = "(Touch[Pp]ad)/\\d+\\.\\d+",
            regex_compiled = lrex.new('(Touch[Pp]ad)/\\d+\\.\\d+', 'cf')
        }, {
            brand_replacement = "HP",
            device_replacement = "HP iPAQ $1",
            model_replacement = "iPAQ $1",
            regex = "HPiPAQ([A-Za-z0-9]+)/\\d+.\\d+",
            regex_compiled = lrex.new('HPiPAQ([A-Za-z0-9]+)/\\d+.\\d+', 'cf')
        }, {
            brand_replacement = "Sony",
            device_replacement = "$1",
            model_replacement = "$1 $2",
            regex = "PDA; (PalmOS)/sony/model ([a-z]+)/Revision",
            regex_compiled = lrex.new('PDA; (PalmOS)/sony/model ([a-z]+)/Revision', 'cf')
        }, {
            brand_replacement = "Apple",
            device_replacement = "AppleTV",
            model_replacement = "AppleTV",
            regex = "(Apple\\s?TV)",
            regex_compiled = lrex.new('(Apple\\s?TV)', 'cf')
        }, {
            brand_replacement = "Tesla",
            device_replacement = "Tesla Model S",
            model_replacement = "Model S",
            regex = "(QtCarBrowser)",
            regex_compiled = lrex.new('(QtCarBrowser)', 'cf')
        }, {
            brand_replacement = "Apple",
            device_replacement = "$1",
            model_replacement = "$1$2",
            regex = "(iPhone|iPad|iPod)(\\d+,\\d+)",
            regex_compiled = lrex.new('(iPhone|iPad|iPod)(\\d+,\\d+)', 'cf')
        }, {
            brand_replacement = "Apple",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "(iPad)(?:;| Simulator;)",
            regex_compiled = lrex.new('(iPad)(?:;| Simulator;)', 'cf')
        }, {
            brand_replacement = "Apple",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "(iPod)(?:;| touch;| Simulator;)",
            regex_compiled = lrex.new('(iPod)(?:;| touch;| Simulator;)', 'cf')
        }, {
            brand_replacement = "Apple",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "(iPhone)(?:;| Simulator;)",
            regex_compiled = lrex.new('(iPhone)(?:;| Simulator;)', 'cf')
        }, {
            brand_replacement = "Apple",
            device_replacement = "iPhone",
            model_replacement = "iPhone",
            regex = "iPhone",
            regex_compiled = lrex.new('iPhone', 'cf')
        }, {
            brand_replacement = "Apple",
            device_replacement = "$1$2,$3",
            model_replacement = "$1$2,$3",
            regex = "CFNetwork/.* Darwin/\\d.*\\(((?:Mac|iMac|PowerMac|PowerBook)[^\\d]*)(\\d+)(?:,|%2C)(\\d+)",
            regex_compiled = lrex.new('CFNetwork/.* Darwin/\\d.*\\(((?:Mac|iMac|PowerMac|PowerBook)[^\\d]*)(\\d+)(?:,|%2C)(\\d+)', 'cf')
        }, {
            brand_replacement = "Apple",
            device_replacement = "Mac",
            model_replacement = "Mac",
            regex = "CFNetwork/.* Darwin/\\d+\\.\\d+\\.\\d+ \\(x86_64\\)",
            regex_compiled = lrex.new('CFNetwork/.* Darwin/\\d+\\.\\d+\\.\\d+ \\(x86_64\\)', 'cf')
        }, {
            brand_replacement = "Apple",
            device_replacement = "iOS-Device",
            model_replacement = "iOS-Device",
            regex = "CFNetwork/.* Darwin/\\d",
            regex_compiled = lrex.new('CFNetwork/.* Darwin/\\d', 'cf')
        }, {
            brand_replacement = "Apple",
            device_replacement = "iPhone",
            model_replacement = "iPhone",
            regex = "Outlook-(iOS)/\\d+\\.\\d+\\.prod\\.iphone",
            regex_compiled = lrex.new('Outlook-(iOS)/\\d+\\.\\d+\\.prod\\.iphone', 'cf')
        }, {
            brand_replacement = "Acer",
            device_replacement = "Acer $1",
            model_replacement = "$1",
            regex = "acer_([A-Za-z0-9]+)_",
            regex_compiled = lrex.new('acer_([A-Za-z0-9]+)_', 'cf')
        }, {
            brand_replacement = "Alcatel",
            device_replacement = "Alcatel $1",
            model_replacement = "$1",
            regex = "(?:ALCATEL|Alcatel)-([A-Za-z0-9\\-]+)",
            regex_compiled = lrex.new('(?:ALCATEL|Alcatel)-([A-Za-z0-9\\-]+)', 'cf')
        }, {
            brand_replacement = "Amoi",
            device_replacement = "Amoi $1",
            model_replacement = "$1",
            regex = "(?:Amoi|AMOI)\\-([A-Za-z0-9]+)",
            regex_compiled = lrex.new('(?:Amoi|AMOI)\\-([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "Asus",
            device_replacement = "Asus $1",
            model_replacement = "$1",
            regex = "(?:; |\\/|^)((?:Transformer (?:Pad|Prime) |Transformer |PadFone[ _]?)[A-Za-z0-9]*)",
            regex_compiled = lrex.new('(?:; |\\/|^)((?:Transformer (?:Pad|Prime) |Transformer |PadFone[ _]?)[A-Za-z0-9]*)', 'cf')
        }, {
            brand_replacement = "Asus",
            device_replacement = "Asus $1",
            model_replacement = "$1",
            regex = "(?:asus.*?ASUS|Asus|ASUS|asus)[\\- ;]*((?:Transformer (?:Pad|Prime) |Transformer |Padfone |Nexus[ _])?[A-Za-z0-9]+)",
            regex_compiled = lrex.new('(?:asus.*?ASUS|Asus|ASUS|asus)[\\- ;]*((?:Transformer (?:Pad|Prime) |Transformer |Padfone |Nexus[ _])?[A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "Bird",
            device_replacement = "Bird $1",
            model_replacement = "$1",
            regex = "\\bBIRD[ \\-\\.]([A-Za-z0-9]+)",
            regex_compiled = lrex.new('\\bBIRD[ \\-\\.]([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "Dell",
            device_replacement = "Dell $1",
            model_replacement = "$1",
            regex = "\\bDell ([A-Za-z0-9]+)",
            regex_compiled = lrex.new('\\bDell ([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "DoCoMo",
            device_replacement = "DoCoMo $1",
            model_replacement = "$1",
            regex = "DoCoMo/2\\.0 ([A-Za-z0-9]+)",
            regex_compiled = lrex.new('DoCoMo/2\\.0 ([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "DoCoMo",
            device_replacement = "DoCoMo $1",
            model_replacement = "$1",
            regex = "([A-Za-z0-9]+)_W;FOMA",
            regex_compiled = lrex.new('([A-Za-z0-9]+)_W;FOMA', 'cf')
        }, {
            brand_replacement = "DoCoMo",
            device_replacement = "DoCoMo $1",
            model_replacement = "$1",
            regex = "([A-Za-z0-9]+);FOMA",
            regex_compiled = lrex.new('([A-Za-z0-9]+);FOMA', 'cf')
        }, {
            brand_replacement = "HTC",
            device_replacement = "HTC $1",
            model_replacement = "$1",
            regex = "\\b(?:HTC/|HTC/[a-z0-9]+/)?HTC[ _\\-;]? *(.*?)(?:-?Mozilla|fingerPrint|[;/\\(\\)]|$)",
            regex_compiled = lrex.new('\\b(?:HTC/|HTC/[a-z0-9]+/)?HTC[ _\\-;]? *(.*?)(?:-?Mozilla|fingerPrint|[;/\\(\\)]|$)', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "Huawei $1",
            model_replacement = "$1",
            regex = "Huawei([A-Za-z0-9]+)",
            regex_compiled = lrex.new('Huawei([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "Huawei $1",
            model_replacement = "$1",
            regex = "HUAWEI-([A-Za-z0-9]+)",
            regex_compiled = lrex.new('HUAWEI-([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "Huawei",
            device_replacement = "Huawei Vodafone $1",
            model_replacement = "Vodafone $1",
            regex = "vodafone([A-Za-z0-9]+)",
            regex_compiled = lrex.new('vodafone([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "i-mate",
            device_replacement = "i-mate $1",
            model_replacement = "$1",
            regex = "i\\-mate ([A-Za-z0-9]+)",
            regex_compiled = lrex.new('i\\-mate ([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "Kyocera",
            device_replacement = "Kyocera $1",
            model_replacement = "$1",
            regex = "Kyocera\\-([A-Za-z0-9]+)",
            regex_compiled = lrex.new('Kyocera\\-([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "Kyocera",
            device_replacement = "Kyocera $1",
            model_replacement = "$1",
            regex = "KWC\\-([A-Za-z0-9]+)",
            regex_compiled = lrex.new('KWC\\-([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "Lenovo",
            device_replacement = "Lenovo $1",
            model_replacement = "$1",
            regex = "Lenovo[_\\-]([A-Za-z0-9]+)",
            regex_compiled = lrex.new('Lenovo[_\\-]([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "$2",
            device_replacement = "$1",
            model_replacement = "$3",
            regex = "(HbbTV)/[0-9]+\\.[0-9]+\\.[0-9]+ \\([^;]*; *(LG)E *; *([^;]*) *;[^;]*;[^;]*;\\)",
            regex_compiled = lrex.new('(HbbTV)/[0-9]+\\.[0-9]+\\.[0-9]+ \\([^;]*; *(LG)E *; *([^;]*) *;[^;]*;[^;]*;\\)', 'cf')
        }, {
            brand_replacement = "Thomson",
            device_replacement = "$1",
            model_replacement = "$4",
            regex = "(HbbTV)/1\\.1\\.1.*CE-HTML/1\\.\\d;(Vendor/)*(THOM[^;]*?)[;\\s](?:.*SW-Version/.*)*(LF[^;]+);?",
            regex_compiled = lrex.new('(HbbTV)/1\\.1\\.1.*CE-HTML/1\\.\\d;(Vendor/)*(THOM[^;]*?)[;\\s](?:.*SW-Version/.*)*(LF[^;]+);?', 'cf')
        }, {
            brand_replacement = "$2",
            device_replacement = "$1",
            model_replacement = "$3",
            regex = "(HbbTV)(?:/1\\.1\\.1)?(?: ?\\(;;;;;\\))?; *CE-HTML(?:/1\\.\\d)?; *([^ ]+) ([^;]+);",
            regex_compiled = lrex.new('(HbbTV)(?:/1\\.1\\.1)?(?: ?\\(;;;;;\\))?; *CE-HTML(?:/1\\.\\d)?; *([^ ]+) ([^;]+);', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "$1",
            regex = "(HbbTV)/1\\.1\\.1 \\(;;;;;\\) Maple_2011",
            regex_compiled = lrex.new('(HbbTV)/1\\.1\\.1 \\(;;;;;\\) Maple_2011', 'cf')
        }, {
            brand_replacement = "$2$3",
            device_replacement = "$1",
            model_replacement = "$4",
            regex = "(HbbTV)/[0-9]+\\.[0-9]+\\.[0-9]+ \\([^;]*; *(?:CUS:([^;]*)|([^;]+)) *; *([^;]*) *;.*;",
            regex_compiled = lrex.new('(HbbTV)/[0-9]+\\.[0-9]+\\.[0-9]+ \\([^;]*; *(?:CUS:([^;]*)|([^;]+)) *; *([^;]*) *;.*;', 'cf')
        }, {
            device_replacement = "$1",
            regex = "(HbbTV)/[0-9]+\\.[0-9]+\\.[0-9]+",
            regex_compiled = lrex.new('(HbbTV)/[0-9]+\\.[0-9]+\\.[0-9]+', 'cf')
        }, {
            brand_replacement = "LG",
            device_replacement = "NetCast$2",
            model_replacement = "$1",
            regex = 'LGE; (?:Media\\/)?([^;]*);[^;]*;[^;]*;?\\); "?LG NetCast(\\.TV|\\.Media)?-\\d+',
            regex_compiled = lrex.new('LGE; (?:Media\\/)?([^;]*);[^;]*;[^;]*;?\\); \"?LG NetCast(\\.TV|\\.Media)?-\\d+', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "Inettv",
            model_replacement = "$2",
            regex = "InettvBrowser/[0-9]+\\.[0-9A-Z]+ \\([^;]*;(Sony)([^;]*);[^;]*;[^\\)]*\\)",
            regex_compiled = lrex.new('InettvBrowser/[0-9]+\\.[0-9A-Z]+ \\([^;]*;(Sony)([^;]*);[^;]*;[^\\)]*\\)', 'cf')
        }, {
            brand_replacement = "Generic_Inettv",
            device_replacement = "Inettv",
            model_replacement = "$1",
            regex = "InettvBrowser/[0-9]+\\.[0-9A-Z]+ \\([^;]*;([^;]*);[^;]*;[^\\)]*\\)",
            regex_compiled = lrex.new('InettvBrowser/[0-9]+\\.[0-9A-Z]+ \\([^;]*;([^;]*);[^;]*;[^\\)]*\\)', 'cf')
        }, {
            brand_replacement = "Generic_Inettv",
            device_replacement = "Inettv",
            regex = "(?:InettvBrowser|TSBNetTV|NETTV|HBBTV)",
            regex_compiled = lrex.new('(?:InettvBrowser|TSBNetTV|NETTV|HBBTV)', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "Series60/\\d\\.\\d (LG)[\\-]?([A-Za-z0-9 \\-]+)",
            regex_compiled = lrex.new('Series60/\\d\\.\\d (LG)[\\-]?([A-Za-z0-9 \\-]+)', 'cf')
        }, {
            brand_replacement = "LG",
            device_replacement = "LG $1",
            model_replacement = "$1",
            regex = "\\b(?:LGE[ \\-]LG\\-(?:AX)?|LGE |LGE?-LG|LGE?[ \\-]|LG[ /\\-]|lg[\\-])([A-Za-z0-9]+)\\b",
            regex_compiled = lrex.new('\\b(?:LGE[ \\-]LG\\-(?:AX)?|LGE |LGE?-LG|LGE?[ \\-]|LG[ /\\-]|lg[\\-])([A-Za-z0-9]+)\\b', 'cf')
        }, {
            brand_replacement = "LG",
            device_replacement = "LG $1",
            model_replacement = "$1",
            regex = "(?:^LG[\\-]?|^LGE[\\-/]?)([A-Za-z]+[0-9]+[A-Za-z]*)",
            regex_compiled = lrex.new('(?:^LG[\\-]?|^LGE[\\-/]?)([A-Za-z]+[0-9]+[A-Za-z]*)', 'cf')
        }, {
            brand_replacement = "LG",
            device_replacement = "LG $1",
            model_replacement = "$1",
            regex = "^LG([0-9]+[A-Za-z]*)",
            regex_compiled = lrex.new('^LG([0-9]+[A-Za-z]*)', 'cf')
        }, {
            brand_replacement = "Microsoft",
            device_replacement = "Microsoft $1",
            model_replacement = "$1",
            regex = "(KIN\\.[^ ]+) (\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(KIN\\.[^ ]+) (\\d+)\\.(\\d+)', 'cf')
        }, {
            brand_replacement = "Microsoft",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "(?:MSIE|XBMC).*\\b(Xbox)\\b",
            regex_compiled = lrex.new('(?:MSIE|XBMC).*\\b(Xbox)\\b', 'cf')
        }, {
            brand_replacement = "Microsoft",
            device_replacement = "Microsoft Surface RT",
            model_replacement = "Surface RT",
            regex = "; ARM; Trident/6\\.0; Touch[\\);]",
            regex_compiled = lrex.new('; ARM; Trident/6\\.0; Touch[\\);]', 'cf')
        }, {
            brand_replacement = "Motorola",
            device_replacement = "Motorola $1",
            model_replacement = "$1",
            regex = "Motorola\\-([A-Za-z0-9]+)",
            regex_compiled = lrex.new('Motorola\\-([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "Motorola",
            device_replacement = "Motorola $1",
            model_replacement = "$1",
            regex = "MOTO\\-([A-Za-z0-9]+)",
            regex_compiled = lrex.new('MOTO\\-([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "Motorola",
            device_replacement = "Motorola $1",
            model_replacement = "$1",
            regex = "MOT\\-([A-z0-9][A-z0-9\\-]*)",
            regex_compiled = lrex.new('MOT\\-([A-z0-9][A-z0-9\\-]*)', 'cf')
        }, {
            brand_replacement = "Nintendo",
            device_replacement = "Nintendo Wii U",
            model_replacement = "Wii U",
            regex = "Nintendo WiiU",
            regex_compiled = lrex.new('Nintendo WiiU', 'cf')
        }, {
            brand_replacement = "Nintendo",
            device_replacement = "Nintendo $1",
            model_replacement = "$1",
            regex = "Nintendo (DS|3DS|DSi|Wii);",
            regex_compiled = lrex.new('Nintendo (DS|3DS|DSi|Wii);', 'cf')
        }, {
            brand_replacement = "Pantech",
            device_replacement = "Pantech $1",
            model_replacement = "$1",
            regex = "(?:Pantech|PANTECH)[ _-]?([A-Za-z0-9\\-]+)",
            regex_compiled = lrex.new('(?:Pantech|PANTECH)[ _-]?([A-Za-z0-9\\-]+)', 'cf')
        }, {
            brand_replacement = "Philips",
            device_replacement = "Philips $1",
            model_replacement = "$1",
            regex = "Philips([A-Za-z0-9]+)",
            regex_compiled = lrex.new('Philips([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "Philips",
            device_replacement = "Philips $1",
            model_replacement = "$1",
            regex = "Philips ([A-Za-z0-9]+)",
            regex_compiled = lrex.new('Philips ([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $1",
            model_replacement = "$1",
            regex = "(SMART-TV); .* Tizen ",
            regex_compiled = lrex.new('(SMART-TV); .* Tizen ', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $1",
            model_replacement = "$1",
            regex = "SymbianOS/9\\.\\d.* Samsung[/\\-]([A-Za-z0-9 \\-]+)",
            regex_compiled = lrex.new('SymbianOS/9\\.\\d.* Samsung[/\\-]([A-Za-z0-9 \\-]+)', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2$3",
            model_replacement = "$2-$3",
            regex = "(Samsung)(SGH)(i[0-9]+)",
            regex_compiled = lrex.new('(Samsung)(SGH)(i[0-9]+)', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "$1",
            model_replacement = "$1",
            regex = "SAMSUNG-ANDROID-MMS/([^;/]+)",
            regex_compiled = lrex.new('SAMSUNG-ANDROID-MMS/([^;/]+)', 'cf')
        }, {
            brand_replacement = "Samsung",
            device_replacement = "Samsung $1",
            model_replacement = "$1",
            regex = "SAMSUNG(?:; |[ -/])([A-Za-z0-9\\-]+)",
            regex_compiled = lrex.new('SAMSUNG(?:; |[ -/])([A-Za-z0-9\\-]+)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Sega",
            device_replacement = "Sega $1",
            model_replacement = "$1",
            regex = "(Dreamcast)",
            regex_compiled = lrex.new('(Dreamcast)', 'cf')
        }, {
            brand_replacement = "Siemens",
            device_replacement = "Siemens $1",
            model_replacement = "$1",
            regex = "^SIE-([A-Za-z0-9]+)",
            regex_compiled = lrex.new('^SIE-([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "Softbank",
            device_replacement = "Softbank $1",
            model_replacement = "$1",
            regex = "Softbank/[12]\\.0/([A-Za-z0-9]+)",
            regex_compiled = lrex.new('Softbank/[12]\\.0/([A-Za-z0-9]+)', 'cf')
        }, {
            brand_replacement = "SonyEricsson",
            device_replacement = "Ericsson $1",
            model_replacement = "$1",
            regex = "SonyEricsson ?([A-Za-z0-9\\-]+)",
            regex_compiled = lrex.new('SonyEricsson ?([A-Za-z0-9\\-]+)', 'cf')
        }, {
            brand_replacement = "$2",
            device_replacement = "$2 $1",
            model_replacement = "$1",
            regex = "Android [^;]+; ([^ ]+) (Sony)/",
            regex_compiled = lrex.new('Android [^;]+; ([^ ]+) (Sony)/', 'cf')
        }, {
            brand_replacement = "$1",
            device_replacement = "$1 $2",
            model_replacement = "$2",
            regex = "(Sony)(?:BDP\\/|\\/)?([^ /;\\)]+)[ /;\\)]",
            regex_compiled = lrex.new('(Sony)(?:BDP\\/|\\/)?([^ /;\\)]+)[ /;\\)]', 'cf')
        }, {
            brand_replacement = "Apple",
            device_replacement = "iPad",
            model_replacement = "iPad",
            regex = "Puffin/[\\d\\.]+IT",
            regex_compiled = lrex.new('Puffin/[\\d\\.]+IT', 'cf')
        }, {
            brand_replacement = "Apple",
            device_replacement = "iPhone",
            model_replacement = "iPhone",
            regex = "Puffin/[\\d\\.]+IP",
            regex_compiled = lrex.new('Puffin/[\\d\\.]+IP', 'cf')
        }, {
            brand_replacement = "Generic",
            device_replacement = "Generic Tablet",
            model_replacement = "Tablet",
            regex = "Puffin/[\\d\\.]+AT",
            regex_compiled = lrex.new('Puffin/[\\d\\.]+AT', 'cf')
        }, {
            brand_replacement = "Generic",
            device_replacement = "Generic Smartphone",
            model_replacement = "Smartphone",
            regex = "Puffin/[\\d\\.]+AP",
            regex_compiled = lrex.new('Puffin/[\\d\\.]+AP', 'cf')
        }, {
            brand_replacement = "Generic_Android",
            model_replacement = "$1",
            regex = "Android[\\- ][\\d]+\\.[\\d]+; [A-Za-z]{2}\\-[A-Za-z]{0,2}; WOWMobile (.+) Build[/ ]",
            regex_compiled = lrex.new('Android[\\- ][\\d]+\\.[\\d]+; [A-Za-z]{2}\\-[A-Za-z]{0,2}; WOWMobile (.+) Build[/ ]', 'cf')
        }, {
            brand_replacement = "Generic_Android",
            model_replacement = "$1",
            regex = "Android[\\- ][\\d]+\\.[\\d]+\\-update1; [A-Za-z]{2}\\-[A-Za-z]{0,2} *; *(.+?) Build[/ ]",
            regex_compiled = lrex.new('Android[\\- ][\\d]+\\.[\\d]+\\-update1; [A-Za-z]{2}\\-[A-Za-z]{0,2} *; *(.+?) Build[/ ]', 'cf')
        }, {
            brand_replacement = "Generic_Android",
            model_replacement = "$1",
            regex = "Android[\\- ][\\d]+(?:\\.[\\d]+){1,2}; *[A-Za-z]{2}[_\\-][A-Za-z]{0,2}\\-? *; *(.+?) Build[/ ]",
            regex_compiled = lrex.new('Android[\\- ][\\d]+(?:\\.[\\d]+){1,2}; *[A-Za-z]{2}[_\\-][A-Za-z]{0,2}\\-? *; *(.+?) Build[/ ]', 'cf')
        }, {
            brand_replacement = "Generic_Android",
            model_replacement = "$1",
            regex = "Android[\\- ][\\d]+(?:\\.[\\d]+){1,2}; *[A-Za-z]{0,2}\\- *; *(.+?) Build[/ ]",
            regex_compiled = lrex.new('Android[\\- ][\\d]+(?:\\.[\\d]+){1,2}; *[A-Za-z]{0,2}\\- *; *(.+?) Build[/ ]', 'cf')
        }, {
            brand_replacement = "Generic",
            device_replacement = "Generic Smartphone",
            model_replacement = "Smartphone",
            regex = "Android[\\- ][\\d]+(?:\\.[\\d]+){1,2}; *[a-z]{0,2}[_\\-]?[A-Za-z]{0,2};? Build[/ ]",
            regex_compiled = lrex.new('Android[\\- ][\\d]+(?:\\.[\\d]+){1,2}; *[a-z]{0,2}[_\\-]?[A-Za-z]{0,2};? Build[/ ]', 'cf')
        }, {
            brand_replacement = "Generic_Android",
            model_replacement = "$1",
            regex = "Android[\\- ][\\d]+(?:\\.[\\d]+){1,2}; *\\-?[A-Za-z]{2}; *(.+?) Build[/ ]",
            regex_compiled = lrex.new('Android[\\- ][\\d]+(?:\\.[\\d]+){1,2}; *\\-?[A-Za-z]{2}; *(.+?) Build[/ ]', 'cf')
        }, {
            brand_replacement = "Generic_Android",
            model_replacement = "$1",
            regex = "Android[\\- ][\\d]+(?:\\.[\\d]+){1,2}(?:;.*)?; *(.+?) Build[/ ]",
            regex_compiled = lrex.new('Android[\\- ][\\d]+(?:\\.[\\d]+){1,2}(?:;.*)?; *(.+?) Build[/ ]', 'cf')
        }, {
            brand_replacement = "Generic_Inettv",
            model_replacement = "$1",
            regex = "(GoogleTV)",
            regex_compiled = lrex.new('(GoogleTV)', 'cf')
        }, {
            brand_replacement = "Generic_Inettv",
            model_replacement = "$1",
            regex = "(WebTV)/\\d+.\\d+",
            regex_compiled = lrex.new('(WebTV)/\\d+.\\d+', 'cf')
        }, {
            brand_replacement = "Generic_Inettv",
            model_replacement = "$1",
            regex = "^(Roku)/DVP-\\d+\\.\\d+",
            regex_compiled = lrex.new('^(Roku)/DVP-\\d+\\.\\d+', 'cf')
        }, {
            brand_replacement = "Generic",
            device_replacement = "Generic Tablet",
            model_replacement = "Tablet",
            regex = "(Android 3\\.\\d|Opera Tablet|Tablet; .+Firefox/|Android.*(?:Tab|Pad))",
            regex_compiled = lrex.new('(Android 3\\.\\d|Opera Tablet|Tablet; .+Firefox/|Android.*(?:Tab|Pad))', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Generic",
            device_replacement = "Generic Smartphone",
            model_replacement = "Smartphone",
            regex = "(Symbian|\\bS60(Version|V\\d)|\\bS60\\b|\\((Series 60|Windows Mobile|Palm OS|Bada); Opera Mini|Windows CE|Opera Mobi|BREW|Brew|Mobile; .+Firefox/|iPhone OS|Android|MobileSafari|Windows *Phone|\\(webOS/|PalmOS)",
            regex_compiled = lrex.new('(Symbian|\\bS60(Version|V\\d)|\\bS60\\b|\\((Series 60|Windows Mobile|Palm OS|Bada); Opera Mini|Windows CE|Opera Mobi|BREW|Brew|Mobile; .+Firefox/|iPhone OS|Android|MobileSafari|Windows *Phone|\\(webOS/|PalmOS)', 'cf')
        }, {
            brand_replacement = "Generic",
            device_replacement = "Generic Smartphone",
            model_replacement = "Smartphone",
            regex = "(hiptop|avantgo|plucker|xiino|blazer|elaine)",
            regex_compiled = lrex.new('(hiptop|avantgo|plucker|xiino|blazer|elaine)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Spider",
            device_replacement = "Spider",
            model_replacement = "Desktop",
            regex = "(bot|BUbiNG|zao|borg|DBot|oegp|silk|Xenu|zeal|^NING|CCBot|crawl|htdig|lycos|slurp|teoma|voila|yahoo|Sogou|CiBra|Nutch|^Java/|^JNLP/|Daumoa|Daum|Genieo|ichiro|larbin|pompos|Scrapy|snappy|speedy|spider|msnbot|msrbot|vortex|^vortex|crawler|favicon|indexer|Riddler|scooter|scraper|scrubby|WhatWeb|WinHTTP|bingbot|BingPreview|openbot|gigabot|furlbot|polybot|seekbot|^voyager|archiver|Icarus6j|mogimogi|Netvibes|blitzbot|altavista|charlotte|findlinks|Retreiver|TLSProber|WordPress|SeznamBot|ProoXiBot|wsr\\-agent|Squrl Java|EtaoSpider|PaperLiBot|SputnikBot|A6\\-Indexer|netresearch|searchsight|baiduspider|YisouSpider|ICC\\-Crawler|http%20client|Python-urllib|dataparksearch|converacrawler|Screaming Frog|AppEngine-Google|YahooCacheSystem|fast\\-webcrawler|Sogou Pic Spider|semanticdiscovery|Innovazion Crawler|facebookexternalhit|Google.*/\\+/web/snippet|Google-HTTP-Java-Client|BlogBridge|IlTrovatore-Setaccio|InternetArchive|GomezAgent|WebThumbnail|heritrix|NewsGator|PagePeeker|Reaper|ZooShot|holmes|NL-Crawler|Pingdom|StatusCake|WhatsApp|masscan|Google Web Preview|Qwantify|Yeti)",
            regex_compiled = lrex.new('(bot|BUbiNG|zao|borg|DBot|oegp|silk|Xenu|zeal|^NING|CCBot|crawl|htdig|lycos|slurp|teoma|voila|yahoo|Sogou|CiBra|Nutch|^Java/|^JNLP/|Daumoa|Daum|Genieo|ichiro|larbin|pompos|Scrapy|snappy|speedy|spider|msnbot|msrbot|vortex|^vortex|crawler|favicon|indexer|Riddler|scooter|scraper|scrubby|WhatWeb|WinHTTP|bingbot|BingPreview|openbot|gigabot|furlbot|polybot|seekbot|^voyager|archiver|Icarus6j|mogimogi|Netvibes|blitzbot|altavista|charlotte|findlinks|Retreiver|TLSProber|WordPress|SeznamBot|ProoXiBot|wsr\\-agent|Squrl Java|EtaoSpider|PaperLiBot|SputnikBot|A6\\-Indexer|netresearch|searchsight|baiduspider|YisouSpider|ICC\\-Crawler|http%20client|Python-urllib|dataparksearch|converacrawler|Screaming Frog|AppEngine-Google|YahooCacheSystem|fast\\-webcrawler|Sogou Pic Spider|semanticdiscovery|Innovazion Crawler|facebookexternalhit|Google.*/\\+/web/snippet|Google-HTTP-Java-Client|BlogBridge|IlTrovatore-Setaccio|InternetArchive|GomezAgent|WebThumbnail|heritrix|NewsGator|PagePeeker|Reaper|ZooShot|holmes|NL-Crawler|Pingdom|StatusCake|WhatsApp|masscan|Google Web Preview|Qwantify|Yeti)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Generic",
            device_replacement = "Generic Feature Phone",
            model_replacement = "Feature Phone",
            regex = "^(1207|3gso|4thp|501i|502i|503i|504i|505i|506i|6310|6590|770s|802s|a wa|acer|acs\\-|airn|alav|asus|attw|au\\-m|aur |aus |abac|acoo|aiko|alco|alca|amoi|anex|anny|anyw|aptu|arch|argo|bmobile|bell|bird|bw\\-n|bw\\-u|beck|benq|bilb|blac|c55/|cdm\\-|chtm|capi|comp|cond|dall|dbte|dc\\-s|dica|ds\\-d|ds12|dait|devi|dmob|doco|dopo|dorado|el(?:38|39|48|49|50|55|58|68)|el[3456]\\d{2}dual|erk0|esl8|ex300|ez40|ez60|ez70|ezos|ezze|elai|emul|eric|ezwa|fake|fly\\-|fly_|g\\-mo|g1 u|g560|gf\\-5|grun|gene|go.w|good|grad|hcit|hd\\-m|hd\\-p|hd\\-t|hei\\-|hp i|hpip|hs\\-c|htc |htc\\-|htca|htcg)",
            regex_compiled = lrex.new('^(1207|3gso|4thp|501i|502i|503i|504i|505i|506i|6310|6590|770s|802s|a wa|acer|acs\\-|airn|alav|asus|attw|au\\-m|aur |aus |abac|acoo|aiko|alco|alca|amoi|anex|anny|anyw|aptu|arch|argo|bmobile|bell|bird|bw\\-n|bw\\-u|beck|benq|bilb|blac|c55/|cdm\\-|chtm|capi|comp|cond|dall|dbte|dc\\-s|dica|ds\\-d|ds12|dait|devi|dmob|doco|dopo|dorado|el(?:38|39|48|49|50|55|58|68)|el[3456]\\d{2}dual|erk0|esl8|ex300|ez40|ez60|ez70|ezos|ezze|elai|emul|eric|ezwa|fake|fly\\-|fly_|g\\-mo|g1 u|g560|gf\\-5|grun|gene|go.w|good|grad|hcit|hd\\-m|hd\\-p|hd\\-t|hei\\-|hp i|hpip|hs\\-c|htc |htc\\-|htca|htcg)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Generic",
            device_replacement = "Generic Feature Phone",
            model_replacement = "Feature Phone",
            regex = "^(htcp|htcs|htct|htc_|haie|hita|huaw|hutc|i\\-20|i\\-go|i\\-ma|i\\-mobile|i230|iac|iac\\-|iac/|ig01|im1k|inno|iris|jata|kddi|kgt|kgt/|kpt |kwc\\-|klon|lexi|lg g|lg\\-a|lg\\-b|lg\\-c|lg\\-d|lg\\-f|lg\\-g|lg\\-k|lg\\-l|lg\\-m|lg\\-o|lg\\-p|lg\\-s|lg\\-t|lg\\-u|lg\\-w|lg/k|lg/l|lg/u|lg50|lg54|lge\\-|lge/|leno|m1\\-w|m3ga|m50/|maui|mc01|mc21|mcca|medi|meri|mio8|mioa|mo01|mo02|mode|modo|mot |mot\\-|mt50|mtp1|mtv |mate|maxo|merc|mits|mobi|motv|mozz|n100|n101|n102|n202|n203|n300|n302|n500|n502|n505|n700|n701|n710|nec\\-|nem\\-|newg|neon)",
            regex_compiled = lrex.new('^(htcp|htcs|htct|htc_|haie|hita|huaw|hutc|i\\-20|i\\-go|i\\-ma|i\\-mobile|i230|iac|iac\\-|iac/|ig01|im1k|inno|iris|jata|kddi|kgt|kgt/|kpt |kwc\\-|klon|lexi|lg g|lg\\-a|lg\\-b|lg\\-c|lg\\-d|lg\\-f|lg\\-g|lg\\-k|lg\\-l|lg\\-m|lg\\-o|lg\\-p|lg\\-s|lg\\-t|lg\\-u|lg\\-w|lg/k|lg/l|lg/u|lg50|lg54|lge\\-|lge/|leno|m1\\-w|m3ga|m50/|maui|mc01|mc21|mcca|medi|meri|mio8|mioa|mo01|mo02|mode|modo|mot |mot\\-|mt50|mtp1|mtv |mate|maxo|merc|mits|mobi|motv|mozz|n100|n101|n102|n202|n203|n300|n302|n500|n502|n505|n700|n701|n710|nec\\-|nem\\-|newg|neon)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Generic",
            device_replacement = "Generic Feature Phone",
            model_replacement = "Feature Phone",
            regex = "^(netf|noki|nzph|o2 x|o2\\-x|opwv|owg1|opti|oran|ot\\-s|p800|pand|pg\\-1|pg\\-2|pg\\-3|pg\\-6|pg\\-8|pg\\-c|pg13|phil|pn\\-2|pt\\-g|palm|pana|pire|pock|pose|psio|qa\\-a|qc\\-2|qc\\-3|qc\\-5|qc\\-7|qc07|qc12|qc21|qc32|qc60|qci\\-|qwap|qtek|r380|r600|raks|rim9|rove|s55/|sage|sams|sc01|sch\\-|scp\\-|sdk/|se47|sec\\-|sec0|sec1|semc|sgh\\-|shar|sie\\-|sk\\-0|sl45|slid|smb3|smt5|sp01|sph\\-|spv |spv\\-|sy01|samm|sany|sava|scoo|send|siem|smar|smit|soft|sony|t\\-mo|t218|t250|t600|t610|t618|tcl\\-|tdg\\-|telm|tim\\-|ts70|tsm\\-|tsm3|tsm5|tx\\-9|tagt)",
            regex_compiled = lrex.new('^(netf|noki|nzph|o2 x|o2\\-x|opwv|owg1|opti|oran|ot\\-s|p800|pand|pg\\-1|pg\\-2|pg\\-3|pg\\-6|pg\\-8|pg\\-c|pg13|phil|pn\\-2|pt\\-g|palm|pana|pire|pock|pose|psio|qa\\-a|qc\\-2|qc\\-3|qc\\-5|qc\\-7|qc07|qc12|qc21|qc32|qc60|qci\\-|qwap|qtek|r380|r600|raks|rim9|rove|s55/|sage|sams|sc01|sch\\-|scp\\-|sdk/|se47|sec\\-|sec0|sec1|semc|sgh\\-|shar|sie\\-|sk\\-0|sl45|slid|smb3|smt5|sp01|sph\\-|spv |spv\\-|sy01|samm|sany|sava|scoo|send|siem|smar|smit|soft|sony|t\\-mo|t218|t250|t600|t610|t618|tcl\\-|tdg\\-|telm|tim\\-|ts70|tsm\\-|tsm3|tsm5|tx\\-9|tagt)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Generic",
            device_replacement = "Generic Feature Phone",
            model_replacement = "Feature Phone",
            regex = "^(talk|teli|topl|tosh|up.b|upg1|utst|v400|v750|veri|vk\\-v|vk40|vk50|vk52|vk53|vm40|vx98|virg|vertu|vite|voda|vulc|w3c |w3c\\-|wapj|wapp|wapu|wapm|wig |wapi|wapr|wapv|wapy|wapa|waps|wapt|winc|winw|wonu|x700|xda2|xdag|yas\\-|your|zte\\-|zeto|aste|audi|avan|blaz|brew|brvw|bumb|ccwa|cell|cldc|cmd\\-|dang|eml2|fetc|hipt|http|ibro|idea|ikom|ipaq|jbro|jemu|jigs|keji|kyoc|kyok|libw|m\\-cr|midp|mmef|moto|mwbp|mywa|newt|nok6|o2im|pant|pdxg|play|pluc|port|prox|rozo|sama|seri|smal|symb|treo|upsi|vx52|vx53|vx60|vx61|vx70|vx80|vx81|vx83|vx85|wap\\-|webc|whit|wmlb|xda\\-|xda_)",
            regex_compiled = lrex.new('^(talk|teli|topl|tosh|up.b|upg1|utst|v400|v750|veri|vk\\-v|vk40|vk50|vk52|vk53|vm40|vx98|virg|vertu|vite|voda|vulc|w3c |w3c\\-|wapj|wapp|wapu|wapm|wig |wapi|wapr|wapv|wapy|wapa|waps|wapt|winc|winw|wonu|x700|xda2|xdag|yas\\-|your|zte\\-|zeto|aste|audi|avan|blaz|brew|brvw|bumb|ccwa|cell|cldc|cmd\\-|dang|eml2|fetc|hipt|http|ibro|idea|ikom|ipaq|jbro|jemu|jigs|keji|kyoc|kyok|libw|m\\-cr|midp|mmef|moto|mwbp|mywa|newt|nok6|o2im|pant|pdxg|play|pluc|port|prox|rozo|sama|seri|smal|symb|treo|upsi|vx52|vx53|vx60|vx61|vx70|vx80|vx81|vx83|vx85|wap\\-|webc|whit|wmlb|xda\\-|xda_)', 'i'),
            regex_flag = "i"
        }, {
            brand_replacement = "Generic",
            device_replacement = "Generic Feature Phone",
            model_replacement = "Feature Phone",
            regex = "^(Ice)$",
            regex_compiled = lrex.new('^(Ice)$', 'cf')
        }, {
            brand_replacement = "Generic",
            device_replacement = "Generic Feature Phone",
            model_replacement = "Feature Phone",
            regex = "(wap[\\-\\ ]browser|maui|netfront|obigo|teleca|up\\.browser|midp|Opera Mini)",
            regex_compiled = lrex.new('(wap[\\-\\ ]browser|maui|netfront|obigo|teleca|up\\.browser|midp|Opera Mini)', 'i'),
            regex_flag = "i"
        }
    },
    os_parsers = {
        {
            os_v1_replacement = "2013",
            regex = "HbbTV/\\d+\\.\\d+\\.\\d+ \\( ;(LG)E ;NetCast 4.0",
            regex_compiled = lrex.new('HbbTV/\\d+\\.\\d+\\.\\d+ \\( ;(LG)E ;NetCast 4.0', 'cf')
        }, {
            os_v1_replacement = "2012",
            regex = "HbbTV/\\d+\\.\\d+\\.\\d+ \\( ;(LG)E ;NetCast 3.0",
            regex_compiled = lrex.new('HbbTV/\\d+\\.\\d+\\.\\d+ \\( ;(LG)E ;NetCast 3.0', 'cf')
        }, {
            os_replacement = "Samsung",
            os_v1_replacement = "2011",
            regex = "HbbTV/1.1.1 \\(;;;;;\\) Maple_2011",
            regex_compiled = lrex.new('HbbTV/1.1.1 \\(;;;;;\\) Maple_2011', 'cf')
        }, {
            os_v2_replacement = "UE40F7000",
            regex = "HbbTV/\\d+\\.\\d+\\.\\d+ \\(;(Samsung);SmartTV([0-9]{4});.*FXPDEUC",
            regex_compiled = lrex.new('HbbTV/\\d+\\.\\d+\\.\\d+ \\(;(Samsung);SmartTV([0-9]{4});.*FXPDEUC', 'cf')
        }, {
            os_v2_replacement = "UE32F4500",
            regex = "HbbTV/\\d+\\.\\d+\\.\\d+ \\(;(Samsung);SmartTV([0-9]{4});.*MST12DEUC",
            regex_compiled = lrex.new('HbbTV/\\d+\\.\\d+\\.\\d+ \\(;(Samsung);SmartTV([0-9]{4});.*MST12DEUC', 'cf')
        }, {
            os_v1_replacement = "2013",
            regex = "HbbTV/1.1.1 \\(; (Philips);.*NETTV/4",
            regex_compiled = lrex.new('HbbTV/1.1.1 \\(; (Philips);.*NETTV/4', 'cf')
        }, {
            os_v1_replacement = "2012",
            regex = "HbbTV/1.1.1 \\(; (Philips);.*NETTV/3",
            regex_compiled = lrex.new('HbbTV/1.1.1 \\(; (Philips);.*NETTV/3', 'cf')
        }, {
            os_v1_replacement = "2011",
            regex = "HbbTV/1.1.1 \\(; (Philips);.*NETTV/2",
            regex_compiled = lrex.new('HbbTV/1.1.1 \\(; (Philips);.*NETTV/2', 'cf')
        }, {
            os_replacement = "FireHbbTV",
            regex = "HbbTV/\\d+\\.\\d+\\.\\d+.*(firetv)-firefox-plugin (\\d+).(\\d+).(\\d+)",
            regex_compiled = lrex.new('HbbTV/\\d+\\.\\d+\\.\\d+.*(firetv)-firefox-plugin (\\d+).(\\d+).(\\d+)', 'cf')
        }, {
            regex = "HbbTV/\\d+\\.\\d+\\.\\d+ \\(.*; ?([a-zA-Z]+) ?;.*(201[1-9]).*\\)",
            regex_compiled = lrex.new('HbbTV/\\d+\\.\\d+\\.\\d+ \\(.*; ?([a-zA-Z]+) ?;.*(201[1-9]).*\\)', 'cf')
        }, {
            regex = "(Windows Phone) (?:OS[ /])?(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Windows Phone) (?:OS[ /])?(\\d+)\\.(\\d+)', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "(CPU[ +]OS|iPhone[ +]OS|CPU[ +]iPhone)[ +]+(\\d+)[_\\.](\\d+)(?:[_\\.](\\d+))?.*Outlook-iOS-Android",
            regex_compiled = lrex.new('(CPU[ +]OS|iPhone[ +]OS|CPU[ +]iPhone)[ +]+(\\d+)[_\\.](\\d+)(?:[_\\.](\\d+))?.*Outlook-iOS-Android', 'cf')
        }, {
            regex = "(Android)[ \\-/](\\d+)\\.(\\d+)(?:[.\\-]([a-z0-9]+))?",
            regex_compiled = lrex.new('(Android)[ \\-/](\\d+)\\.(\\d+)(?:[.\\-]([a-z0-9]+))?', 'cf')
        }, {
            os_v1_replacement = "1",
            os_v2_replacement = "2",
            regex = "(Android) Donut",
            regex_compiled = lrex.new('(Android) Donut', 'cf')
        }, {
            os_v1_replacement = "2",
            os_v2_replacement = "1",
            regex = "(Android) Eclair",
            regex_compiled = lrex.new('(Android) Eclair', 'cf')
        }, {
            os_v1_replacement = "2",
            os_v2_replacement = "2",
            regex = "(Android) Froyo",
            regex_compiled = lrex.new('(Android) Froyo', 'cf')
        }, {
            os_v1_replacement = "2",
            os_v2_replacement = "3",
            regex = "(Android) Gingerbread",
            regex_compiled = lrex.new('(Android) Gingerbread', 'cf')
        }, {
            os_v1_replacement = "3",
            regex = "(Android) Honeycomb",
            regex_compiled = lrex.new('(Android) Honeycomb', 'cf')
        }, {
            os_replacement = "Android",
            regex = "^UCWEB.*; (Adr) (\\d+)\\.(\\d+)(?:[.\\-]([a-z0-9]+))?;",
            regex_compiled = lrex.new('^UCWEB.*; (Adr) (\\d+)\\.(\\d+)(?:[.\\-]([a-z0-9]+))?;', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "^UCWEB.*; (iPad|iPh|iPd) OS (\\d+)_(\\d+)(?:_(\\d+))?;",
            regex_compiled = lrex.new('^UCWEB.*; (iPad|iPh|iPd) OS (\\d+)_(\\d+)(?:_(\\d+))?;', 'cf')
        }, {
            os_replacement = "Windows Phone",
            regex = "^UCWEB.*; (wds) (\\d+)\\.(\\d+)(?:\\.(\\d+))?;",
            regex_compiled = lrex.new('^UCWEB.*; (wds) (\\d+)\\.(\\d+)(?:\\.(\\d+))?;', 'cf')
        }, {
            os_replacement = "Android",
            regex = "^(JUC).*; ?U; ?(?:Android)?(\\d+)\\.(\\d+)(?:[\\.\\-]([a-z0-9]+))?",
            regex_compiled = lrex.new('^(JUC).*; ?U; ?(?:Android)?(\\d+)\\.(\\d+)(?:[\\.\\-]([a-z0-9]+))?', 'cf')
        }, {
            os_replacement = "Android",
            regex = "(android)\\s(?:mobile\\/)(\\d+)\\.(\\d+)\\.?(\\d+)?",
            regex_compiled = lrex.new('(android)\\s(?:mobile\\/)(\\d+)\\.(\\d+)\\.?(\\d+)?', 'cf')
        }, {
            os_replacement = "Android",
            regex = "(Silk-Accelerated=[a-z]{4,5})",
            regex_compiled = lrex.new('(Silk-Accelerated=[a-z]{4,5})', 'cf')
        }, {
            os_replacement = "Windows Phone",
            regex = "(XBLWP7)",
            regex_compiled = lrex.new('(XBLWP7)', 'cf')
        }, {
            os_replacement = "Windows Mobile",
            regex = "(Windows ?Mobile)",
            regex_compiled = lrex.new('(Windows ?Mobile)', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "XP",
            regex = "(Windows (?:NT 5\\.2|NT 5\\.1))",
            regex_compiled = lrex.new('(Windows (?:NT 5\\.2|NT 5\\.1))', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "7",
            regex = "(Windows NT 6\\.1)",
            regex_compiled = lrex.new('(Windows NT 6\\.1)', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "Vista",
            regex = "(Windows NT 6\\.0)",
            regex_compiled = lrex.new('(Windows NT 6\\.0)', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "ME",
            regex = "(Win 9x 4\\.90)",
            regex_compiled = lrex.new('(Win 9x 4\\.90)', 'cf')
        }, {
            regex = "(Windows 98|Windows XP|Windows ME|Windows 95|Windows CE|Windows 7|Windows NT 4\\.0|Windows Vista|Windows 2000|Windows 3.1)",
            regex_compiled = lrex.new('(Windows 98|Windows XP|Windows ME|Windows 95|Windows CE|Windows 7|Windows NT 4\\.0|Windows Vista|Windows 2000|Windows 3.1)', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "RT",
            regex = "(Windows NT 6\\.2; ARM;)",
            regex_compiled = lrex.new('(Windows NT 6\\.2; ARM;)', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "8",
            regex = "(Windows NT 6\\.2)",
            regex_compiled = lrex.new('(Windows NT 6\\.2)', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "RT 8.1",
            regex = "(Windows NT 6\\.3; ARM;)",
            regex_compiled = lrex.new('(Windows NT 6\\.3; ARM;)', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "8.1",
            regex = "(Windows NT 6\\.3)",
            regex_compiled = lrex.new('(Windows NT 6\\.3)', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "10",
            regex = "(Windows NT 6\\.4)",
            regex_compiled = lrex.new('(Windows NT 6\\.4)', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "10",
            regex = "(Windows NT 10\\.0)",
            regex_compiled = lrex.new('(Windows NT 10\\.0)', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "2000",
            regex = "(Windows NT 5\\.0)",
            regex_compiled = lrex.new('(Windows NT 5\\.0)', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "NT 4.0",
            regex = "(WinNT4.0)",
            regex_compiled = lrex.new('(WinNT4.0)', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "CE",
            regex = "(Windows ?CE)",
            regex_compiled = lrex.new('(Windows ?CE)', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "$1",
            regex = "Win ?(95|98|3.1|NT|ME|2000)",
            regex_compiled = lrex.new('Win ?(95|98|3.1|NT|ME|2000)', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "3.1",
            regex = "Win16",
            regex_compiled = lrex.new('Win16', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "95",
            regex = "Win32",
            regex_compiled = lrex.new('Win32', 'cf')
        }, {
            os_replacement = "Windows",
            os_v1_replacement = "$1",
            regex = "^Box.*Windows/([\\d.]+);",
            regex_compiled = lrex.new('^Box.*Windows/([\\d.]+);', 'cf')
        }, {
            regex = "(Tizen)[/ ](\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Tizen)[/ ](\\d+)\\.(\\d+)', 'cf')
        }, {
            os_replacement = "Mac OS X",
            regex = "((?:Mac[ +]?|; )OS[ +]X)[\\s+/](?:(\\d+)[_.](\\d+)(?:[_.](\\d+))?|Mach-O)",
            regex_compiled = lrex.new('((?:Mac[ +]?|; )OS[ +]X)[\\s+/](?:(\\d+)[_.](\\d+)(?:[_.](\\d+))?|Mach-O)', 'cf')
        }, {
            os_replacement = "Mac OS X",
            os_v1_replacement = "10",
            os_v2_replacement = "5",
            regex = " (Dar)(win)/(9).(\\d+).*\\((?:i386|x86_64|Power Macintosh)\\)",
            regex_compiled = lrex.new(' (Dar)(win)/(9).(\\d+).*\\((?:i386|x86_64|Power Macintosh)\\)', 'cf')
        }, {
            os_replacement = "Mac OS X",
            os_v1_replacement = "10",
            os_v2_replacement = "6",
            regex = " (Dar)(win)/(10).(\\d+).*\\((?:i386|x86_64)\\)",
            regex_compiled = lrex.new(' (Dar)(win)/(10).(\\d+).*\\((?:i386|x86_64)\\)', 'cf')
        }, {
            os_replacement = "Mac OS X",
            os_v1_replacement = "10",
            os_v2_replacement = "7",
            regex = " (Dar)(win)/(11).(\\d+).*\\((?:i386|x86_64)\\)",
            regex_compiled = lrex.new(' (Dar)(win)/(11).(\\d+).*\\((?:i386|x86_64)\\)', 'cf')
        }, {
            os_replacement = "Mac OS X",
            os_v1_replacement = "10",
            os_v2_replacement = "8",
            regex = " (Dar)(win)/(12).(\\d+).*\\((?:i386|x86_64)\\)",
            regex_compiled = lrex.new(' (Dar)(win)/(12).(\\d+).*\\((?:i386|x86_64)\\)', 'cf')
        }, {
            os_replacement = "Mac OS X",
            os_v1_replacement = "10",
            os_v2_replacement = "9",
            regex = " (Dar)(win)/(13).(\\d+).*\\((?:i386|x86_64)\\)",
            regex_compiled = lrex.new(' (Dar)(win)/(13).(\\d+).*\\((?:i386|x86_64)\\)', 'cf')
        }, {
            os_replacement = "Mac OS",
            regex = "Mac_PowerPC",
            regex_compiled = lrex.new('Mac_PowerPC', 'cf')
        }, {
            regex = "(?:PPC|Intel) (Mac OS X)",
            regex_compiled = lrex.new('(?:PPC|Intel) (Mac OS X)', 'cf')
        }, {
            os_replacement = "Mac OS X",
            regex = "^Box.*;(Darwin)/(10)\\.(1\\d)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('^Box.*;(Darwin)/(10)\\.(1\\d)(?:\\.(\\d+))?', 'cf')
        }, {
            os_replacement = "ATV OS X",
            regex = "(Apple\\s?TV)(?:/(\\d+)\\.(\\d+))?",
            regex_compiled = lrex.new('(Apple\\s?TV)(?:/(\\d+)\\.(\\d+))?', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "(CPU[ +]OS|iPhone[ +]OS|CPU[ +]iPhone|CPU IPhone OS)[ +]+(\\d+)[_\\.](\\d+)(?:[_\\.](\\d+))?",
            regex_compiled = lrex.new('(CPU[ +]OS|iPhone[ +]OS|CPU[ +]iPhone|CPU IPhone OS)[ +]+(\\d+)[_\\.](\\d+)(?:[_\\.](\\d+))?', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "(iPhone|iPad|iPod); Opera",
            regex_compiled = lrex.new('(iPhone|iPad|iPod); Opera', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "(iPhone|iPad|iPod).*Mac OS X.*Version/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(iPhone|iPad|iPod).*Mac OS X.*Version/(\\d+)\\.(\\d+)', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "(CFNetwork)/(5)48\\.0\\.3.* Darwin/11\\.0\\.0",
            regex_compiled = lrex.new('(CFNetwork)/(5)48\\.0\\.3.* Darwin/11\\.0\\.0', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "(CFNetwork)/(5)48\\.(0)\\.4.* Darwin/(1)1\\.0\\.0",
            regex_compiled = lrex.new('(CFNetwork)/(5)48\\.(0)\\.4.* Darwin/(1)1\\.0\\.0', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "(CFNetwork)/(5)48\\.(1)\\.4",
            regex_compiled = lrex.new('(CFNetwork)/(5)48\\.(1)\\.4', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "(CFNetwork)/(4)85\\.1(3)\\.9",
            regex_compiled = lrex.new('(CFNetwork)/(4)85\\.1(3)\\.9', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "(CFNetwork)/(6)09\\.(1)\\.4",
            regex_compiled = lrex.new('(CFNetwork)/(6)09\\.(1)\\.4', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "(CFNetwork)/(6)(0)9",
            regex_compiled = lrex.new('(CFNetwork)/(6)(0)9', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "(CFNetwork)/6(7)2\\.(1)\\.13",
            regex_compiled = lrex.new('(CFNetwork)/6(7)2\\.(1)\\.13', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "(CFNetwork)/6(7)2\\.(1)\\.(1)4",
            regex_compiled = lrex.new('(CFNetwork)/6(7)2\\.(1)\\.(1)4', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "7",
            os_v2_replacement = "1",
            regex = "(CF)(Network)/6(7)(2)\\.1\\.15",
            regex_compiled = lrex.new('(CF)(Network)/6(7)(2)\\.1\\.15', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "(CFNetwork)/6(7)2\\.(0)\\.(?:2|8)",
            regex_compiled = lrex.new('(CFNetwork)/6(7)2\\.(0)\\.(?:2|8)', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "8",
            os_v2_replacement = "0.b5",
            regex = "(CFNetwork)/709\\.1",
            regex_compiled = lrex.new('(CFNetwork)/709\\.1', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "8",
            regex = "(CF)(Network)/711\\.(\\d)",
            regex_compiled = lrex.new('(CF)(Network)/711\\.(\\d)', 'cf')
        }, {
            os_replacement = "Mac OS X",
            os_v1_replacement = "10",
            os_v2_replacement = "10",
            regex = "(CF)(Network)/(720)\\.(\\d)",
            regex_compiled = lrex.new('(CF)(Network)/(720)\\.(\\d)', 'cf')
        }, {
            os_replacement = "Mac OS X",
            os_v1_replacement = "10",
            os_v2_replacement = "11",
            regex = "(CF)(Network)/(760)\\.(\\d)",
            regex_compiled = lrex.new('(CF)(Network)/(760)\\.(\\d)', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "9",
            regex = "(CF)(Network)/758\\.(\\d)",
            regex_compiled = lrex.new('(CF)(Network)/758\\.(\\d)', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "10",
            regex = "(CF)(Network)/808\\.(\\d)",
            regex_compiled = lrex.new('(CF)(Network)/808\\.(\\d)', 'cf')
        }, {
            os_replacement = "Mac OS X",
            os_v1_replacement = "10",
            os_v2_replacement = "13",
            regex = "CFNetwork/.* Darwin/17\\.\\d+.*\\(x86_64\\)",
            regex_compiled = lrex.new('CFNetwork/.* Darwin/17\\.\\d+.*\\(x86_64\\)', 'cf')
        }, {
            os_replacement = "Mac OS X",
            os_v1_replacement = "10",
            os_v2_replacement = "12",
            regex = "CFNetwork/.* Darwin/16\\.\\d+.*\\(x86_64\\)",
            regex_compiled = lrex.new('CFNetwork/.* Darwin/16\\.\\d+.*\\(x86_64\\)', 'cf')
        }, {
            os_replacement = "Mac OS X",
            os_v1_replacement = "10",
            os_v2_replacement = "11",
            regex = "CFNetwork/8.* Darwin/15\\.\\d+.*\\(x86_64\\)",
            regex_compiled = lrex.new('CFNetwork/8.* Darwin/15\\.\\d+.*\\(x86_64\\)', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "1",
            regex = "CFNetwork/.* Darwin/(9)\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/.* Darwin/(9)\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "4",
            regex = "CFNetwork/.* Darwin/(10)\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/.* Darwin/(10)\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "5",
            regex = "CFNetwork/.* Darwin/(11)\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/.* Darwin/(11)\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "6",
            regex = "CFNetwork/.* Darwin/(13)\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/.* Darwin/(13)\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "7",
            regex = "CFNetwork/6.* Darwin/(14)\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/6.* Darwin/(14)\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "8",
            os_v2_replacement = "0",
            regex = "CFNetwork/7.* Darwin/(14)\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/7.* Darwin/(14)\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "9",
            os_v2_replacement = "0",
            regex = "CFNetwork/7.* Darwin/(15)\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/7.* Darwin/(15)\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "10",
            os_v2_replacement = "3",
            regex = "CFNetwork/8.* Darwin/16\\.5\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/8.* Darwin/16\\.5\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "10",
            os_v2_replacement = "3",
            os_v3_replacement = "2",
            regex = "CFNetwork/8.* Darwin/16\\.6\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/8.* Darwin/16\\.6\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "10",
            os_v2_replacement = "3",
            os_v3_replacement = "3",
            regex = "CFNetwork/8.* Darwin/16\\.7\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/8.* Darwin/16\\.7\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "10",
            regex = "CFNetwork/8.* Darwin/(16)\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/8.* Darwin/(16)\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "11",
            os_v2_replacement = "0",
            regex = "CFNetwork/8.* Darwin/17\\.0\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/8.* Darwin/17\\.0\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "11",
            os_v2_replacement = "1",
            regex = "CFNetwork/8.* Darwin/17\\.2\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/8.* Darwin/17\\.2\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "11",
            os_v2_replacement = "2",
            regex = "CFNetwork/8.* Darwin/17\\.3\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/8.* Darwin/17\\.3\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            os_v1_replacement = "11",
            regex = "CFNetwork/8.* Darwin/(17)\\.\\d+",
            regex_compiled = lrex.new('CFNetwork/8.* Darwin/(17)\\.\\d+', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "CFNetwork/.* Darwin/",
            regex_compiled = lrex.new('CFNetwork/.* Darwin/', 'cf')
        }, {
            os_replacement = "iOS",
            regex = "\\b(iOS[ /]|iOS; |iPhone(?:/| v|[ _]OS[/,]|; | OS : |\\d,\\d/|\\d,\\d; )|iPad/)(\\d{1,2})[_\\.](\\d{1,2})(?:[_\\.](\\d+))?",
            regex_compiled = lrex.new('\\b(iOS[ /]|iOS; |iPhone(?:/| v|[ _]OS[/,]|; | OS : |\\d,\\d/|\\d,\\d; )|iPad/)(\\d{1,2})[_\\.](\\d{1,2})(?:[_\\.](\\d+))?', 'cf')
        }, {
            regex = "\\((iOS);",
            regex_compiled = lrex.new('\\((iOS);', 'cf')
        }, {
            regex = "Outlook-(iOS)/\\d+\\.\\d+\\.prod\\.iphone",
            regex_compiled = lrex.new('Outlook-(iOS)/\\d+\\.\\d+\\.prod\\.iphone', 'cf')
        }, {
            os_replacement = "tvOS",
            regex = "(tvOS)/(\\d+).(\\d+)",
            regex_compiled = lrex.new('(tvOS)/(\\d+).(\\d+)', 'cf')
        }, {
            os_replacement = "Chrome OS",
            regex = "(CrOS) [a-z0-9_]+ (\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(CrOS) [a-z0-9_]+ (\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            os_replacement = "Debian",
            regex = "([Dd]ebian)",
            regex_compiled = lrex.new('([Dd]ebian)', 'cf')
        }, {
            regex = "(Linux Mint)(?:/(\\d+))?",
            regex_compiled = lrex.new('(Linux Mint)(?:/(\\d+))?', 'cf')
        }, {
            regex = "(Mandriva)(?: Linux)?/(?:[\\d.-]+m[a-z]{2}(\\d+).(\\d))?",
            regex_compiled = lrex.new('(Mandriva)(?: Linux)?/(?:[\\d.-]+m[a-z]{2}(\\d+).(\\d))?', 'cf')
        }, {
            os_replacement = "Symbian OS",
            regex = "(Symbian[Oo][Ss])[/ ](\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Symbian[Oo][Ss])[/ ](\\d+)\\.(\\d+)', 'cf')
        }, {
            os_replacement = "Symbian^3 Anna",
            regex = "(Symbian/3).+NokiaBrowser/7\\.3",
            regex_compiled = lrex.new('(Symbian/3).+NokiaBrowser/7\\.3', 'cf')
        }, {
            os_replacement = "Symbian^3 Belle",
            regex = "(Symbian/3).+NokiaBrowser/7\\.4",
            regex_compiled = lrex.new('(Symbian/3).+NokiaBrowser/7\\.4', 'cf')
        }, {
            os_replacement = "Symbian^3",
            regex = "(Symbian/3)",
            regex_compiled = lrex.new('(Symbian/3)', 'cf')
        }, {
            os_replacement = "Symbian OS",
            regex = "\\b(Series 60|SymbOS|S60Version|S60V\\d|S60\\b)",
            regex_compiled = lrex.new('\\b(Series 60|SymbOS|S60Version|S60V\\d|S60\\b)', 'cf')
        }, {
            regex = "(MeeGo)",
            regex_compiled = lrex.new('(MeeGo)', 'cf')
        }, {
            os_replacement = "Symbian OS",
            regex = "Symbian [Oo][Ss]",
            regex_compiled = lrex.new('Symbian [Oo][Ss]', 'cf')
        }, {
            os_replacement = "Nokia Series 40",
            regex = "Series40;",
            regex_compiled = lrex.new('Series40;', 'cf')
        }, {
            os_replacement = "Nokia Series 30 Plus",
            regex = "Series30Plus;",
            regex_compiled = lrex.new('Series30Plus;', 'cf')
        }, {
            os_replacement = "BlackBerry OS",
            regex = "(BB10);.+Version/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(BB10);.+Version/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            os_replacement = "BlackBerry OS",
            regex = "(Black[Bb]erry)[0-9a-z]+/(\\d+)\\.(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(Black[Bb]erry)[0-9a-z]+/(\\d+)\\.(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            os_replacement = "BlackBerry OS",
            regex = "(Black[Bb]erry).+Version/(\\d+)\\.(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(Black[Bb]erry).+Version/(\\d+)\\.(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            os_replacement = "BlackBerry Tablet OS",
            regex = "(RIM Tablet OS) (\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(RIM Tablet OS) (\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            os_replacement = "BlackBerry Tablet OS",
            regex = "(Play[Bb]ook)",
            regex_compiled = lrex.new('(Play[Bb]ook)', 'cf')
        }, {
            os_replacement = "BlackBerry OS",
            regex = "(Black[Bb]erry)",
            regex_compiled = lrex.new('(Black[Bb]erry)', 'cf')
        }, {
            os_replacement = "Firefox OS",
            os_v1_replacement = "1",
            os_v2_replacement = "0",
            os_v3_replacement = "1",
            regex = "\\((?:Mobile|Tablet);.+Gecko/18.0 Firefox/\\d+\\.\\d+",
            regex_compiled = lrex.new('\\((?:Mobile|Tablet);.+Gecko/18.0 Firefox/\\d+\\.\\d+', 'cf')
        }, {
            os_replacement = "Firefox OS",
            os_v1_replacement = "1",
            os_v2_replacement = "1",
            regex = "\\((?:Mobile|Tablet);.+Gecko/18.1 Firefox/\\d+\\.\\d+",
            regex_compiled = lrex.new('\\((?:Mobile|Tablet);.+Gecko/18.1 Firefox/\\d+\\.\\d+', 'cf')
        }, {
            os_replacement = "Firefox OS",
            os_v1_replacement = "1",
            os_v2_replacement = "2",
            regex = "\\((?:Mobile|Tablet);.+Gecko/26.0 Firefox/\\d+\\.\\d+",
            regex_compiled = lrex.new('\\((?:Mobile|Tablet);.+Gecko/26.0 Firefox/\\d+\\.\\d+', 'cf')
        }, {
            os_replacement = "Firefox OS",
            os_v1_replacement = "1",
            os_v2_replacement = "3",
            regex = "\\((?:Mobile|Tablet);.+Gecko/28.0 Firefox/\\d+\\.\\d+",
            regex_compiled = lrex.new('\\((?:Mobile|Tablet);.+Gecko/28.0 Firefox/\\d+\\.\\d+', 'cf')
        }, {
            os_replacement = "Firefox OS",
            os_v1_replacement = "1",
            os_v2_replacement = "4",
            regex = "\\((?:Mobile|Tablet);.+Gecko/30.0 Firefox/\\d+\\.\\d+",
            regex_compiled = lrex.new('\\((?:Mobile|Tablet);.+Gecko/30.0 Firefox/\\d+\\.\\d+', 'cf')
        }, {
            os_replacement = "Firefox OS",
            os_v1_replacement = "2",
            os_v2_replacement = "0",
            regex = "\\((?:Mobile|Tablet);.+Gecko/32.0 Firefox/\\d+\\.\\d+",
            regex_compiled = lrex.new('\\((?:Mobile|Tablet);.+Gecko/32.0 Firefox/\\d+\\.\\d+', 'cf')
        }, {
            os_replacement = "Firefox OS",
            os_v1_replacement = "2",
            os_v2_replacement = "1",
            regex = "\\((?:Mobile|Tablet);.+Gecko/34.0 Firefox/\\d+\\.\\d+",
            regex_compiled = lrex.new('\\((?:Mobile|Tablet);.+Gecko/34.0 Firefox/\\d+\\.\\d+', 'cf')
        }, {
            os_replacement = "Firefox OS",
            regex = "\\((?:Mobile|Tablet);.+Firefox/\\d+\\.\\d+",
            regex_compiled = lrex.new('\\((?:Mobile|Tablet);.+Firefox/\\d+\\.\\d+', 'cf')
        }, {
            regex = "(BREW)[ /](\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(BREW)[ /](\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(BREW);",
            regex_compiled = lrex.new('(BREW);', 'cf')
        }, {
            os_replacement = "Brew MP",
            regex = "(Brew MP|BMP)[ /](\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Brew MP|BMP)[ /](\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            os_replacement = "Brew MP",
            regex = "BMP;",
            regex_compiled = lrex.new('BMP;', 'cf')
        }, {
            regex = "(GoogleTV)(?: (\\d+)\\.(\\d+)(?:\\.(\\d+))?|/[\\da-z]+)",
            regex_compiled = lrex.new('(GoogleTV)(?: (\\d+)\\.(\\d+)(?:\\.(\\d+))?|/[\\da-z]+)', 'cf')
        }, {
            regex = "(WebTV)/(\\d+).(\\d+)",
            regex_compiled = lrex.new('(WebTV)/(\\d+).(\\d+)', 'cf')
        }, {
            os_replacement = "Chromecast",
            regex = "(CrKey)(?:[/](\\d+)\\.(\\d+)(?:\\.(\\d+))?)?",
            regex_compiled = lrex.new('(CrKey)(?:[/](\\d+)\\.(\\d+)(?:\\.(\\d+))?)?', 'cf')
        }, {
            os_replacement = "webOS",
            regex = "(hpw|web)OS/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(hpw|web)OS/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            regex = "(VRE);",
            regex_compiled = lrex.new('(VRE);', 'cf')
        }, {
            regex = "(Fedora|Red Hat|PCLinuxOS|Puppy|Ubuntu|Kindle|Bada|Lubuntu|BackTrack|Slackware|(?:Free|Open|Net|\\b)BSD)[/ ](\\d+)\\.(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?",
            regex_compiled = lrex.new('(Fedora|Red Hat|PCLinuxOS|Puppy|Ubuntu|Kindle|Bada|Lubuntu|BackTrack|Slackware|(?:Free|Open|Net|\\b)BSD)[/ ](\\d+)\\.(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?', 'cf')
        }, {
            os_replacement = "Gentoo",
            regex = "(Linux)[ /](\\d+)\\.(\\d+)(?:\\.(\\d+))?.*gentoo",
            regex_compiled = lrex.new('(Linux)[ /](\\d+)\\.(\\d+)(?:\\.(\\d+))?.*gentoo', 'cf')
        }, {
            regex = "\\((Bada);",
            regex_compiled = lrex.new('\\((Bada);', 'cf')
        }, {
            regex = "(Windows|Android|WeTab|Maemo|Web0S)",
            regex_compiled = lrex.new('(Windows|Android|WeTab|Maemo|Web0S)', 'cf')
        }, {
            regex = "(Ubuntu|Kubuntu|Arch Linux|CentOS|Slackware|Gentoo|openSUSE|SUSE|Red Hat|Fedora|PCLinuxOS|Mageia|(?:Free|Open|Net|\\b)BSD)",
            regex_compiled = lrex.new('(Ubuntu|Kubuntu|Arch Linux|CentOS|Slackware|Gentoo|openSUSE|SUSE|Red Hat|Fedora|PCLinuxOS|Mageia|(?:Free|Open|Net|\\b)BSD)', 'cf')
        }, {
            regex = "(Linux)(?:[ /](\\d+)\\.(\\d+)(?:\\.(\\d+))?)?",
            regex_compiled = lrex.new('(Linux)(?:[ /](\\d+)\\.(\\d+)(?:\\.(\\d+))?)?', 'cf')
        }, {
            os_replacement = "Solaris",
            regex = "SunOS",
            regex_compiled = lrex.new('SunOS', 'cf')
        }, {
            os_replacement = "Linux",
            regex = "\\(linux-gnu\\)",
            regex_compiled = lrex.new('\\(linux-gnu\\)', 'cf')
        }, {
            os_replacement = "Red Hat",
            regex = "\\(x86_64-redhat-linux-gnu\\)",
            regex_compiled = lrex.new('\\(x86_64-redhat-linux-gnu\\)', 'cf')
        }, {
            os_replacement = "FreeBSD",
            regex = "\\((freebsd)(\\d+)\\.(\\d+)\\)",
            regex_compiled = lrex.new('\\((freebsd)(\\d+)\\.(\\d+)\\)', 'cf')
        }, {
            regex = "^(Roku)/DVP-(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('^(Roku)/DVP-(\\d+)\\.(\\d+)', 'cf')
        }
    },
    user_agent_parsers = {
        {
            regex = "(ESPN)[%20| ]+Radio/(\\d+)\\.(\\d+)\\.(\\d+) CFNetwork",
            regex_compiled = lrex.new('(ESPN)[%20| ]+Radio/(\\d+)\\.(\\d+)\\.(\\d+) CFNetwork', 'cf')
        }, {
            family_replacement = "AntennaPod",
            regex = "(Antenna)/(\\d+) CFNetwork",
            regex_compiled = lrex.new('(Antenna)/(\\d+) CFNetwork', 'cf')
        }, {
            regex = "(TopPodcasts)Pro/(\\d+) CFNetwork",
            regex_compiled = lrex.new('(TopPodcasts)Pro/(\\d+) CFNetwork', 'cf')
        }, {
            regex = "(MusicDownloader)Lite/(\\d+)\\.(\\d+)\\.(\\d+) CFNetwork",
            regex_compiled = lrex.new('(MusicDownloader)Lite/(\\d+)\\.(\\d+)\\.(\\d+) CFNetwork', 'cf')
        }, {
            regex = "^(.*)-iPad/(\\d+)\\.?(\\d+)?.?(\\d+)?.?(\\d+)? CFNetwork",
            regex_compiled = lrex.new('^(.*)-iPad/(\\d+)\\.?(\\d+)?.?(\\d+)?.?(\\d+)? CFNetwork', 'cf')
        }, {
            regex = "^(.*)-iPhone/(\\d+)\\.?(\\d+)?.?(\\d+)?.?(\\d+)? CFNetwork",
            regex_compiled = lrex.new('^(.*)-iPhone/(\\d+)\\.?(\\d+)?.?(\\d+)?.?(\\d+)? CFNetwork', 'cf')
        }, {
            regex = "^(.*)/(\\d+)\\.?(\\d+)?.?(\\d+)?.?(\\d+)? CFNetwork",
            regex_compiled = lrex.new('^(.*)/(\\d+)\\.?(\\d+)?.?(\\d+)?.?(\\d+)? CFNetwork', 'cf')
        }, {
            family_replacement = "ESPN",
            regex = "(espn\\.go)",
            regex_compiled = lrex.new('(espn\\.go)', 'cf')
        }, {
            family_replacement = "ESPN",
            regex = "(espnradio\\.com)",
            regex_compiled = lrex.new('(espnradio\\.com)', 'cf')
        }, {
            family_replacement = "ESPN",
            regex = "ESPN APP$",
            regex_compiled = lrex.new('ESPN APP$', 'cf')
        }, {
            family_replacement = "AudioBoom",
            regex = "(audioboom\\.com)",
            regex_compiled = lrex.new('(audioboom\\.com)', 'cf')
        }, {
            regex = " (Rivo) RHYTHM",
            regex_compiled = lrex.new(' (Rivo) RHYTHM', 'cf')
        }, {
            family_replacement = "CFNetwork",
            regex = "(CFNetwork)(?:/(\\d+)\\.(\\d+)\\.?(\\d+)?)?",
            regex_compiled = lrex.new('(CFNetwork)(?:/(\\d+)\\.(\\d+)\\.?(\\d+)?)?', 'cf')
        }, {
            family_replacement = "PingdomBot",
            regex = "(Pingdom.com_bot_version_)(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Pingdom.com_bot_version_)(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "PingdomBot",
            regex = "(PingdomTMS)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(PingdomTMS)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "NewRelicPingerBot",
            regex = "(NewRelicPinger)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(NewRelicPinger)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Tableau",
            regex = "(Tableau)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Tableau)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(Salesforce)(?:.)\\/(\\d+)\\.(\\d?)",
            regex_compiled = lrex.new('(Salesforce)(?:.)\\/(\\d+)\\.(\\d?)', 'cf')
        }, {
            family_replacement = "StatusCakeBot",
            regex = "(\\(StatusCake\\))",
            regex_compiled = lrex.new('(\\(StatusCake\\))', 'cf')
        }, {
            family_replacement = "FacebookBot",
            regex = "(facebookexternalhit)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(facebookexternalhit)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "GooglePlusBot",
            regex = "Google.*/\\+/web/snippet",
            regex_compiled = lrex.new('Google.*/\\+/web/snippet', 'cf')
        }, {
            family_replacement = "GmailImageProxy",
            regex = "via ggpht.com GoogleImageProxy",
            regex_compiled = lrex.new('via ggpht.com GoogleImageProxy', 'cf')
        }, {
            family_replacement = "TwitterBot",
            regex = "(Twitterbot)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Twitterbot)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "/((?:Ant-)?Nutch|[A-z]+[Bb]ot|[A-z]+[Ss]pider|Axtaris|fetchurl|Isara|ShopSalad|Tailsweep)[ \\-](\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?",
            regex_compiled = lrex.new('/((?:Ant-)?Nutch|[A-z]+[Bb]ot|[A-z]+[Ss]pider|Axtaris|fetchurl|Isara|ShopSalad|Tailsweep)[ \\-](\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?', 'cf')
        }, {
            regex = "\\b(008|Altresium|Argus|BaiduMobaider|BoardReader|DNSGroup|DataparkSearch|EDI|Goodzer|Grub|INGRID|Infohelfer|LinkedInBot|LOOQ|Nutch|PathDefender|Peew|PostPost|Steeler|Twitterbot|VSE|WebCrunch|WebZIP|Y!J-BR[A-Z]|YahooSeeker|envolk|sproose|wminer)/(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?",
            regex_compiled = lrex.new('\\b(008|Altresium|Argus|BaiduMobaider|BoardReader|DNSGroup|DataparkSearch|EDI|Goodzer|Grub|INGRID|Infohelfer|LinkedInBot|LOOQ|Nutch|PathDefender|Peew|PostPost|Steeler|Twitterbot|VSE|WebCrunch|WebZIP|Y!J-BR[A-Z]|YahooSeeker|envolk|sproose|wminer)/(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?', 'cf')
        }, {
            family_replacement = "MSIECrawler",
            regex = "(MSIE) (\\d+)\\.(\\d+)([a-z]\\d?)?;.* MSIECrawler",
            regex_compiled = lrex.new('(MSIE) (\\d+)\\.(\\d+)([a-z]\\d?)?;.* MSIECrawler', 'cf')
        }, {
            regex = "(DAVdroid)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(DAVdroid)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            regex = "(Google-HTTP-Java-Client|Apache-HttpClient|Go-http-client|scalaj-http|http%20client|Python-urllib|HttpMonitor|TLSProber|WinHTTP|JNLP|okhttp|aihttp|reqwest)(?:[ /](\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?)?",
            regex_compiled = lrex.new('(Google-HTTP-Java-Client|Apache-HttpClient|Go-http-client|scalaj-http|http%20client|Python-urllib|HttpMonitor|TLSProber|WinHTTP|JNLP|okhttp|aihttp|reqwest)(?:[ /](\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?)?', 'cf')
        }, {
            family_replacement = "Pinterestbot",
            regex = "(Pinterest(?:bot)?)/(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?[;\\s\\(]+\\+https://www.pinterest.com/bot.html",
            regex_compiled = lrex.new('(Pinterest(?:bot)?)/(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?[;\\s\\(]+\\+https://www.pinterest.com/bot.html', 'cf')
        }, {
            regex = "(1470\\.net crawler|50\\.nu|8bo Crawler Bot|Aboundex|Accoona-[A-z]+-Agent|AdsBot-Google(?:-[a-z]+)?|altavista|AppEngine-Google|archive.*?\\.org_bot|archiver|Ask Jeeves|[Bb]ai[Dd]u[Ss]pider(?:-[A-Za-z]+)*|bingbot|BingPreview|blitzbot|BlogBridge|Bloglovin|BoardReader(?: [A-Za-z]+)*|boitho.com-dc|BotSeer|BUbiNG|\\b\\w*favicon\\w*\\b|\\bYeti(?:-[a-z]+)?|Catchpoint(?: bot)?|[Cc]harlotte|Checklinks|clumboot|Comodo HTTP\\(S\\) Crawler|Comodo-Webinspector-Crawler|ConveraCrawler|CRAWL-E|CrawlConvera|Daumoa(?:-feedfetcher)?|Feed Seeker Bot|Feedbin|findlinks|Flamingo_SearchEngine|FollowSite Bot|furlbot|Genieo|gigabot|GomezAgent|gonzo1|(?:[a-zA-Z]+-)?Googlebot(?:-[a-zA-Z]+)?|Google SketchUp|grub-client|gsa-crawler|heritrix|HiddenMarket|holmes|HooWWWer|htdig|ia_archiver|ICC-Crawler|Icarus6j|ichiro(?:/mobile)?|IconSurf|IlTrovatore(?:-Setaccio)?|InfuzApp|Innovazion Crawler|InternetArchive|IP2[a-z]+Bot|jbot\\b|KaloogaBot|Kraken|Kurzor|larbin|LEIA|LesnikBot|Linguee Bot|LinkAider|LinkedInBot|Lite Bot|Llaut|lycos|Mail\\.RU_Bot|masscan|masidani_bot|Mediapartners-Google|Microsoft .*? Bot|mogimogi|mozDex|MJ12bot|msnbot(?:-media *)?|msrbot|Mtps Feed Aggregation System|netresearch|Netvibes|NewsGator[^/]*|^NING|Nutch[^/]*|Nymesis|ObjectsSearch|Orbiter|OOZBOT|PagePeeker|PagesInventory|PaxleFramework|Peeplo Screenshot Bot|PlantyNet_WebRobot|Pompos|Qwantify|Read%20Later|Reaper|RedCarpet|Retreiver|Riddler|Rival IQ|scooter|Scrapy|Scrubby|searchsight|seekbot|semanticdiscovery|SemrushBot|Simpy|SimplePie|SEOstats|SimpleRSS|SiteCon|Slackbot-LinkExpanding|Slack-ImgProxy|Slurp|snappy|Speedy Spider|Squrl Java|Stringer|TheUsefulbot|ThumbShotsBot|Thumbshots\\.ru|Tiny Tiny RSS|TwitterBot|WhatsApp|URL2PNG|Vagabondo|VoilaBot|^vortex|Votay bot|^voyager|WASALive.Bot|Web-sniffer|WebThumb|WeSEE:[A-z]+|WhatWeb|WIRE|WordPress|Wotbox|www\\.almaden\\.ibm\\.com|Xenu(?:.s)? Link Sleuth|Xerka [A-z]+Bot|yacy(?:bot)?|Yahoo[a-z]*Seeker|Yahoo! Slurp|Yandex\\w+|YodaoBot(?:-[A-z]+)?|YottaaMonitor|Yowedo|^Zao|^Zao-Crawler|ZeBot_www\\.ze\\.bz|ZooShot|ZyBorg)(?:[ /]v?(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?)?",
            regex_compiled = lrex.new('(1470\\.net crawler|50\\.nu|8bo Crawler Bot|Aboundex|Accoona-[A-z]+-Agent|AdsBot-Google(?:-[a-z]+)?|altavista|AppEngine-Google|archive.*?\\.org_bot|archiver|Ask Jeeves|[Bb]ai[Dd]u[Ss]pider(?:-[A-Za-z]+)*|bingbot|BingPreview|blitzbot|BlogBridge|Bloglovin|BoardReader(?: [A-Za-z]+)*|boitho.com-dc|BotSeer|BUbiNG|\\b\\w*favicon\\w*\\b|\\bYeti(?:-[a-z]+)?|Catchpoint(?: bot)?|[Cc]harlotte|Checklinks|clumboot|Comodo HTTP\\(S\\) Crawler|Comodo-Webinspector-Crawler|ConveraCrawler|CRAWL-E|CrawlConvera|Daumoa(?:-feedfetcher)?|Feed Seeker Bot|Feedbin|findlinks|Flamingo_SearchEngine|FollowSite Bot|furlbot|Genieo|gigabot|GomezAgent|gonzo1|(?:[a-zA-Z]+-)?Googlebot(?:-[a-zA-Z]+)?|Google SketchUp|grub-client|gsa-crawler|heritrix|HiddenMarket|holmes|HooWWWer|htdig|ia_archiver|ICC-Crawler|Icarus6j|ichiro(?:/mobile)?|IconSurf|IlTrovatore(?:-Setaccio)?|InfuzApp|Innovazion Crawler|InternetArchive|IP2[a-z]+Bot|jbot\\b|KaloogaBot|Kraken|Kurzor|larbin|LEIA|LesnikBot|Linguee Bot|LinkAider|LinkedInBot|Lite Bot|Llaut|lycos|Mail\\.RU_Bot|masscan|masidani_bot|Mediapartners-Google|Microsoft .*? Bot|mogimogi|mozDex|MJ12bot|msnbot(?:-media *)?|msrbot|Mtps Feed Aggregation System|netresearch|Netvibes|NewsGator[^/]*|^NING|Nutch[^/]*|Nymesis|ObjectsSearch|Orbiter|OOZBOT|PagePeeker|PagesInventory|PaxleFramework|Peeplo Screenshot Bot|PlantyNet_WebRobot|Pompos|Qwantify|Read%20Later|Reaper|RedCarpet|Retreiver|Riddler|Rival IQ|scooter|Scrapy|Scrubby|searchsight|seekbot|semanticdiscovery|SemrushBot|Simpy|SimplePie|SEOstats|SimpleRSS|SiteCon|Slackbot-LinkExpanding|Slack-ImgProxy|Slurp|snappy|Speedy Spider|Squrl Java|Stringer|TheUsefulbot|ThumbShotsBot|Thumbshots\\.ru|Tiny Tiny RSS|TwitterBot|WhatsApp|URL2PNG|Vagabondo|VoilaBot|^vortex|Votay bot|^voyager|WASALive.Bot|Web-sniffer|WebThumb|WeSEE:[A-z]+|WhatWeb|WIRE|WordPress|Wotbox|www\\.almaden\\.ibm\\.com|Xenu(?:.s)? Link Sleuth|Xerka [A-z]+Bot|yacy(?:bot)?|Yahoo[a-z]*Seeker|Yahoo! Slurp|Yandex\\w+|YodaoBot(?:-[A-z]+)?|YottaaMonitor|Yowedo|^Zao|^Zao-Crawler|ZeBot_www\\.ze\\.bz|ZooShot|ZyBorg)(?:[ /]v?(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?)?', 'cf')
        }, {
            regex = "\\b(Boto3?|JetS3t|aws-(?:cli|sdk-(?:cpp|go|java|nodejs|ruby2?))|s3fs)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('\\b(Boto3?|JetS3t|aws-(?:cli|sdk-(?:cpp|go|java|nodejs|ruby2?))|s3fs)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            regex = "(?:\\/[A-Za-z0-9\\.]+)? *([A-Za-z0-9 \\-_\\!\\[\\]:]*(?:[Aa]rchiver|[Ii]ndexer|[Ss]craper|[Bb]ot|[Ss]pider|[Cc]rawl[a-z]*))/(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?",
            regex_compiled = lrex.new('(?:\\/[A-Za-z0-9\\.]+)? *([A-Za-z0-9 \\-_\\!\\[\\]:]*(?:[Aa]rchiver|[Ii]ndexer|[Ss]craper|[Bb]ot|[Ss]pider|[Cc]rawl[a-z]*))/(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?', 'cf')
        }, {
            regex = "(?:\\/[A-Za-z0-9\\.]+)? *([A-Za-z0-9 _\\!\\[\\]:]*(?:[Aa]rchiver|[Ii]ndexer|[Ss]craper|[Bb]ot|[Ss]pider|[Cc]rawl[a-z]*)) (\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?",
            regex_compiled = lrex.new('(?:\\/[A-Za-z0-9\\.]+)? *([A-Za-z0-9 _\\!\\[\\]:]*(?:[Aa]rchiver|[Ii]ndexer|[Ss]craper|[Bb]ot|[Ss]pider|[Cc]rawl[a-z]*)) (\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?', 'cf')
        }, {
            regex = "((?:[A-z0-9]+|[A-z\\-]+ ?)?(?: the )?(?:[Ss][Pp][Ii][Dd][Ee][Rr]|[Ss]crape|[A-Za-z0-9-]*(?:[^C][^Uu])[Bb]ot|[Cc][Rr][Aa][Ww][Ll])[A-z0-9]*)(?:(?:[ /]| v)(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?)?",
            regex_compiled = lrex.new('((?:[A-z0-9]+|[A-z\\-]+ ?)?(?: the )?(?:[Ss][Pp][Ii][Dd][Ee][Rr]|[Ss]crape|[A-Za-z0-9-]*(?:[^C][^Uu])[Bb]ot|[Cc][Rr][Aa][Ww][Ll])[A-z0-9]*)(?:(?:[ /]| v)(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?)?', 'cf')
        }, {
            regex = "(HbbTV)/(\\d+)\\.(\\d+)\\.(\\d+) \\(",
            regex_compiled = lrex.new('(HbbTV)/(\\d+)\\.(\\d+)\\.(\\d+) \\(', 'cf')
        }, {
            regex = "(Chimera|SeaMonkey|Camino|Waterfox)/(\\d+)\\.(\\d+)\\.?([ab]?\\d+[a-z]*)?",
            regex_compiled = lrex.new('(Chimera|SeaMonkey|Camino|Waterfox)/(\\d+)\\.(\\d+)\\.?([ab]?\\d+[a-z]*)?', 'cf')
        }, {
            family_replacement = "Facebook",
            regex = "\\[FB.*;(FBAV)/(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?",
            regex_compiled = lrex.new('\\[FB.*;(FBAV)/(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?', 'cf')
        }, {
            regex = "\\[(Pinterest)/[^\\]]+\\]",
            regex_compiled = lrex.new('\\[(Pinterest)/[^\\]]+\\]', 'cf')
        }, {
            regex = "(Pinterest)(?: for Android(?: Tablet)?)?/(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?",
            regex_compiled = lrex.new('(Pinterest)(?: for Android(?: Tablet)?)?/(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?', 'cf')
        }, {
            regex = "Mozilla.*Mobile.*(Instagram).(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('Mozilla.*Mobile.*(Instagram).(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "Mozilla.*Mobile.*(Flipboard).(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('Mozilla.*Mobile.*(Flipboard).(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "Mozilla.*Mobile.*(Flipboard-Briefing).(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('Mozilla.*Mobile.*(Flipboard-Briefing).(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "Mozilla.*Mobile.*(Onefootball)\\/Android.(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('Mozilla.*Mobile.*(Onefootball)\\/Android.(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Basilisk",
            regex = "(Firefox)/(\\d+)\\.(\\d+) Basilisk/(\\d+)",
            regex_compiled = lrex.new('(Firefox)/(\\d+)\\.(\\d+) Basilisk/(\\d+)', 'cf')
        }, {
            family_replacement = "Pale Moon",
            regex = "(PaleMoon)/(\\d+)\\.(\\d+)\\.?(\\d+)?",
            regex_compiled = lrex.new('(PaleMoon)/(\\d+)\\.(\\d+)\\.?(\\d+)?', 'cf')
        }, {
            family_replacement = "Firefox Mobile",
            regex = "(Fennec)/(\\d+)\\.(\\d+)\\.?([ab]?\\d+[a-z]*)",
            regex_compiled = lrex.new('(Fennec)/(\\d+)\\.(\\d+)\\.?([ab]?\\d+[a-z]*)', 'cf')
        }, {
            family_replacement = "Firefox Mobile",
            regex = "(Fennec)/(\\d+)\\.(\\d+)(pre)",
            regex_compiled = lrex.new('(Fennec)/(\\d+)\\.(\\d+)(pre)', 'cf')
        }, {
            family_replacement = "Firefox Mobile",
            regex = "(Fennec)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Fennec)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Firefox Mobile",
            regex = "(?:Mobile|Tablet);.*(Firefox)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(?:Mobile|Tablet);.*(Firefox)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Firefox ($1)",
            regex = "(Namoroka|Shiretoko|Minefield)/(\\d+)\\.(\\d+)\\.(\\d+(?:pre)?)",
            regex_compiled = lrex.new('(Namoroka|Shiretoko|Minefield)/(\\d+)\\.(\\d+)\\.(\\d+(?:pre)?)', 'cf')
        }, {
            family_replacement = "Firefox Alpha",
            regex = "(Firefox)/(\\d+)\\.(\\d+)(a\\d+[a-z]*)",
            regex_compiled = lrex.new('(Firefox)/(\\d+)\\.(\\d+)(a\\d+[a-z]*)', 'cf')
        }, {
            family_replacement = "Firefox Beta",
            regex = "(Firefox)/(\\d+)\\.(\\d+)(b\\d+[a-z]*)",
            regex_compiled = lrex.new('(Firefox)/(\\d+)\\.(\\d+)(b\\d+[a-z]*)', 'cf')
        }, {
            family_replacement = "Firefox Alpha",
            regex = "(Firefox)-(?:\\d+\\.\\d+)?/(\\d+)\\.(\\d+)(a\\d+[a-z]*)",
            regex_compiled = lrex.new('(Firefox)-(?:\\d+\\.\\d+)?/(\\d+)\\.(\\d+)(a\\d+[a-z]*)', 'cf')
        }, {
            family_replacement = "Firefox Beta",
            regex = "(Firefox)-(?:\\d+\\.\\d+)?/(\\d+)\\.(\\d+)(b\\d+[a-z]*)",
            regex_compiled = lrex.new('(Firefox)-(?:\\d+\\.\\d+)?/(\\d+)\\.(\\d+)(b\\d+[a-z]*)', 'cf')
        }, {
            family_replacement = "Firefox ($1)",
            regex = "(Namoroka|Shiretoko|Minefield)/(\\d+)\\.(\\d+)([ab]\\d+[a-z]*)?",
            regex_compiled = lrex.new('(Namoroka|Shiretoko|Minefield)/(\\d+)\\.(\\d+)([ab]\\d+[a-z]*)?', 'cf')
        }, {
            family_replacement = "MicroB",
            regex = "(Firefox).*Tablet browser (\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Firefox).*Tablet browser (\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(MozillaDeveloperPreview)/(\\d+)\\.(\\d+)([ab]\\d+[a-z]*)?",
            regex_compiled = lrex.new('(MozillaDeveloperPreview)/(\\d+)\\.(\\d+)([ab]\\d+[a-z]*)?', 'cf')
        }, {
            family_replacement = "Firefox iOS",
            regex = "(FxiOS)/(\\d+)\\.(\\d+)(\\.(\\d+))?(\\.(\\d+))?",
            regex_compiled = lrex.new('(FxiOS)/(\\d+)\\.(\\d+)(\\.(\\d+))?(\\.(\\d+))?', 'cf')
        }, {
            regex = "(Flock)/(\\d+)\\.(\\d+)(b\\d+?)",
            regex_compiled = lrex.new('(Flock)/(\\d+)\\.(\\d+)(b\\d+?)', 'cf')
        }, {
            regex = "(RockMelt)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(RockMelt)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Netscape",
            regex = "(Navigator)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Navigator)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Netscape",
            regex = "(Navigator)/(\\d+)\\.(\\d+)([ab]\\d+)",
            regex_compiled = lrex.new('(Navigator)/(\\d+)\\.(\\d+)([ab]\\d+)', 'cf')
        }, {
            family_replacement = "Netscape",
            regex = "(Netscape6)/(\\d+)\\.(\\d+)\\.?([ab]?\\d+)?",
            regex_compiled = lrex.new('(Netscape6)/(\\d+)\\.(\\d+)\\.?([ab]?\\d+)?', 'cf')
        }, {
            family_replacement = "My Internet Browser",
            regex = "(MyIBrow)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(MyIBrow)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "UC Browser",
            regex = "(UC? ?Browser|UCWEB|U3)[ /]?(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(UC? ?Browser|UCWEB|U3)[ /]?(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(Opera Tablet).*Version/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(Opera Tablet).*Version/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            regex = "(Opera Mini)(?:/att)?/?(\\d+)?(?:\\.(\\d+))?(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(Opera Mini)(?:/att)?/?(\\d+)?(?:\\.(\\d+))?(?:\\.(\\d+))?', 'cf')
        }, {
            family_replacement = "Opera Mobile",
            regex = "(Opera)/.+Opera Mobi.+Version/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Opera)/.+Opera Mobi.+Version/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Opera Mobile",
            regex = "(Opera)/(\\d+)\\.(\\d+).+Opera Mobi",
            regex_compiled = lrex.new('(Opera)/(\\d+)\\.(\\d+).+Opera Mobi', 'cf')
        }, {
            family_replacement = "Opera Mobile",
            regex = "Opera Mobi.+(Opera)(?:/|\\s+)(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('Opera Mobi.+(Opera)(?:/|\\s+)(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Opera Mobile",
            regex = "Opera Mobi",
            regex_compiled = lrex.new('Opera Mobi', 'cf')
        }, {
            regex = "(Opera)/9.80.*Version/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(Opera)/9.80.*Version/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            family_replacement = "Opera Mobile",
            regex = "(?:Mobile Safari).*(OPR)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(?:Mobile Safari).*(OPR)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Opera",
            regex = "(?:Chrome).*(OPR)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(?:Chrome).*(OPR)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Opera Coast",
            regex = "(Coast)/(\\d+).(\\d+).(\\d+)",
            regex_compiled = lrex.new('(Coast)/(\\d+).(\\d+).(\\d+)', 'cf')
        }, {
            family_replacement = "Opera Mini",
            regex = "(OPiOS)/(\\d+).(\\d+).(\\d+)",
            regex_compiled = lrex.new('(OPiOS)/(\\d+).(\\d+).(\\d+)', 'cf')
        }, {
            family_replacement = "Opera Neon",
            regex = "Chrome/.+( MMS)/(\\d+).(\\d+).(\\d+)",
            regex_compiled = lrex.new('Chrome/.+( MMS)/(\\d+).(\\d+).(\\d+)', 'cf')
        }, {
            family_replacement = "webOS Browser",
            regex = "(hpw|web)OS/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(hpw|web)OS/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            family_replacement = "LuaKit",
            regex = "(luakit)",
            regex_compiled = lrex.new('(luakit)', 'cf')
        }, {
            regex = "(Snowshoe)/(\\d+)\\.(\\d+).(\\d+)",
            regex_compiled = lrex.new('(Snowshoe)/(\\d+)\\.(\\d+).(\\d+)', 'cf')
        }, {
            regex = "Gecko/\\d+ (Lightning)/(\\d+)\\.(\\d+)\\.?((?:[ab]?\\d+[a-z]*)|(?:\\d*))",
            regex_compiled = lrex.new('Gecko/\\d+ (Lightning)/(\\d+)\\.(\\d+)\\.?((?:[ab]?\\d+[a-z]*)|(?:\\d*))', 'cf')
        }, {
            family_replacement = "Swiftfox",
            regex = "(Firefox)/(\\d+)\\.(\\d+)\\.(\\d+(?:pre)?) \\(Swiftfox\\)",
            regex_compiled = lrex.new('(Firefox)/(\\d+)\\.(\\d+)\\.(\\d+(?:pre)?) \\(Swiftfox\\)', 'cf')
        }, {
            family_replacement = "Swiftfox",
            regex = "(Firefox)/(\\d+)\\.(\\d+)([ab]\\d+[a-z]*)? \\(Swiftfox\\)",
            regex_compiled = lrex.new('(Firefox)/(\\d+)\\.(\\d+)([ab]\\d+[a-z]*)? \\(Swiftfox\\)', 'cf')
        }, {
            family_replacement = "Rekonq",
            regex = "(rekonq)/(\\d+)\\.(\\d+)\\.?(\\d+)? Safari",
            regex_compiled = lrex.new('(rekonq)/(\\d+)\\.(\\d+)\\.?(\\d+)? Safari', 'cf')
        }, {
            family_replacement = "Rekonq",
            regex = "rekonq",
            regex_compiled = lrex.new('rekonq', 'cf')
        }, {
            family_replacement = "Conkeror",
            regex = "(conkeror|Conkeror)/(\\d+)\\.(\\d+)\\.?(\\d+)?",
            regex_compiled = lrex.new('(conkeror|Conkeror)/(\\d+)\\.(\\d+)\\.?(\\d+)?', 'cf')
        }, {
            family_replacement = "Konqueror",
            regex = "(konqueror)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(konqueror)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(WeTab)-Browser",
            regex_compiled = lrex.new('(WeTab)-Browser', 'cf')
        }, {
            family_replacement = "Comodo Dragon",
            regex = "(Comodo_Dragon)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Comodo_Dragon)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(Symphony) (\\d+).(\\d+)",
            regex_compiled = lrex.new('(Symphony) (\\d+).(\\d+)', 'cf')
        }, {
            family_replacement = "NetFront NX",
            regex = "PLAYSTATION 3.+WebKit",
            regex_compiled = lrex.new('PLAYSTATION 3.+WebKit', 'cf')
        }, {
            family_replacement = "NetFront",
            regex = "PLAYSTATION 3",
            regex_compiled = lrex.new('PLAYSTATION 3', 'cf')
        }, {
            family_replacement = "NetFront",
            regex = "(PlayStation Portable)",
            regex_compiled = lrex.new('(PlayStation Portable)', 'cf')
        }, {
            family_replacement = "NetFront NX",
            regex = "(PlayStation Vita)",
            regex_compiled = lrex.new('(PlayStation Vita)', 'cf')
        }, {
            family_replacement = "NetFront NX",
            regex = "AppleWebKit.+ (NX)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('AppleWebKit.+ (NX)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "NetFront NX",
            regex = "(Nintendo 3DS)",
            regex_compiled = lrex.new('(Nintendo 3DS)', 'cf')
        }, {
            family_replacement = "Amazon Silk",
            regex = "(Silk)/(\\d+)\\.(\\d+)(?:\\.([0-9\\-]+))?",
            regex_compiled = lrex.new('(Silk)/(\\d+)\\.(\\d+)(?:\\.([0-9\\-]+))?', 'cf')
        }, {
            regex = "(Puffin)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(Puffin)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            family_replacement = "Edge Mobile",
            regex = "Windows Phone .*(Edge)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('Windows Phone .*(Edge)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Samsung Internet",
            regex = "(SamsungBrowser)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(SamsungBrowser)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Seznam prohlížeč",
            regex = "(SznProhlizec)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(SznProhlizec)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            family_replacement = "Coc Coc",
            regex = "(coc_coc_browser)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(coc_coc_browser)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            family_replacement = "Baidu Browser",
            regex = "(baidubrowser)[/\\s](\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?",
            regex_compiled = lrex.new('(baidubrowser)[/\\s](\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?', 'cf')
        }, {
            family_replacement = "Baidu Explorer",
            regex = "(FlyFlow)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(FlyFlow)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Maxthon",
            regex = "(MxBrowser)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(MxBrowser)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            regex = "(Crosswalk)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Crosswalk)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Chrome Mobile WebView",
            regex = "; wv\\).+(Chrome)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('; wv\\).+(Chrome)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Chrome Mobile",
            regex = "(CrMo)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(CrMo)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Chrome Mobile iOS",
            regex = "(CriOS)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(CriOS)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Chrome Mobile",
            regex = "(Chrome)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+) Mobile(?:[ /]|$)",
            regex_compiled = lrex.new('(Chrome)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+) Mobile(?:[ /]|$)', 'cf')
        }, {
            family_replacement = "Chrome Mobile",
            regex = " Mobile .*(Chrome)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new(' Mobile .*(Chrome)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Chrome Frame",
            regex = "(chromeframe)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(chromeframe)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Tizen Browser",
            regex = "(SLP Browser)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(SLP Browser)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Sogou Explorer",
            regex = "(SE 2\\.X) MetaSr (\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(SE 2\\.X) MetaSr (\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "QQ Browser Mini",
            regex = "(MQQBrowser/Mini)(?:(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?)?",
            regex_compiled = lrex.new('(MQQBrowser/Mini)(?:(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?)?', 'cf')
        }, {
            family_replacement = "QQ Browser Mobile",
            regex = "(MQQBrowser)(?:/(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?)?",
            regex_compiled = lrex.new('(MQQBrowser)(?:/(\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?)?', 'cf')
        }, {
            family_replacement = "QQ Browser",
            regex = "(QQBrowser)(?:/(\\d+)(?:\\.(\\d+)\\.(\\d+)(?:\\.(\\d+))?)?)?",
            regex_compiled = lrex.new('(QQBrowser)(?:/(\\d+)(?:\\.(\\d+)\\.(\\d+)(?:\\.(\\d+))?)?)?', 'cf')
        }, {
            family_replacement = "RackspaceBot",
            regex = "(Rackspace Monitoring)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Rackspace Monitoring)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(PyAMF)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(PyAMF)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Yandex Browser",
            regex = "(YaBrowser)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(YaBrowser)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Mail.ru Chromium Browser",
            regex = "(Chrome)/(\\d+)\\.(\\d+)\\.(\\d+).* MRCHROME",
            regex_compiled = lrex.new('(Chrome)/(\\d+)\\.(\\d+)\\.(\\d+).* MRCHROME', 'cf')
        }, {
            regex = "(AOL) (\\d+)\\.(\\d+); AOLBuild (\\d+)",
            regex_compiled = lrex.new('(AOL) (\\d+)\\.(\\d+); AOLBuild (\\d+)', 'cf')
        }, {
            regex = "(PodCruncher|Downcast)[ /]?(\\d+)\\.?(\\d+)?\\.?(\\d+)?\\.?(\\d+)?",
            regex_compiled = lrex.new('(PodCruncher|Downcast)[ /]?(\\d+)\\.?(\\d+)?\\.?(\\d+)?\\.?(\\d+)?', 'cf')
        }, {
            regex = " (BoxNotes)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new(' (BoxNotes)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Slack Desktop Client",
            regex = "(Slack_SSB)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Slack_SSB)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "HipChat Desktop Client",
            regex = "(HipChat)/?(\\d+)?",
            regex_compiled = lrex.new('(HipChat)/?(\\d+)?', 'cf')
        }, {
            regex = "\\b(MobileIron|FireWeb|Jasmine|ANTGalio|Midori|Fresco|Lobo|PaleMoon|Maxthon|Lynx|OmniWeb|Dillo|Camino|Demeter|Fluid|Fennec|Epiphany|Shiira|Sunrise|Spotify|Flock|Netscape|Lunascape|WebPilot|NetFront|Netfront|Konqueror|SeaMonkey|Kazehakase|Vienna|Iceape|Iceweasel|IceWeasel|Iron|K-Meleon|Sleipnir|Galeon|GranParadiso|Opera Mini|iCab|NetNewsWire|ThunderBrowse|Iris|UP\\.Browser|Bunjalloo|Google Earth|Raven for Mac|Openwave|MacOutlook|Electron|OktaMobile)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('\\b(MobileIron|FireWeb|Jasmine|ANTGalio|Midori|Fresco|Lobo|PaleMoon|Maxthon|Lynx|OmniWeb|Dillo|Camino|Demeter|Fluid|Fennec|Epiphany|Shiira|Sunrise|Spotify|Flock|Netscape|Lunascape|WebPilot|NetFront|Netfront|Konqueror|SeaMonkey|Kazehakase|Vienna|Iceape|Iceweasel|IceWeasel|Iron|K-Meleon|Sleipnir|Galeon|GranParadiso|Opera Mini|iCab|NetNewsWire|ThunderBrowse|Iris|UP\\.Browser|Bunjalloo|Google Earth|Raven for Mac|Openwave|MacOutlook|Electron|OktaMobile)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Outlook",
            regex = "Microsoft Office Outlook 12\\.\\d+\\.\\d+|MSOffice 12",
            regex_compiled = lrex.new('Microsoft Office Outlook 12\\.\\d+\\.\\d+|MSOffice 12', 'cf'),
            v1_replacement = "2007"
        }, {
            family_replacement = "Outlook",
            regex = "Microsoft Outlook 14\\.\\d+\\.\\d+|MSOffice 14",
            regex_compiled = lrex.new('Microsoft Outlook 14\\.\\d+\\.\\d+|MSOffice 14', 'cf'),
            v1_replacement = "2010"
        }, {
            family_replacement = "Outlook",
            regex = "Microsoft Outlook 15\\.\\d+\\.\\d+",
            regex_compiled = lrex.new('Microsoft Outlook 15\\.\\d+\\.\\d+', 'cf'),
            v1_replacement = "2013"
        }, {
            family_replacement = "Outlook",
            regex = "Microsoft Outlook (?:Mail )?16\\.\\d+\\.\\d+",
            regex_compiled = lrex.new('Microsoft Outlook (?:Mail )?16\\.\\d+\\.\\d+', 'cf'),
            v1_replacement = "2016"
        }, {
            family_replacement = "Windows Live Mail",
            regex = "Outlook-Express\\/7\\.0.*",
            regex_compiled = lrex.new('Outlook-Express\\/7\\.0.*', 'cf')
        }, {
            regex = "(Airmail) (\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(Airmail) (\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            family_replacement = "Thunderbird",
            regex = "(Thunderbird)/(\\d+)\\.(\\d+)(?:\\.(\\d+(?:pre)?))?",
            regex_compiled = lrex.new('(Thunderbird)/(\\d+)\\.(\\d+)(?:\\.(\\d+(?:pre)?))?', 'cf')
        }, {
            family_replacement = "Postbox",
            regex = "(Postbox)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Postbox)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Barca",
            regex = "(Barca(?:Pro)?)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(Barca(?:Pro)?)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            family_replacement = "Lotus Notes",
            regex = "(Lotus-Notes)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(Lotus-Notes)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            regex = "(Vivaldi)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Vivaldi)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(Edge)/(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(Edge)/(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            family_replacement = "Brave",
            regex = "(brave)/(\\d+)\\.(\\d+)\\.(\\d+) Chrome",
            regex_compiled = lrex.new('(brave)/(\\d+)\\.(\\d+)\\.(\\d+) Chrome', 'cf')
        }, {
            family_replacement = "Iron",
            regex = "(Chrome)/(\\d+)\\.(\\d+)\\.(\\d+)[\\d.]* Iron[^/]",
            regex_compiled = lrex.new('(Chrome)/(\\d+)\\.(\\d+)\\.(\\d+)[\\d.]* Iron[^/]', 'cf')
        }, {
            regex = "\\b(Dolphin)(?: |HDCN/|/INT\\-)(\\d+)\\.(\\d+)\\.?(\\d+)?",
            regex_compiled = lrex.new('\\b(Dolphin)(?: |HDCN/|/INT\\-)(\\d+)\\.(\\d+)\\.?(\\d+)?', 'cf')
        }, {
            regex = "(HeadlessChrome)(?:/(\\d+)\\.(\\d+)\\.(\\d+))?",
            regex_compiled = lrex.new('(HeadlessChrome)(?:/(\\d+)\\.(\\d+)\\.(\\d+))?', 'cf')
        }, {
            regex = "(Evolution)/(\\d+)\\.(\\d+)\\.(\\d+\\.\\d+)",
            regex_compiled = lrex.new('(Evolution)/(\\d+)\\.(\\d+)\\.(\\d+\\.\\d+)', 'cf')
        }, {
            regex = "(RCM CardDAV plugin)/(\\d+)\\.(\\d+)\\.(\\d+(?:-dev)?)",
            regex_compiled = lrex.new('(RCM CardDAV plugin)/(\\d+)\\.(\\d+)\\.(\\d+(?:-dev)?)', 'cf')
        }, {
            regex = "(bingbot|Bolt|AdobeAIR|Jasmine|IceCat|Skyfire|Midori|Maxthon|Lynx|Arora|IBrowse|Dillo|Camino|Shiira|Fennec|Phoenix|Flock|Netscape|Lunascape|Epiphany|WebPilot|Opera Mini|Opera|NetFront|Netfront|Konqueror|Googlebot|SeaMonkey|Kazehakase|Vienna|Iceape|Iceweasel|IceWeasel|Iron|K-Meleon|Sleipnir|Galeon|GranParadiso|iCab|iTunes|MacAppStore|NetNewsWire|Space Bison|Stainless|Orca|Dolfin|BOLT|Minimo|Tizen Browser|Polaris|Abrowser|Planetweb|ICE Browser|mDolphin|qutebrowser|Otter|QupZilla|MailBar|kmail2|YahooMobileMail|ExchangeWebServices|ExchangeServicesClient|Dragon|Outlook-iOS-Android)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(bingbot|Bolt|AdobeAIR|Jasmine|IceCat|Skyfire|Midori|Maxthon|Lynx|Arora|IBrowse|Dillo|Camino|Shiira|Fennec|Phoenix|Flock|Netscape|Lunascape|Epiphany|WebPilot|Opera Mini|Opera|NetFront|Netfront|Konqueror|Googlebot|SeaMonkey|Kazehakase|Vienna|Iceape|Iceweasel|IceWeasel|Iron|K-Meleon|Sleipnir|Galeon|GranParadiso|iCab|iTunes|MacAppStore|NetNewsWire|Space Bison|Stainless|Orca|Dolfin|BOLT|Minimo|Tizen Browser|Polaris|Abrowser|Planetweb|ICE Browser|mDolphin|qutebrowser|Otter|QupZilla|MailBar|kmail2|YahooMobileMail|ExchangeWebServices|ExchangeServicesClient|Dragon|Outlook-iOS-Android)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            regex = "(Chromium|Chrome)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(Chromium|Chrome)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            family_replacement = "IE Mobile",
            regex = "(IEMobile)[ /](\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(IEMobile)[ /](\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(BacaBerita App)\\/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(BacaBerita App)\\/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "^(bPod|Pocket Casts|Player FM)$",
            regex_compiled = lrex.new('^(bPod|Pocket Casts|Player FM)$', 'cf')
        }, {
            regex = "^(AlexaMediaPlayer|VLC)/(\\d+)\\.(\\d+)\\.([^.\\s]+)",
            regex_compiled = lrex.new('^(AlexaMediaPlayer|VLC)/(\\d+)\\.(\\d+)\\.([^.\\s]+)', 'cf')
        }, {
            regex = "^(AntennaPod|WMPlayer|Zune|Podkicker|Radio|ExoPlayerDemo|Overcast|PocketTunes|NSPlayer|okhttp|DoggCatcher|QuickNews|QuickTime|Peapod|Podcasts|GoldenPod|VLC|Spotify|Miro|MediaGo|Juice|iPodder|gPodder|Banshee)/(\\d+)\\.(\\d+)\\.?(\\d+)?\\.?(\\d+)?",
            regex_compiled = lrex.new('^(AntennaPod|WMPlayer|Zune|Podkicker|Radio|ExoPlayerDemo|Overcast|PocketTunes|NSPlayer|okhttp|DoggCatcher|QuickNews|QuickTime|Peapod|Podcasts|GoldenPod|VLC|Spotify|Miro|MediaGo|Juice|iPodder|gPodder|Banshee)/(\\d+)\\.(\\d+)\\.?(\\d+)?\\.?(\\d+)?', 'cf')
        }, {
            regex = "^(Peapod|Liferea)/([^.\\s]+)\\.([^.\\s]+)?\\.?([^.\\s]+)?",
            regex_compiled = lrex.new('^(Peapod|Liferea)/([^.\\s]+)\\.([^.\\s]+)?\\.?([^.\\s]+)?', 'cf')
        }, {
            regex = "^(bPod|Player FM) BMID/(\\S+)",
            regex_compiled = lrex.new('^(bPod|Player FM) BMID/(\\S+)', 'cf')
        }, {
            regex = "^(Podcast ?Addict)/v(\\d+) ",
            regex_compiled = lrex.new('^(Podcast ?Addict)/v(\\d+) ', 'cf')
        }, {
            family_replacement = "PodcastAddict",
            regex = "^(Podcast ?Addict) ",
            regex_compiled = lrex.new('^(Podcast ?Addict) ', 'cf')
        }, {
            regex = "(Replay) AV",
            regex_compiled = lrex.new('(Replay) AV', 'cf')
        }, {
            regex = "(VOX) Music Player",
            regex_compiled = lrex.new('(VOX) Music Player', 'cf')
        }, {
            regex = "(CITA) RSS Aggregator/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(CITA) RSS Aggregator/(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(Pocket Casts)$",
            regex_compiled = lrex.new('(Pocket Casts)$', 'cf')
        }, {
            regex = "(Player FM)$",
            regex_compiled = lrex.new('(Player FM)$', 'cf')
        }, {
            regex = "(LG Player|Doppler|FancyMusic|MediaMonkey|Clementine) (\\d+)\\.(\\d+)\\.?([^.\\s]+)?\\.?([^.\\s]+)?",
            regex_compiled = lrex.new('(LG Player|Doppler|FancyMusic|MediaMonkey|Clementine) (\\d+)\\.(\\d+)\\.?([^.\\s]+)?\\.?([^.\\s]+)?', 'cf')
        }, {
            regex = "(philpodder)/(\\d+)\\.(\\d+)\\.?([^.\\s]+)?\\.?([^.\\s]+)?",
            regex_compiled = lrex.new('(philpodder)/(\\d+)\\.(\\d+)\\.?([^.\\s]+)?\\.?([^.\\s]+)?', 'cf')
        }, {
            regex = "(Player FM|Pocket Casts|DoggCatcher|Spotify|MediaMonkey|MediaGo|BashPodder)",
            regex_compiled = lrex.new('(Player FM|Pocket Casts|DoggCatcher|Spotify|MediaMonkey|MediaGo|BashPodder)', 'cf')
        }, {
            regex = "(QuickTime)\\.(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(QuickTime)\\.(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(Kinoma)(\\d+)",
            regex_compiled = lrex.new('(Kinoma)(\\d+)', 'cf')
        }, {
            family_replacement = "FancyMusic",
            regex = "(Fancy) Cloud Music (\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Fancy) Cloud Music (\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "ESPN",
            regex = "EspnDownloadManager",
            regex_compiled = lrex.new('EspnDownloadManager', 'cf')
        }, {
            regex = "(ESPN) Radio (\\d+)\\.(\\d+)\\.?(\\d+)? ?(?:rv:(\\d+))? ",
            regex_compiled = lrex.new('(ESPN) Radio (\\d+)\\.(\\d+)\\.?(\\d+)? ?(?:rv:(\\d+))? ', 'cf')
        }, {
            regex = "(podracer|jPodder) v ?(\\d+)\\.(\\d+)\\.?(\\d+)?",
            regex_compiled = lrex.new('(podracer|jPodder) v ?(\\d+)\\.(\\d+)\\.?(\\d+)?', 'cf')
        }, {
            regex = "(ZDM)/(\\d+)\\.(\\d+)[; ]?",
            regex_compiled = lrex.new('(ZDM)/(\\d+)\\.(\\d+)[; ]?', 'cf')
        }, {
            regex = "(Zune|BeyondPod) (\\d+)\\.?(\\d+)?[\\);]",
            regex_compiled = lrex.new('(Zune|BeyondPod) (\\d+)\\.?(\\d+)?[\\);]', 'cf')
        }, {
            regex = "(WMPlayer)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(WMPlayer)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "WMPlayer",
            regex = "^(Lavf)",
            regex_compiled = lrex.new('^(Lavf)', 'cf')
        }, {
            regex = "^(RSSRadio)[ /]?(\\d+)?",
            regex_compiled = lrex.new('^(RSSRadio)[ /]?(\\d+)?', 'cf')
        }, {
            family_replacement = "RSSRadio",
            regex = "(RSS_Radio) (\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(RSS_Radio) (\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Podkicker",
            regex = "(Podkicker) \\S+/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Podkicker) \\S+/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "^(HTC) Streaming Player \\S+ / \\S+ / \\S+ / (\\d+)\\.(\\d+)\\.?(\\d+)?",
            regex_compiled = lrex.new('^(HTC) Streaming Player \\S+ / \\S+ / \\S+ / (\\d+)\\.(\\d+)\\.?(\\d+)?', 'cf')
        }, {
            regex = "^(Stitcher)/iOS",
            regex_compiled = lrex.new('^(Stitcher)/iOS', 'cf')
        }, {
            regex = "^(Stitcher)/Android",
            regex_compiled = lrex.new('^(Stitcher)/Android', 'cf')
        }, {
            regex = "^(VLC) .*version (\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('^(VLC) .*version (\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = " (VLC) for",
            regex_compiled = lrex.new(' (VLC) for', 'cf')
        }, {
            family_replacement = "VLC",
            regex = "(vlc)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(vlc)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "^(foobar)\\S+/([^.\\s]+)\\.([^.\\s]+)?\\.?([^.\\s]+)?",
            regex_compiled = lrex.new('^(foobar)\\S+/([^.\\s]+)\\.([^.\\s]+)?\\.?([^.\\s]+)?', 'cf')
        }, {
            regex = "^(Clementine)\\S+ ([^.\\s]+)\\.([^.\\s]+)?\\.?([^.\\s]+)?",
            regex_compiled = lrex.new('^(Clementine)\\S+ ([^.\\s]+)\\.([^.\\s]+)?\\.?([^.\\s]+)?', 'cf')
        }, {
            family_replacement = "Amarok",
            regex = "(amarok)/([^.\\s]+)\\.([^.\\s]+)?\\.?([^.\\s]+)?",
            regex_compiled = lrex.new('(amarok)/([^.\\s]+)\\.([^.\\s]+)?\\.?([^.\\s]+)?', 'cf')
        }, {
            regex = "(Custom)-Feed Reader",
            regex_compiled = lrex.new('(Custom)-Feed Reader', 'cf')
        }, {
            regex = "(iRider|Crazy Browser|SkipStone|iCab|Lunascape|Sleipnir|Maemo Browser) (\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(iRider|Crazy Browser|SkipStone|iCab|Lunascape|Sleipnir|Maemo Browser) (\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(iCab|Lunascape|Opera|Android|Jasmine|Polaris|Microsoft SkyDriveSync|The Bat!) (\\d+)\\.(\\d+)\\.?(\\d+)?",
            regex_compiled = lrex.new('(iCab|Lunascape|Opera|Android|Jasmine|Polaris|Microsoft SkyDriveSync|The Bat!) (\\d+)\\.(\\d+)\\.?(\\d+)?', 'cf')
        }, {
            regex = "(Kindle)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Kindle)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(Android) Donut",
            regex_compiled = lrex.new('(Android) Donut', 'cf'),
            v1_replacement = "1",
            v2_replacement = "2"
        }, {
            regex = "(Android) Eclair",
            regex_compiled = lrex.new('(Android) Eclair', 'cf'),
            v1_replacement = "2",
            v2_replacement = "1"
        }, {
            regex = "(Android) Froyo",
            regex_compiled = lrex.new('(Android) Froyo', 'cf'),
            v1_replacement = "2",
            v2_replacement = "2"
        }, {
            regex = "(Android) Gingerbread",
            regex_compiled = lrex.new('(Android) Gingerbread', 'cf'),
            v1_replacement = "2",
            v2_replacement = "3"
        }, {
            regex = "(Android) Honeycomb",
            regex_compiled = lrex.new('(Android) Honeycomb', 'cf'),
            v1_replacement = "3"
        }, {
            family_replacement = "IE Large Screen",
            regex = "(MSIE) (\\d+)\\.(\\d+).*XBLWP7",
            regex_compiled = lrex.new('(MSIE) (\\d+)\\.(\\d+).*XBLWP7', 'cf')
        }, {
            regex = "(Nextcloud)",
            regex_compiled = lrex.new('(Nextcloud)', 'cf')
        }, {
            regex = "(mirall)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(mirall)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Owncloud",
            regex = "(ownCloud-android)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(ownCloud-android)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(Obigo)InternetBrowser",
            regex_compiled = lrex.new('(Obigo)InternetBrowser', 'cf')
        }, {
            regex = "(Obigo)\\-Browser",
            regex_compiled = lrex.new('(Obigo)\\-Browser', 'cf')
        }, {
            family_replacement = "Obigo",
            regex = "(Obigo|OBIGO)[^\\d]*(\\d+)(?:.(\\d+))?",
            regex_compiled = lrex.new('(Obigo|OBIGO)[^\\d]*(\\d+)(?:.(\\d+))?', 'cf')
        }, {
            family_replacement = "Maxthon",
            regex = "(MAXTHON|Maxthon) (\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(MAXTHON|Maxthon) (\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(Maxthon|MyIE2|Uzbl|Shiira)",
            regex_compiled = lrex.new('(Maxthon|MyIE2|Uzbl|Shiira)', 'cf'),
            v1_replacement = "0"
        }, {
            regex = "(BrowseX) \\((\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(BrowseX) \\((\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "NCSA Mosaic",
            regex = "(NCSA_Mosaic)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(NCSA_Mosaic)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Polaris",
            regex = "(POLARIS)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(POLARIS)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Polaris",
            regex = "(Embider)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Embider)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Bon Echo",
            regex = "(BonEcho)/(\\d+)\\.(\\d+)\\.?([ab]?\\d+)?",
            regex_compiled = lrex.new('(BonEcho)/(\\d+)\\.(\\d+)\\.?([ab]?\\d+)?', 'cf')
        }, {
            family_replacement = "Mobile Safari",
            regex = "(iPod|iPhone|iPad).+Version/(\\d+)\\.(\\d+)(?:\\.(\\d+))?.*[ +]Safari",
            regex_compiled = lrex.new('(iPod|iPhone|iPad).+Version/(\\d+)\\.(\\d+)(?:\\.(\\d+))?.*[ +]Safari', 'cf')
        }, {
            family_replacement = "Mobile Safari UI/WKWebView",
            regex = "(iPod|iPod touch|iPhone|iPad);.*CPU.*OS[ +](\\d+)_(\\d+)(?:_(\\d+))?.* AppleNews\\/\\d+\\.\\d+\\.\\d+?",
            regex_compiled = lrex.new('(iPod|iPod touch|iPhone|iPad);.*CPU.*OS[ +](\\d+)_(\\d+)(?:_(\\d+))?.* AppleNews\\/\\d+\\.\\d+\\.\\d+?', 'cf')
        }, {
            family_replacement = "Mobile Safari UI/WKWebView",
            regex = "(iPod|iPhone|iPad).+Version/(\\d+)\\.(\\d+)(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(iPod|iPhone|iPad).+Version/(\\d+)\\.(\\d+)(?:\\.(\\d+))?', 'cf')
        }, {
            family_replacement = "Mobile Safari",
            regex = "(iPod|iPod touch|iPhone|iPad);.*CPU.*OS[ +](\\d+)_(\\d+)(?:_(\\d+))?.*Mobile.*[ +]Safari",
            regex_compiled = lrex.new('(iPod|iPod touch|iPhone|iPad);.*CPU.*OS[ +](\\d+)_(\\d+)(?:_(\\d+))?.*Mobile.*[ +]Safari', 'cf')
        }, {
            family_replacement = "Mobile Safari UI/WKWebView",
            regex = "(iPod|iPod touch|iPhone|iPad);.*CPU.*OS[ +](\\d+)_(\\d+)(?:_(\\d+))?.*Mobile",
            regex_compiled = lrex.new('(iPod|iPod touch|iPhone|iPad);.*CPU.*OS[ +](\\d+)_(\\d+)(?:_(\\d+))?.*Mobile', 'cf')
        }, {
            family_replacement = "Mobile Safari",
            regex = "(iPod|iPhone|iPad).* Safari",
            regex_compiled = lrex.new('(iPod|iPhone|iPad).* Safari', 'cf')
        }, {
            family_replacement = "Mobile Safari UI/WKWebView",
            regex = "(iPod|iPhone|iPad)",
            regex_compiled = lrex.new('(iPod|iPhone|iPad)', 'cf')
        }, {
            regex = "(Outlook-iOS)/\\d+\\.\\d+\\.prod\\.iphone \\((\\d+)\\.(\\d+)\\.(\\d+)\\)",
            regex_compiled = lrex.new('(Outlook-iOS)/\\d+\\.\\d+\\.prod\\.iphone \\((\\d+)\\.(\\d+)\\.(\\d+)\\)', 'cf')
        }, {
            regex = "(AvantGo) (\\d+).(\\d+)",
            regex_compiled = lrex.new('(AvantGo) (\\d+).(\\d+)', 'cf')
        }, {
            family_replacement = "ONE Browser",
            regex = "(OneBrowser)/(\\d+).(\\d+)",
            regex_compiled = lrex.new('(OneBrowser)/(\\d+).(\\d+)', 'cf')
        }, {
            regex = "(Avant)",
            regex_compiled = lrex.new('(Avant)', 'cf'),
            v1_replacement = "1"
        }, {
            regex = "(QtCarBrowser)",
            regex_compiled = lrex.new('(QtCarBrowser)', 'cf'),
            v1_replacement = "1"
        }, {
            family_replacement = "iBrowser Mini",
            regex = "^(iBrowser/Mini)(\\d+).(\\d+)",
            regex_compiled = lrex.new('^(iBrowser/Mini)(\\d+).(\\d+)', 'cf')
        }, {
            regex = "^(iBrowser|iRAPP)/(\\d+).(\\d+)",
            regex_compiled = lrex.new('^(iBrowser|iRAPP)/(\\d+).(\\d+)', 'cf')
        }, {
            family_replacement = "Nokia Services (WAP) Browser",
            regex = "^(Nokia)",
            regex_compiled = lrex.new('^(Nokia)', 'cf')
        }, {
            family_replacement = "Nokia Browser",
            regex = "(NokiaBrowser)/(\\d+)\\.(\\d+).(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(NokiaBrowser)/(\\d+)\\.(\\d+).(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Nokia Browser",
            regex = "(NokiaBrowser)/(\\d+)\\.(\\d+).(\\d+)",
            regex_compiled = lrex.new('(NokiaBrowser)/(\\d+)\\.(\\d+).(\\d+)', 'cf')
        }, {
            family_replacement = "Nokia Browser",
            regex = "(NokiaBrowser)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(NokiaBrowser)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Nokia Browser",
            regex = "(BrowserNG)/(\\d+)\\.(\\d+).(\\d+)",
            regex_compiled = lrex.new('(BrowserNG)/(\\d+)\\.(\\d+).(\\d+)', 'cf')
        }, {
            family_replacement = "Nokia Browser",
            regex = "(Series60)/5\\.0",
            regex_compiled = lrex.new('(Series60)/5\\.0', 'cf'),
            v1_replacement = "7",
            v2_replacement = "0"
        }, {
            family_replacement = "Nokia OSS Browser",
            regex = "(Series60)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Series60)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Ovi Browser",
            regex = "(S40OviBrowser)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(S40OviBrowser)/(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(Nokia)[EN]?(\\d+)",
            regex_compiled = lrex.new('(Nokia)[EN]?(\\d+)', 'cf')
        }, {
            family_replacement = "BlackBerry WebKit",
            regex = "(PlayBook).+RIM Tablet OS (\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(PlayBook).+RIM Tablet OS (\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "BlackBerry WebKit",
            regex = "(Black[bB]erry|BB10).+Version/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Black[bB]erry|BB10).+Version/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "BlackBerry",
            regex = "(Black[bB]erry)\\s?(\\d+)",
            regex_compiled = lrex.new('(Black[bB]erry)\\s?(\\d+)', 'cf')
        }, {
            regex = "(OmniWeb)/v(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(OmniWeb)/v(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Palm Blazer",
            regex = "(Blazer)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Blazer)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Palm Pre",
            regex = "(Pre)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Pre)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(ELinks)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(ELinks)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(ELinks) \\((\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(ELinks) \\((\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(Links) \\((\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Links) \\((\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(QtWeb) Internet Browser/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(QtWeb) Internet Browser/(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(PhantomJS)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(PhantomJS)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "WebKit Nightly",
            regex = "(AppleWebKit)/(\\d+)\\.?(\\d+)?\\+ .* Safari",
            regex_compiled = lrex.new('(AppleWebKit)/(\\d+)\\.?(\\d+)?\\+ .* Safari', 'cf')
        }, {
            family_replacement = "Safari",
            regex = "(Version)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?.*Safari/",
            regex_compiled = lrex.new('(Version)/(\\d+)\\.(\\d+)(?:\\.(\\d+))?.*Safari/', 'cf')
        }, {
            regex = "(Safari)/\\d+",
            regex_compiled = lrex.new('(Safari)/\\d+', 'cf')
        }, {
            regex = "(OLPC)/Update(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(OLPC)/Update(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(OLPC)/Update()\\.(\\d+)",
            regex_compiled = lrex.new('(OLPC)/Update()\\.(\\d+)', 'cf'),
            v1_replacement = "0"
        }, {
            regex = "(SEMC\\-Browser)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(SEMC\\-Browser)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Teleca Browser",
            regex = "(Teleca)",
            regex_compiled = lrex.new('(Teleca)', 'cf')
        }, {
            family_replacement = "Phantom Browser",
            regex = "(Phantom)/V(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Phantom)/V(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "IE",
            regex = "(Trident)/(7|8)\\.(0)",
            regex_compiled = lrex.new('(Trident)/(7|8)\\.(0)', 'cf'),
            v1_replacement = "11"
        }, {
            family_replacement = "IE",
            regex = "(Trident)/(6)\\.(0)",
            regex_compiled = lrex.new('(Trident)/(6)\\.(0)', 'cf'),
            v1_replacement = "10"
        }, {
            family_replacement = "IE",
            regex = "(Trident)/(5)\\.(0)",
            regex_compiled = lrex.new('(Trident)/(5)\\.(0)', 'cf'),
            v1_replacement = "9"
        }, {
            family_replacement = "IE",
            regex = "(Trident)/(4)\\.(0)",
            regex_compiled = lrex.new('(Trident)/(4)\\.(0)', 'cf'),
            v1_replacement = "8"
        }, {
            regex = "(Espial)/(\\d+)(?:\\.(\\d+))?(?:\\.(\\d+))?",
            regex_compiled = lrex.new('(Espial)/(\\d+)(?:\\.(\\d+))?(?:\\.(\\d+))?', 'cf')
        }, {
            family_replacement = "Apple Mail",
            regex = "(AppleWebKit)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(AppleWebKit)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(Firefox)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Firefox)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "(Firefox)/(\\d+)\\.(\\d+)(pre|[ab]\\d+[a-z]*)?",
            regex_compiled = lrex.new('(Firefox)/(\\d+)\\.(\\d+)(pre|[ab]\\d+[a-z]*)?', 'cf')
        }, {
            family_replacement = "IE",
            regex = "([MS]?IE) (\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('([MS]?IE) (\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Python Requests",
            regex = "(python-requests)/(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(python-requests)/(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "\\b(Windows-Update-Agent|Microsoft-CryptoAPI|SophosUpdateManager|SophosAgent|Debian APT-HTTP|Ubuntu APT-HTTP|libcurl-agent|libwww-perl|urlgrabber|curl|PycURL|Wget|aria2|Axel|OpenBSD ftp|lftp|jupdate)(?:[ /](\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?)?",
            regex_compiled = lrex.new('\\b(Windows-Update-Agent|Microsoft-CryptoAPI|SophosUpdateManager|SophosAgent|Debian APT-HTTP|Ubuntu APT-HTTP|libcurl-agent|libwww-perl|urlgrabber|curl|PycURL|Wget|aria2|Axel|OpenBSD ftp|lftp|jupdate)(?:[ /](\\d+)(?:\\.(\\d+)(?:\\.(\\d+))?)?)?', 'cf')
        }, {
            regex = "(Java)[/ ]{0,1}\\d+\\.(\\d+)\\.(\\d+)[_-]*([a-zA-Z0-9]+)*",
            regex_compiled = lrex.new('(Java)[/ ]{0,1}\\d+\\.(\\d+)\\.(\\d+)[_-]*([a-zA-Z0-9]+)*', 'cf')
        }, {
            regex = "^(Cyberduck)/(\\d+)\\.(\\d+)\\.(\\d+)(?:\\.\\d+)?",
            regex_compiled = lrex.new('^(Cyberduck)/(\\d+)\\.(\\d+)\\.(\\d+)(?:\\.\\d+)?', 'cf')
        }, {
            regex = "^(S3 Browser) (\\d+)-(\\d+)-(\\d+)(?:\\s*http://s3browser\\.com)?",
            regex_compiled = lrex.new('^(S3 Browser) (\\d+)-(\\d+)-(\\d+)(?:\\s*http://s3browser\\.com)?', 'cf')
        }, {
            regex = "^(rclone)/v(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('^(rclone)/v(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "^(Roku)/DVP-(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('^(Roku)/DVP-(\\d+)\\.(\\d+)', 'cf')
        }, {
            family_replacement = "Kurio App",
            regex = "(Kurio)\\/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('(Kurio)\\/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }, {
            regex = "^(Box(?: Sync)?)/(\\d+)\\.(\\d+)\\.(\\d+)",
            regex_compiled = lrex.new('^(Box(?: Sync)?)/(\\d+)\\.(\\d+)\\.(\\d+)', 'cf')
        }
    }
}