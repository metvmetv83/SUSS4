import re
import requests

SOURCE_URL = "https://raw.githubusercontent.com/metvmetv83/SUSS4/refs/heads/main/playlist.m3u"

BASE_TEMPLATE = """#EXTM3U
#EXTINF:-1 tvg-id="245931" tvg-name="kanal-d",Kanal D
http://87.121.104.29:8001/?id=245931&token=TOKEN

#EXTINF:-1 tvg-id="246195" tvg-name="sinema-tv",Sinema TV
http://87.121.104.29:8001/?id=246195&token=TOKEN
"""

r = requests.get(SOURCE_URL, timeout=20)
text = r.text

match = re.search(r'token=([a-f0-9]+)', text)

if not match:
    raise Exception("Token bulunamadı")

token = match.group(1)

final_playlist = BASE_TEMPLATE.replace("TOKEN", token)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(final_playlist)

print("Yeni token:", token)
