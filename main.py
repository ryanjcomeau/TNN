# make sure python installed
#set up virtual env:
   # python3 -m venv .venv 
    #source .venv/bin/activate
#install packages:
    #pip install requests beautifulsoup4 openai schedule python-dotenv
#create files:
    #├── .venv/                  # virtual environment
    #├── .env                    # (store your API keys here)
    #├── fitness_blog_bot.py     # (main script)
    #├── README.md               # optional


import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI  # new import

# 1) Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # new client object

def fetch_text(url):
    """Download page & extract paragraphs."""
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})  # helps with some sites
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return "\n\n".join(p.get_text() for p in soup.find_all("p"))

def summarize_to_blog(text, max_words=500):
    """Use OpenAI to write a blog-style summary."""
    prompt = (
        f"Write a concise, engaging blog post (≈{max_words} words) based on the following content:\n\n"
        + text
    )
    response = client.chat.completions.create(  # updated method
        model="gpt-4o-mini",  # you can still use "gpt-3.5-turbo" if you want
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_words * 4 // 3,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def save_blog(content, filename="blog_post.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    url = input("Enter the URL to summarize: ").strip()
    print("Fetching content…")
    text = fetch_text(url)
    print(f"Extracted ~{len(text.split())} words. Summarizing…")
    blog = summarize_to_blog(text)
    save_blog(blog)
    print("✅ Blog post saved to blog_post.md")

if __name__ == "__main__":
    main()
