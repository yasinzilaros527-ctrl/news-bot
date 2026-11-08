import os, json, time, html
import feedparser, requests

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL_ID"]
PER_FEED = 4
SEEN_FILE = "seen.json"

FEEDS = {
    "🇮🇷 فارسی": "https://feeds.bbci.co.uk/persian/rss.xml",
    "🇬🇧 English": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "🇸🇦 العربية": "https://feeds.bbci.co.uk/arabic/rss.xml",
    "🇪🇸 Español": "https://feeds.bbci.co.uk/mundo/rss.xml",
    "🇫🇷 Français": "https://www.france24.com/fr/rss",
    "🇩🇪 Deutsch": "https://rss.dw.com/rdf/rss-de-all",
    "🇷🇺 Русский": "https://feeds.bbci.co.uk/russian/rss.xml",
    "🇹🇷 Türkçe": "https://feeds.bbci.co.uk/turkce/rss.xml",
    "🇧🇷 Português": "https://feeds.bbci.co.uk/portuguese/rss.xml",
    "🇮🇳 हिन्दी": "https://feeds.bbci.co.uk/hindi/rss.xml",
    "🇨🇳 中文": "https://feeds.bbci.co.uk/zhongwen/simp/rss.xml",
    "🇯🇵 日本語": "https://feeds.bbci.co.uk/japanese/rss.xml",
}

try:
    seen = set(json.load(open(SEEN_FILE)))
except Exception:
    seen = set()

def send(text):
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHANNEL, "text": text, "parse_mode": "HTML",
              "disable_web_page_preview": "false"},
        timeout=30,
    )
    print(r.status_code, r.text[:100])

for lang, url in FEEDS.items():
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print("خطا:", lang, e)
        continue
    sent = 0
    for e in feed.entries:
        link = e.get("link")
        if not link or link in seen:
            continue
        title = html.escape(e.get("title", ""))
        send(f"{lang}\n\n<b>{title}</b>\n\n{link}")
        seen.add(link)
        sent += 1
        time.sleep(3)
        if sent >= PER_FEED:
            break

json.dump(list(seen)[-3000:], open(SEEN_FILE, "w"))
