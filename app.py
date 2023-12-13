import os
import string
import asyncio
import requests
from pytube import YouTube
from pytube.exceptions import PytubeError
from flask import Flask, render_template, request, send_file

app = Flask(__name__, static_url_path='/static')

async def download_video_background(yt_url, format):
    try:
        yt = YouTube(yt_url, on_progress_callback=None)
        if format == 'mp4':
            video_stream = yt.streams.get_highest_resolution()
            file_extension = 'mp4'
        elif format == 'mp3':
            audio_stream = yt.streams.get_audio_only(subtype='mp4')
            file_extension = 'mp3'

        filename = clean_filename(yt.title) + '.' + file_extension
        tmp_file_path = os.path.join('/tmp', filename)

        if format == 'mp4':
            video_stream.download(output_path='/tmp', filename=filename)
        elif format == 'mp3':
            audio_stream.download(output_path='/tmp', filename=filename)

        return tmp_file_path
    except Exception as e:
        # Handle the exception
        return None

@app.route('/')
def serveMain():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
async def download_youtube():
    yt_url = request.form['ytUrl']
    format = request.form['format']

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tmp_file_path = await loop.run_in_executor(None, download_video_background, yt_url, format)

    if tmp_file_path:
        return send_file(tmp_file_path, as_attachment=True)

    return "An error occurred during download."

if __name__ == '__main__':
    app.run(debug=True)
