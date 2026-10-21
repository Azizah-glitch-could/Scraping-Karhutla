"""
Scraping tweet bertopik KARHUTLA (kebakaran hutan dan lahan) memakai Apify.
Actor: khadinakbar/x-tweet-scraper

Cara pakai:
1. Simpan token di config.py  ->  APIFY_TOKEN = "token_baru_kamu"
   (atau set environment variable APIFY_TOKEN). config.py WAJIB ada di .gitignore.
2. pip install apify-client pandas
3. python apify_scraper.py
   Script bisa dijalankan berkali-kali: data baru digabung ke CSV lama
   dan duplikat dibuang otomatis, jadi data tidak hilang.
"""
import os
import re
import time

import pandas as pd
from apify_client import ApifyClient

try:
    from config import APIFY_TOKEN
except ImportError:
    APIFY_TOKEN = os.getenv("APIFY_TOKEN", "")

if not APIFY_TOKEN:
    raise SystemExit("APIFY_TOKEN belum diisi. Isi di config.py atau environment variable.")

client = ApifyClient(APIFY_TOKEN)

ACTOR_ID = "khadinakbar/x-tweet-scraper"
OUTPUT_FILE = "data_karhutla.csv"
TARGET = 1000

# Satu kata kunci = satu run (actor ini hanya menerima 1 string di 'searchQuery')
QUERIES = [
    "karhutla",
    "kebakaran hutan",
    "kebakaran lahan",
    "kabut asap karhutla",
    "titik panas karhutla",
    "karhutla Riau",
    "karhutla Kalimantan",
    "karhutla Sumatera",
]
MAX_PER_QUERY = 300

# Filter relevansi: tweet harus mengandung salah satu kata ini
RELEVAN = re.compile(
    r"karhutla|kebakaran (hutan|lahan)|kabut asap|titik panas|hotspot|"
    r"pembakaran lahan|asap",
    re.IGNORECASE,
)


def jumlah_relevan(df: pd.DataFrame) -> int:
    return int(df["full_text"].fillna("").str.contains(RELEVAN).sum())


def scrape_satu_query(q: str):
    run_input = {
        "searchQuery": q,              # <- nama field yang benar
        "sort": "Latest",
        "lang": "id",                  # hanya tweet berbahasa Indonesia
        "maxTweetsPerQuery": MAX_PER_QUERY,
        "excludeRetweets": True,
        "includeSourceQuery": True,
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    return client.dataset(run["defaultDatasetId"]).list_items().items


def main():
    # Muat data lama (kalau ada) supaya hasil run sebelumnya tidak hilang
    if os.path.exists(OUTPUT_FILE):
        df_all = pd.read_csv(OUTPUT_FILE)
        print(f"Data lama dimuat: {len(df_all)} baris")
    else:
        df_all = pd.DataFrame()

    for q in QUERIES:
        if not df_all.empty and jumlah_relevan(df_all) >= TARGET:
            print("Target tercapai, berhenti.")
            break

        print(f"\n[+] Scraping: '{q}' ...")
        try:
            items = scrape_satu_query(q)
        except Exception as e:
            print(f"    [!] Error pada '{q}': {e}")
            continue

        print(f"    -> {len(items)} tweet diterima")
        if items:
            df_all = pd.concat([df_all, pd.DataFrame(items)], ignore_index=True)
            if "tweet_id" in df_all.columns:
                df_all = df_all.drop_duplicates(subset="tweet_id")
            # simpan setiap selesai satu query, jaga-jaga kalau kredit habis di tengah jalan
            df_all.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
        time.sleep(2)

    if df_all.empty:
        print("Tidak ada data yang berhasil diambil.")
        return

    # Filter relevansi topik
    df_final = df_all[df_all["full_text"].fillna("").str.contains(RELEVAN)]
    df_final.to_csv("data_karhutla_final.csv", index=False, encoding="utf-8-sig")

    print("\n" + "=" * 50)
    print(f"Total mentah           : {len(df_all)} baris")
    print(f"Total relevan (final)  : {len(df_final)} baris -> data_karhutla_final.csv")
    print("=" * 50)
    if len(df_final) >= TARGET:
        print("Syarat >= 1000 baris terpenuhi. Siap commit & push ke GitHub.")
    else:
        print(f"Masih kurang {TARGET - len(df_final)} baris. Jalankan lagi atau tambah QUERIES.")


if __name__ == "__main__":
    main()