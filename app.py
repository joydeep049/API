import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

API_URL = "https://devapi.beyondchats.com/api/get_message_with_sources"

def fetch_data():
    data = []
    page = 1

    while True:
        response = requests.get(API_URL, params={'page': page})
        if response.status_code != 200:
            print(f"Error fetching data from API: {response.status_code}")
            break
        
        response_data = response.json()
        print(f"Fetched data for page {page}: {response_data}")  # Debugging print
        
        if 'results' not in response_data:
            print(f"Unexpected response structure: {response_data}")
            break
        
        data.extend(response_data['results'])
        
        if 'total_pages' not in response_data or page >= response_data['total_pages']:
            break
        
        page += 1
    
    return data

def identify_citations(data):
    citations = []
    
    for item in data:
        response_text = item['response_text']
        sources = item['sources']
        matched_sources = []

        for source in sources:
            if source['context'] in response_text:
                matched_sources.append(source)
        
        citations.append({
            'response_text': response_text,
            'citations': matched_sources
        })
    
    return citations

@app.route('/')
def index():
    data = fetch_data()
    citations = identify_citations(data)
    return render_template('template.html', citations=citations)

@app.route('/api/citations')
def api_citations():
    data = fetch_data()
    citations = identify_citations(data)
    return jsonify(citations)

if __name__ == '__main__':
    app.run(debug=True)
