import os
import time
import pickle
import numpy as np
import faiss
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from sentence_transformers import SentenceTransformer
from apscheduler.schedulers.background import BackgroundScheduler
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load .env
load_dotenv()

BASE_URL = "https://docs-path.vercel.app/"

# Globals
visited = set()
text_chunks = []
chunk_sources = []

# Embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dim, fast

def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.netloc == urlparse(BASE_URL).netloc

def scrape_site_playwright(url):
    global visited, text_chunks, chunk_sources

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        queue = [url]

        while queue:
            current_url = queue.pop(0)
            if current_url in visited:
                continue

            try:
                page.goto(current_url, timeout=15000)
                content = page.content()
                soup = BeautifulSoup(content, "html.parser")
                text = soup.get_text(separator="\n", strip=True)

                if text and len(text.strip()) > 100:
                    text_chunks.append(text[:2048])
                    chunk_sources.append(current_url)
                    print(f"[SCRAPED] {current_url}")

                for a in soup.find_all("a", href=True):
                    full_url = urljoin(current_url, a['href'])
                    if is_valid_url(full_url) and full_url not in visited:
                        queue.append(full_url)

                visited.add(current_url)

            except Exception as e:
                print(f"[ERROR] Failed on {current_url}: {e}")

        browser.close()

def generate_embeddings(texts):
    print("[INFO] Generating embeddings...")
    return embedder.encode(texts, show_progress_bar=True)

def save_vector_db(embeddings, sources):
    if len(embeddings) == 0:
        print("[WARNING] No embeddings to save.")
        return

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, "website_index.faiss")

    with open("sources.pkl", "wb") as f:
        pickle.dump(sources, f)

    print(f"[INFO] Saved {len(embeddings)} embeddings to FAISS.")

def daily_job():
    print("\n[INFO] Running daily website scraping + embedding update...")

    visited.clear()
    text_chunks.clear()
    chunk_sources.clear()

    scrape_site_playwright(BASE_URL)

    if not text_chunks:
        print("[WARNING] No content extracted. Skipping embedding.")
        return

    embeddings = generate_embeddings(text_chunks)
    save_vector_db(np.array(embeddings), chunk_sources)
    print("[INFO] Embedding update complete.\n")

# Auto scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(daily_job, "interval", days=1)
scheduler.start()

# Run immediately on startup
daily_job()

# Keep script running
try:
    while True:
        time.sleep(3600)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
