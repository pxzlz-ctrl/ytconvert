import os
import string
import asyncio
from pytube import YouTube
from flask import Flask, render_template, request, jsonify
from pytube.exceptions import PytubeError

app = Flask(__name__, static_url_path='/static')

async def download_youtube_video_async(yt_url, file_format):
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

def clean_filename(title):
    clean_title = title.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).replace('  ', ' ').strip()
    return clean_title

async def background_task(yt_url, file_format):
    tmp_file_path = await download_youtube_video_async(yt_url, file_format)
    # Perform any additional processing or notifications here
    return tmp_file_path

def handler(event, context):
    if event['httpMethod'] == 'POST':
        data = json.loads(event['body'])
        yt_url = data.get('ytUrl')
        file_format = data.get('format')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(background_task(yt_url, file_format))
        loop.close()

        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'Download complete.', 'file_path': result})
        }
