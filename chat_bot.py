import os
import faiss
import pickle
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Load FAISS vector index + source chunks
index = faiss.read_index("website_index.faiss")
with open("sources.pkl", "rb") as f:
    sources = pickle.load(f)

# Load embedder
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# System Instructions
instructions = '''
You are a ai chat bot helping the users with thier doubts or any question regarding my website.You need to remeber that u are not a chat bot or ai , you are a human assisting the user with thier question or queries.
keep the flow of the conersation very natural and genric.Keep the conversation sequential. try to pursue the users to take a demo don't force but pursue in a very intutive and smart way.
you have multiple pages such as - price , home , contact us page. if the user asks for these page or the user's conversation suggest to any of this page then return that page name.
keep your response short and precise , so that it shouldn't look like a long paragraph ,and be intutive and smart while talking to user , use mutiple emojis in text.
if user asks or want to make a call to website customer service then returrn t=any dummy number.
if the user asks to schedule an appointment , then just return a page change to "calendly" and all other fileds empty.
if the user asks to help him sign up or on board then return "page change : auth" and all other fileds empty.
Don't display time untill it's required.
after everything your response should be like this , Always return your response in the following strict JSON format (with double quotes only):
{
    "page change":" (return the page name , if user asked you take hime on that page or you think that there is need to change the page ),
    "text":" (your msg to the user query or on going conversation ),
    "suggested page" : " ( based on user queries or conversation , recommend the different website pages to visit )
}
If no page change or suggestion is needed, use "none".
Make sure it's valid JSON.
'''

def retrieve_context(query, k=3):
    query_emb = embedder.encode([query])
    D, I = index.search(np.array(query_emb), k)
    context = "\n\n".join([sources[i] for i in I[0]])
    return context

def medical_assistant_chat():
    print("👩‍⚕️ MedyBot: Hello!! How can I help you today?")
    chat_history = [
        {"role": "user", "parts": [instructions]}
    ]

    while True:
        now = datetime.now()
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("👩‍⚕️ MedyBot: If you have something, come to me anytime.")
            break

        # Retrieve top 3 relevant website content chunks
        context_snippets = retrieve_context(user_input)

        # Add user input and context to the prompt
        full_input = f"""User query: {user_input}
Relevant website context:
{context_snippets}
Current time: {now}
"""
        chat_history.append({"role": "user", "parts": [full_input]})
        response = model.generate_content(chat_history)
        bot_reply = response.text
        print(f"👩‍⚕️ MedyBot: {bot_reply}")
        chat_history.append({"role": "model", "parts": [bot_reply]})

if __name__ == "__main__":
    medical_assistant_chat()
