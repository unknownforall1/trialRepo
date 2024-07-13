from flask import Flask, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)
ydl_opts = {
    'format': 'best',
    'outtmpl': '/tmp/downloaded_video.mp4',  # Output filename in tmp directory
}

@app.route('/download_thumbnail', methods=['GET'])
def download_thumbnail():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Missing video_id parameter'}), 400

    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(video_id, download=False)
        thumbnail_url = info['thumbnails'][0]['url']  # Get the first thumbnail
        return jsonify({'thumbnail_url': thumbnail_url})

@app.route('/video_details', methods=['GET'])
def video_details():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Missing video_id parameter'}), 400

    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(video_id, download=False)
        details = {
            'title': info.get('title', ''),
            'duration': info.get('duration', ''),
            'channel': info.get('uploader', ''),
            'views': info.get('view_count', 0)
        }
        return jsonify(details)

@app.route('/download_video', methods=['GET'])
def download_video():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Missing video_id parameter'}), 400

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=' + video_id])

    return send_file('/tmp/downloaded_video.mp4', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
