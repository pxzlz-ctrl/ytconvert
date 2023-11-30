import os
import string
import requests
from pytube import YouTube
from pytube.exceptions import PytubeError
from flask import Flask, render_template, request, send_file
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def serveMain():
    return render_template('index.html')

def clean_filename(title):
  clean_title = title.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).replace('  ', ' ').strip()
  return clean_title

@app.route('/download', methods=['POST'])
def download_youtube():
    yt_url = request.form['ytUrl']
    format = request.form['format']
    file_path = None
    try:
        yt = YouTube(yt_url, on_progress_callback=None)
        stream = yt.streams.filter(only_audio=format == 'mp3').first()
        filename = clean_filename(yt.title) + ('.mp3' if format == 'mp3' else '.mp4')
        stream.download('static/videos', filename=filename)
        file_path = os.path.join('static', 'videos', filename)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        # Handle the exception
        return "An error occurred: " + str(e)
    finally:
        if file_path is not None:
            os.remove(file_path)

app.run(host='0.0.0.0', port=8080)
