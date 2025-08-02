# 🧠 Website-Aware Chatbot with Daily Embedding Updates

This project builds a smart chatbot that automatically scrapes a website, creates vector embeddings using Gemini & Sentence Transformers, and stores them in a FAISS vector database. The chatbot can then answer user questions intelligently based on the most relevant website content.

---

## 🚀 Features

- ✅ Daily website scraping using Playwright (headless browser)
- ✅ Content cleaned and chunked smartly using `BeautifulSoup`
- ✅ Embeddings generated using **Gemini 2.5 Flash** via `google-generativeai`
- ✅ Vector similarity search via `FAISS` (lightweight and fast)
- ✅ Chatbot uses relevant website context to craft smart, helpful responses
- ✅ Page recommendation & redirection logic
- ✅ Supports ongoing conversation with sequential memory
- ✅ Uses `apscheduler` to re-embed website once a day
- ✅ Clean response formatting for integration with frontend

---

## 🧩 Folder Structure

```bash
📦your-project/
├── embed_website.py         # Script to scrape and embed website (daily update)
├── chatbot.py               # Chatbot logic with Gemini
├── website_index.faiss      # Saved FAISS index file (generated)
├── sources.pkl              # Pickled content chunks (generated)
├── .env                     # API keys (keep secret)
├── requirements.txt         # All Python dependencies
└── README.md                # You are here
```

---

## 🌐 Target Website

The system is designed to work with:

> 🔗 [https://docs-path.vercel.app/](https://docs-path.vercel.app/)

You can change the website URL easily in `embed_website.py`.

---

## 📥 Installation & Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourname/yourproject.git
cd yourproject
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install all dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browser drivers

```bash
playwright install
```

### 5. Setup environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_google_generative_ai_key
```

> 🔐 You can get your Gemini API key from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

## ⚙️ Scripts Overview

### ✅ `embed_website.py`

- Scrapes the website
- Cleans and chunks the text
- Sends content to Gemini for embedding
- Saves embeddings to FAISS (`website_index.faiss`)
- Stores raw content in `sources.pkl`
- Auto-runs daily using `apscheduler`

Run it manually:

```bash
python embed_website.py
```

### ✅ `chatbot.py`

- Loads the embeddings & content
- Uses `SentenceTransformer` to embed user query
- Finds similar website chunks from FAISS
- Generates reply with Gemini using query + context
- Handles page suggestions, appointment booking, customer service, etc.

Run it:

```bash
python chatbot.py
```

Example interaction:

```
👩‍⚕️ MedyBot: Hello!! How can I help you today?
You: Tell me about your pricing
👩‍⚕️ MedyBot: Sure! Here’s our pricing info 💰🙂
"page change": "price"
"text": "Our plans are tailored for individuals and clinics."
"suggested page": "contact us"
```

---

## 🧠 How It Works

### 🔄 Daily Embedding Flow

1. Scrape target website using Playwright
2. Clean the HTML using `BeautifulSoup`
3. Split content into chunks of \~1000 characters
4. Generate vector embeddings for each chunk using Gemini
5. Save to `FAISS` index
6. Schedule re-run every 24 hours

### 💬 Chatbot Flow

1. Embed the user query with `SentenceTransformer`
2. Search FAISS index for similar website chunks
3. Send context + user query to Gemini
4. Generate natural, helpful responses
5. Format the reply with:

   - `text`
   - `page change` (if user explicitly wants a page)
   - `suggested page` (based on conversation flow)

---

## 🧠 Models Used

| Task                 | Model                                        |
| -------------------- | -------------------------------------------- |
| User Query Embedding | `sentence-transformers/all-MiniLM-L6-v2`     |
| Chunk Embedding      | `Gemini 2.5 Flash` via `google-generativeai` |
| Vector Search        | `FAISS`                                      |
| Chat Response        | `Gemini 2.5 Flash`                           |

---

## 🔄 Scheduling

Embeddings are updated every 24 hours using APScheduler:

> Inside `embed_website.py`:

```python
scheduler.add_job(scrape_and_embed, "interval", days=1)
```

You can modify the interval to `hours=12` or use a cron pattern if needed.

---

## 🧪 Customization

### ✅ Change Website URL:

In `embed_website.py`:

```python
url = "https://docs-path.vercel.app/"  # ← change here
```

### ✅ Modify chunk size:

```python
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
```

### ✅ Adjust embedding model:

You can switch to other `sentence-transformers` if needed for queries.

---

## 🛡️ Security Notes

- Never expose your `.env` file publicly.
- Use `.gitignore` to exclude `*.pkl`, `.env`, and `*.faiss`.

---

## 🧰 Troubleshooting

| Issue              | Solution                                     |
| ------------------ | -------------------------------------------- |
| `playwright` error | Run `playwright install`                     |
| Gemini API fails   | Check `.env` key or usage quota              |
| FAISS not found    | Make sure `website_index.faiss` is generated |
| No chatbot reply   | Check internet and Gemini response validity  |

---

## 💡 Future Improvements

- Add streaming frontend using Gradio or React
- Handle Gemini embedding retries & chunk batching
- Export answers as logs for analytics
- Support multiple URLs or PDFs

---

## 📜 License

MIT License. Free to use with attribution.

---

