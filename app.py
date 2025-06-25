
from flask import Flask, request, jsonify, send_from_directory
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

app = Flask(__name__, static_folder='static')

CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOG_ID = '2498697094217597332'

def authenticate():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return build('blogger', 'v3', credentials=credentials)

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/create_post', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        service = authenticate()
        post = {
            'title': title,
            'content': content
        }

        result = service.posts().insert(blogId=BLOG_ID, body=post, isDraft=False).execute()
        return jsonify({'message': 'Postagem publicada com sucesso!', 'id': result['id']}), 200

    except HttpError as error:
        return jsonify({'error': f'Erro na API do Blogger: {error}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro inesperado: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
