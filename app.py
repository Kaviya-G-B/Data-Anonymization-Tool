from flask import Flask, render_template, request, send_file, redirect, url_for
import pandas as pd
import hashlib
import os

app = Flask(__name__)
UPLOAD_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        df = pd.read_csv(file)

       
        anonymized_df = df.applymap(lambda x: hashlib.sha256(str(x).encode()).hexdigest() if isinstance(x, str) else x)

        anonymized_filename = f"anonymized_{file.filename}"
        anonymized_filepath = os.path.join(UPLOAD_FOLDER, anonymized_filename)
        anonymized_df.to_csv(anonymized_filepath, index=False)

   
        tables = anonymized_df.to_html(classes='table table-striped table-hover', index=False)

        return render_template('result.html', tables=tables, filename=anonymized_filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
