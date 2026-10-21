"""Ambil data dari run Apify yang sudah selesai (berdasarkan Run ID di log terminal)."""
import pandas as pd
from apify_client import ApifyClient

try:
    from config import APIFY_TOKEN
except ImportError:
    raise SystemExit("APIFY_TOKEN tidak ditemukan di config.py")

RUN_IDS = [
    # batch 1 (17:3x)
    "aOybcgfzUA1I9FY1c",   # karhutla
    "uh9WCc7j3ll7nyK5R",   # kebakaran hutan
    "PRIPiOz42P72Oris1",   # kebakaran lahan
    "ooDSRJEsueyAud0gi",   # kabut asap karhutla
    "gHrEeQC4R5znzxVS5",   # titik panas karhutla
    "BteLelY4JsOR4DjrT",   # karhutla Riau
    "xduX2uq5m8iRznvRw",   # karhutla Kalimantan
    "tNHV2g9sUM3ERRioI",   # karhutla Sumatera
    # batch 2 (17:41)
    "tehyXOlespwJWg3ib",   # karhutla
    "3hQYsebqLW2N56GsP",   # kebakaran hutan
    "3x5MOJaQBJF8ZTHkw",   # kebakaran lahan
    "DDcPjsuJYU93Xkewb",   # kabut asap karhutla
    "AqEojAoXhU4knXJhG",   # titik panas karhutla
    "CfU6Y2kiQkz7FuSSR",   # karhutla Riau
    "80mXMbK6rMbc365GY",   # karhutla Kalimantan
    "sEENqvFRRVhlu4ebK",   # karhutla Sumatera
]

client = ApifyClient(APIFY_TOKEN)
rows = []

for rid in RUN_IDS:
    try:
        run = client.run(rid).get()
        if isinstance(run, dict):
            ds_id = run.get("defaultDatasetId") or run.get("default_dataset_id")
        else:
            ds_id = run.default_dataset_id
        items = client.dataset(ds_id).list_items().items
        print(f"{rid}: {len(items)} tweet")
        rows.extend(items)
    except Exception as e:
        print(f"{rid}: GAGAL -> {e}")

if not rows:
    raise SystemExit("Tidak ada data yang berhasil diambil.")

df = pd.DataFrame(rows)
if "tweet_id" in df.columns:
    df = df.drop_duplicates(subset="tweet_id")

df.to_csv("data_karhutla.csv", index=False, encoding="utf-8-sig")
print(f"\nTersimpan: {len(df)} baris -> data_karhutla.csv")
print("Kolom:", list(df.columns)[:8], "...")