import os
import string
from pytube import YouTube
from flask import Flask, render_template, request, send_file
from pytube.exceptions import PytubeError

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def serve_main():
    return render_template('index.html')

def clean_filename(title):
    clean_title = title.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).replace('  ', ' ').strip()
    return clean_title

def download_youtube_video(yt_url, file_format):
    try:
        youtube_video = YouTube(yt_url, on_progress_callback=None)
        
        format_mapping = {
            'mp4': ('get_highest_resolution', 'mp4'),
            'mp3': ('get_audio_only', 'mp3')
        }

        stream_method, file_extension = format_mapping[file_format]
        stream = getattr(youtube_video.streams, stream_method)()

        filename = clean_filename(youtube_video.title) + '.' + file_extension
        tmp_file_path = os.path.join('/tmp', filename)

        stream.download(output_path='/tmp', filename=filename)

        return tmp_file_path
    except PytubeError as e:
        raise Exception(f"Pytube error occurred: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

@app.route('/download', methods=['POST'])
def download_youtube():
    yt_url = request.form.get('ytUrl')
    file_format = request.form.get('format')
    tmp_file_path = None
    
    try:
        tmp_file_path = download_youtube_video(yt_url, file_format)
        return send_file(tmp_file_path, as_attachment=True)
    except Exception as e:
        return str(e)
    finally:
        if tmp_file_path is not None:
            os.remove(tmp_file_path)
