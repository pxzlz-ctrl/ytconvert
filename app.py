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
        if format == 'mp4':
            video_stream = yt.streams.get_highest_resolution()
            file_extension = 'mp4'
        elif format == 'mp3':
            audio_stream = yt.streams.get_audio_only(subtype='mp4')
            file_extension = 'mp3'
        
        filename = clean_filename(yt.title) + '.' + file_extension
        if format == 'mp4':
            video_stream.download(output_path='static/videos', filename=filename)
        elif format == 'mp3':
            audio_stream.download(output_path='static/videos', filename=filename)
            
        file_path = os.path.join('static', 'videos', filename)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        # Handle the exception
        return "An error occurred: " + str(e)
    finally:
        if file_path is not None:
            os.remove(file_path)

app.run()
