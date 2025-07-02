from flask import Flask, render_template, request, send_from_directory
from dotenv import load_dotenv
import os
from deskew import deskew_image


app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'No file uploaded.', 400
        file = request.files['image']
        if file.filename == '':
            return 'No selected file.', 400
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'deskewed_' + file.filename)
        deskew_image(filepath, output_path)

        return render_template('index.html', original=file.filename, deskewed='deskewed_' + file.filename)

    return render_template('index.html')

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
