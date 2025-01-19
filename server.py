from flask import Flask, request, jsonify
from flask_cors import CORS
from xiaohongshu_processor import ContentAdapter
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)
CORS(app)

# Health check endpoint for Railway
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

adapter = ContentAdapter()

@app.route('/api/process', methods=['POST'])
def process_content():
    data = request.json
    text = data.get('text', '')
    
    try:
        result = adapter.process_content(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 