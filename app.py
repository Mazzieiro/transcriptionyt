from flask import Flask, jsonify, request
from youtube_transcript_api import NoTranscriptFound, YouTubeTranscriptApi
import os

app = Flask(__name__)

@app.route('/api/transcribe', methods=['POST'])
def transcribe_video():
    data = request.get_json()
    video_url = data.get('url_yt')
    video_id = video_url.split('v=')[1]

    languages = ['en', 'pt']  # Lista de preferências de idiomas

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Tenta obter a transcrição no idioma preferido ou no fallback
        for lang in languages:
            try:
                transcript = transcript_list.find_transcript([lang])
                transcript = transcript.fetch()
                return jsonify(transcript)
            except NoTranscriptFound:
                continue  # Tenta o próximo idioma na lista

        return jsonify({"error": "No suitable transcript found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
