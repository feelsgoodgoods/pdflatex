from flask import Flask, request, send_file, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def welcome():
    return """
<h1>Welcome!</h1>
<p>This is a simple LaTeX compiler service.</p>
<p>Send a POST request to /compile with a JSON object containing the LaTeX code.</p>
<p>This is a free service for now, please do not abuse it.</p>
<p>Example:</p>
<code>
curl -X POST https://your-heroku-app-url/compile \
     -H "Content-Type: application/json" \
     -d '{"latex":"\\documentclass{article}\\begin{document}Hello, World!\\end{document}"}' \
     --output output.pdf
</code>
"""

@app.route('/compile', methods=['POST'])
def compile_latex():
    data = request.json
    if not data or 'latex' not in data:
        return jsonify({"error": "No LaTeX data provided"}), 400
    latex_text = data['latex']
    filename = 'output.tex'
    pdf_filename = 'output.pdf'

    with open(filename, 'w') as file:
        file.write(latex_text)

    cmd = ['pdflatex', '-interaction=nonstopmode', filename]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        return jsonify({"error": "LaTeX compilation failed", "details": result.stderr}), 500

    if not os.path.exists(pdf_filename):
        return jsonify({"error": "PDF file not generated"}), 500

    return send_file(pdf_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

