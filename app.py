from flask import Flask, request, send_file
from flask_compress import Compress
from flask_uuid import FlaskUUID
import os
from pydub import AudioSegment
import uuid

app = Flask(__name__)
Compress(app)
FlaskUUID(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/compress_audio', methods=['POST'])
def compress_audio():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    # Get parameters from request body
    format_extension = request.form.get('format', 'mp3')  # Default to mp3 if not specified
    bitrate = request.form.get('bitrate', '64k')  # Default to 64k if not specified

    filename = str(uuid.uuid4()) + f'.{format_extension}'  # Generate a unique filename with specified format extension
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Load audio file
    audio = AudioSegment.from_file(filepath)

    # Compress audio
    compressed_audio = audio.export(filepath, format=format_extension, bitrate=bitrate)

    # Return the URL of the compressed file
    return send_file(filepath, as_attachment=True)



@app.route('/')
def index():
    return 'Hello, world!'

if __name__ == '__main__':
    app.run(debug=True)
