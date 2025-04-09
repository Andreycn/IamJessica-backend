from flask import Flask, request, jsonify
import instaloader
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
L = instaloader.Instaloader()

@app.route('/scrape', methods=['POST'])
def scrape_profile():
    data = request.get_json()
    url = data.get('url')
    if not url or \"instagram.com\" not in url:
        return jsonify({\"error\": \"URL inválida.\"}), 400
    try:
        username = url.rstrip('/').split('/')[-1]
        profile = instaloader.Profile.from_username(L.context, username)
        posts = []
        for post in profile.get_posts():
            posts.append({
                \"caption\": post.caption[:200],
                \"likes\": post.likes,
                \"comments\": post.comments,
                \"url\": post.url
            })
            if len(posts) >= 3:
                break
        return jsonify({
            \"username\": profile.username,
            \"followers\": profile.followers,
            \"posts\": profile.mediacount,
            \"topPosts\": posts
        })
    except Exception as e:
        return jsonify({\"error\": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
