"""
youtube_cache.py — YouTube manifest URL'lerini zengin JSON olarak kaydeder
Format: { "id": { "name": "...", "group": "...", "logo": "...", "url": "..." } }
"""
import requests, json, sys

CACHE_URL   = "https://youtubem2.metvmetv07.workers.dev/cache"
OUTPUT_FILE = "youtube_cache.json"

def main():
    print(f"[*] Cache yenileniyor: {CACHE_URL}")
    try:
        r = requests.get(CACHE_URL, timeout=180)
        if r.status_code != 200:
            print(f"[!] HTTP {r.status_code}"); sys.exit(1)

        data = r.json()
        found = sum(1 for v in data.values() if v.get("url"))
        print(f"[+] {found}/{len(data)} kanal URL'si alındı")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"[*] Kaydedildi: {OUTPUT_FILE}")
        for k, v in data.items():
            status = "✓" if v.get("url") else "✗"
            print(f"  {status} {v.get('name','?')}: {v.get('url','')[:60]}")

    except Exception as e:
        print(f"[!] Hata: {e}"); sys.exit(1)

if __name__ == "__main__":
    main()
