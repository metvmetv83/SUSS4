"""
youtube_cache.py — YouTube kanal manifest URL'lerini önbelleğe alır
Worker /cache endpoint'ini çağırır → youtube_cache.json olarak kaydeder
GitHub Actions ile her 45 dakikada çalıştırılır (manifest URL'ler ~1 saat geçerli)
"""

import requests
import json
import sys

CACHE_URL   = "https://youtubem2.metvmetv07.workers.dev/cache"
OUTPUT_FILE = "youtube_cache.json"

def main():
    print(f"[*] Cache yenileniyor: {CACHE_URL}")
    try:
        r = requests.get(CACHE_URL, timeout=120)
        if r.status_code != 200:
            print(f"[!] Hata: HTTP {r.status_code}")
            sys.exit(1)

        data = r.json()
        print(f"[+] {len(data)} kanal URL'si alındı")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"[*] Kaydedildi: {OUTPUT_FILE}")
        for name, url in data.items():
            print(f"  {name}: {url[:70]}...")

    except Exception as e:
        print(f"[!] Hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
