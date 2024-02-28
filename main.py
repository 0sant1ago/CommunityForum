from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Database to store user profiles and discussion threads
user_profiles = {
    "JohnDoe": {
        "nickname": "JohnDoe",
        "profile_info": {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "location": "Cityville, Country",
            "bio": "Passionate about technology and community discussions."
        },
        "reputation": 100
    }
}
discussion_threads = []


# API endpoint for user registration and profile creation
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    nickname = data.get('nickname')
    profile_info = data.get('profile_info')

    if nickname and profile_info:
        user_profiles[nickname] = {'nickname': nickname, 'profile_info': profile_info, 'reputation': 0}
        return render_template('success.html', message="User registered successfully.")
    else:
        return render_template('error.html', error="Nickname and profile information are required."), 400


# API endpoint for creating discussion threads
@app.route('/threads', methods=['POST'])
def create_thread():
    data = request.get_json()
    topic = data.get('topic')
    content = data.get('content')

    if topic and content:
        thread = {'topic': topic, 'content': content, 'author': request.headers.get('Nickname')}
        discussion_threads.append(thread)
        return render_template('success.html', message="Discussion thread created successfully.")
    else:
        return render_template('error.html', error="Topic and content are required."), 400


# API endpoint for fetching user profiles
@app.route('/profiles/<nickname>', methods=['GET'])
def get_profile(nickname):
    profile = user_profiles.get(nickname)

    if profile:
        return jsonify(profile)
    else:
        return render_template('error.html', error="User not found."), 404


# API endpoint for fetching discussion threads
@app.route('/threads', methods=['GET'])
def get_threads():
    return jsonify({"threads": discussion_threads})


# Home page route
@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
