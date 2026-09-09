#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional

CONFIG_FILE = "config.json"
OUTPUT_FOLDER = "playlist"
OUTPUT_PLAYLIST = "playerlist.m3u"

CHROME_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
             "AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/148.0.0.0 Safari/537.36")

def load_config() -> Dict:
    path = Path(CONFIG_FILE)
    if not path.exists():
        raise ValueError(f"{CONFIG_FILE} bulunamadı.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_youtube_stream_url(youtube_url: str, quality: str) -> Optional[str]:
    common = [
        "yt-dlp",
        "--no-playlist",
        "--no-warnings",
        "--user-agent", CHROME_UA,
        "--referer", "https://www.youtube.com/",
        "--geo-bypass",
        "--socket-timeout", "30",
    ]

    attempts = [
        ("mweb_client", [*common, "-g", "--extractor-args", "youtube:player_client=mweb", "-f", quality, youtube_url]),
        ("android_client", [*common, "-g", "--extractor-args", "youtube:player_client=android", "-f", quality, youtube_url]),
        ("tv_embedded", [*common, "-g", "--extractor-args", "youtube:player_client=tv_embedded", "-f", quality, youtube_url]),
        ("deno/default", [*common, "-g", "--js-runtimes", "deno", "--remote-components", "ejs:github", "--extractor-args", "youtube:player_client=default", "-f", quality, youtube_url])
    ]

    for label, cmd in attempts:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
            if result.returncode == 0:
                lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
                for line in lines:
                    if line.startswith("http"):
                        return line
        except Exception:
            continue
            
    return None

def main() -> int:
    print("🎬 YouTube M3U Oynatma Listesi Oluşturucu Başlatıldı\n" + "-" * 50)
    
    try:
        config = load_config()
    except Exception as e:
        print(f"❌ Config yüklenemedi: {e}")
        return 1

    quality = config.get("quality", "best")
    channels = config.get("channels", [])

    if not channels:
        print("❌ config.json içinde işlenecek kanal bulunamadı.")
        return 1

    output_path = Path(OUTPUT_FOLDER)
    output_path.mkdir(parents=True, exist_ok=True)

    m3u_lines = ["#EXTM3U"]
    success_count = 0

    for index, channel in enumerate(channels, start=1):
        name = channel.get("name", f"Kanal {index}")
        url = channel.get("url")

        if not url:
            print(f"⚠️ [{index}/{len(channels)}] {name}: URL bulunamadı, atlanıyor.")
            continue

        print(f"🔄 [{index}/{len(channels)}] taranıyor: {name}")
        stream_url = get_youtube_stream_url(url, quality)

        if stream_url:
            m3u_lines.append(f"#EXTINF:0,{name}")
            m3u_lines.append(stream_url)
            success_count += 1
            print(f"   ✅ Başarılı: {name}")
        else:
            print(f"   ❌ Yayın bağlantısı alınamadı: {name}")

    playlist_file = output_path / OUTPUT_PLAYLIST
    playlist_file.write_text("\n".join(m3u_lines) + "\n", encoding="utf-8")
    
    (output_path / "playlist.m3u8").write_text("\n".join(m3u_lines) + "\n", encoding="utf-8")

    print("-" * 50)
    print(f"🎉 İşlem tamamlandı! Toplam {success_count}/{len(channels)} kanal eklendi.")
    print(f"📁 Oluşan dosya: {playlist_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
