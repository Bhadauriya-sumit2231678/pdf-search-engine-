import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# SerpAPI Key - Add your key here or set as environment variable
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "YOUR_SERPAPI_KEY_HERE")

def search_pdf(query):
    params = {
        "engine": "google",
        "q": f"{query} filetype:pdf",
        "api_key": SERPAPI_KEY,
        "num": 10
    }
    response = requests.get("https://serpapi.com/search", params=params)
    results = []
    if response.status_code == 200:
        data = response.json()
        for result in data.get("organic_results", []):
            link = result.get("link", "")
            if link.endswith(".pdf"):
                results.append({
                    "title": result.get("title", link),
                    "link": link
                })
    return results

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    if not query:
        return jsonify([])
    results = search_pdf(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)