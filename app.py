#!/usr/bin/env python3
"""
Web interface for Post-Mortem Generator
"""

from flask import Flask, render_template_string, request, jsonify
from generate_postmortem import generate_postmortem
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Post-Mortem Generator</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
        }
        input[type="text"], input[type="date"], textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            box-sizing: border-box;
        }
        textarea {
            min-height: 100px;
            font-family: inherit;
        }
        button {
            background: #007bff;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
            margin-right: 10px;
        }
        button:hover {
            background: #0056b3;
        }
        .preview {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 4px;
            border: 1px solid #ddd;
        }
        .preview pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.6;
        }
        .download-btn {
            background: #28a745;
        }
        .download-btn:hover {
            background: #218838;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 Incident Post-Mortem Generator</h1>
        
        <form id="postmortemForm">
            <div class="form-group">
                <label for="incident">1. Incident Name/Title *</label>
                <input type="text" id="incident" name="incident" required placeholder="e.g., API Outage">
            </div>
            
            <div class="form-group">
                <label for="date">2. Incident Date *</label>
                <input type="date" id="date" name="date" required>
            </div>
            
            <div class="form-group">
                <label for="duration">3. Duration *</label>
                <input type="text" id="duration" name="duration" required placeholder="e.g., 2 hours, 30 minutes">
            </div>
            
            <div class="form-group">
                <label for="impact">4. Impact Description *</label>
                <textarea id="impact" name="impact" required placeholder="Describe the impact on users, systems, and business"></textarea>
            </div>
            
            <div class="form-group">
                <label for="rootCause">5. Root Cause *</label>
                <textarea id="rootCause" name="rootCause" required placeholder="Describe the root cause of the incident"></textarea>
            </div>
            
            <div class="form-group">
                <label for="timeline">Timeline (Optional)</label>
                <textarea id="timeline" name="timeline" placeholder="One event per line, e.g.:&#10;10:00 - Incident detected&#10;10:15 - Investigation started"></textarea>
            </div>
            
            <div class="form-group">
                <label for="resolution">Resolution Steps (Optional)</label>
                <textarea id="resolution" name="resolution" placeholder="One step per line"></textarea>
            </div>
            
            <button type="submit">Generate Post-Mortem</button>
            <button type="button" class="download-btn" id="downloadBtn" style="display:none;">Download Markdown</button>
        </form>
        
        <div class="preview" id="preview" style="display:none;">
            <h2>Preview</h2>
            <pre id="previewContent"></pre>
        </div>
    </div>
    
    <script>
        // Set today's date as default
        document.getElementById('date').valueAsDate = new Date();
        
        let currentPostmortem = '';
        
        document.getElementById('postmortemForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = {
                incident: document.getElementById('incident').value,
                date: document.getElementById('date').value,
                duration: document.getElementById('duration').value,
                impact: document.getElementById('impact').value,
                rootCause: document.getElementById('rootCause').value,
                timeline: document.getElementById('timeline').value,
                resolution: document.getElementById('resolution').value
            };
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    currentPostmortem = data.postmortem;
                    document.getElementById('previewContent').textContent = data.postmortem;
                    document.getElementById('preview').style.display = 'block';
                    document.getElementById('downloadBtn').style.display = 'inline-block';
                }
            } catch (err) {
                alert('Error: ' + err.message);
            }
        });
        
        document.getElementById('downloadBtn').addEventListener('click', () => {
            if (!currentPostmortem) return;
            
            const blob = new Blob([currentPostmortem], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `postmortem_${document.getElementById('date').value}_${document.getElementById('incident').value.toLowerCase().replace(/ /g, '_')}.md`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        
        # Format timeline if provided
        timeline = None
        if data.get("timeline"):
            lines = [line.strip() for line in data["timeline"].split("\n") if line.strip()]
            timeline = "\n".join(f"- **{line}**" for line in lines)
        
        # Format resolution if provided
        resolution = None
        if data.get("resolution"):
            lines = [line.strip() for line in data["resolution"].split("\n") if line.strip()]
            resolution = "\n".join(f"{i+1}. {line}" for i, line in enumerate(lines))
        
        postmortem = generate_postmortem(
            incident_name=data["incident"],
            incident_date=data["date"],
            duration=data["duration"],
            impact=data["impact"],
            root_cause=data["rootCause"],
            timeline=timeline,
            resolution=resolution
        )
        
        return jsonify({"postmortem": postmortem})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
