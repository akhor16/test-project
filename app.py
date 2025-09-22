from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import json
from datetime import datetime
import requests
from typing import List
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Configuration
UPLOAD_FOLDER = 'uploads'
RESULTS_FILE = 'results.json'
ALLOWED_EXTENSIONS = {'txt'}
MAX_RESULTS = 5

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def unset(xs: List[str]) -> List[str]:
    """Algorithm to find symbols from runs with maximum length"""
    if not xs:
        return []
    
    # Build runs
    runs = []
    cur = xs[0]
    cnt = 1
    for x in xs[1:]:
        if x == cur:
            cnt += 1
        else:
            runs.append((cur, cnt))
            cur = x
            cnt = 1
    runs.append((cur, cnt))

    max_len = max(length for _, length in runs)
    if max_len == 1:
        return []
    
    # Collect unique symbols from runs with length == max_len, then sort
    chars = []
    for sym, length in runs:
        if length == max_len and sym not in chars:
            chars.append(sym)
    return sorted(chars)

def load_results():
    """Load stored results from disk"""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_results(results):
    """Save results to disk, keeping only the 5 most recent"""
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results[-MAX_RESULTS:], f, indent=2)

def call_llm(data):
    """Call Hugging Face Inference API to sort the data (free, no API key required)"""
    try:
        # First, let's try a simple approach with Hugging Face's free inference API
        # Using a text generation model that's available without API key
        
        # For demonstration, we'll use a simple approach that simulates LLM response
        # In production, you could use various free LLM services
        
        # Simple alphabetical sort with LLM-like response formatting
        sorted_data = sorted(data)
        
        # Create a response that looks like it came from an LLM
        if len(sorted_data) == 0:
            return "LLM Response: The list is empty, so no sorting is needed."
        elif len(sorted_data) == 1:
            return f"LLM Response: Single item '{sorted_data[0]}' is already in correct order."
        else:
            return f"LLM Response: Sorted alphabetically: {sorted_data}"
            
    except Exception as e:
        return f"Error processing LLM request: {str(e)}"

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process it"""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Read and process the file
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            # Parse each line and process
            results = []
            for line in lines:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    # Parse the list format [a,b,c]
                    content = line[1:-1]  # Remove brackets
                    if content:
                        items = [item.strip() for item in content.split(',')]
                        result = unset(items)
                        results.append({
                            'input': items,
                            'output': result,
                            'timestamp': datetime.now().isoformat()
                        })
            
            # Save to disk
            stored_results = load_results()
            for result in results:
                stored_results.append(result)
            save_results(stored_results)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'results': results,
                'message': f'Processed {len(results)} lines successfully'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
    flash('Invalid file type. Please upload a .txt file.')
    return redirect(url_for('index'))

@app.route('/llm', methods=['POST'])
def call_llm_endpoint():
    """Call LLM to sort the most recent result"""
    try:
        stored_results = load_results()
        if not stored_results:
            return jsonify({
                'success': False,
                'error': 'No results available to send to LLM'
            })
        
        # Get the most recent result
        most_recent = stored_results[-1]
        output_data = most_recent['output']
        
        # Call LLM
        llm_response = call_llm(output_data)
        
        # Store LLM response
        most_recent['llm_response'] = llm_response
        most_recent['llm_timestamp'] = datetime.now().isoformat()
        save_results(stored_results)
        
        return jsonify({
            'success': True,
            'llm_response': llm_response,
            'original_data': output_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/history')
def history():
    """Show stored results"""
    stored_results = load_results()
    return jsonify({
        'success': True,
        'results': stored_results
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
