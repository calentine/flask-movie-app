from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Constants for TMDB API
API_KEY = '14207e5d8c426a1eb6358c1fa1bc4a02'
BASE_URL = 'https://api.themoviedb.org/3'

def make_api_request(endpoint, params):
    """Helper function to make a request to TMDB API."""
    url = f'{BASE_URL}/{endpoint}'
    params['api_key'] = API_KEY
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies')
def movies():
    category = request.args.get('category')
    if category:
        params = {'language': 'en-US', 'page': 1}
        movies = make_api_request(f'movie/{category}', params)
        if movies:
            return render_template('movies.html', movies=movies.get('results', []), category=category)
        else:
            return "Failed to retrieve data from TMDB API", 500
    return "No category provided", 400

@app.route('/search_movie', methods=['GET'])
def search_movie():
    movie_name = request.args.get('movie_name')
    if movie_name:
        params = {'query': movie_name, 'language': 'en-US', 'page': 1}
        search_results = make_api_request('search/movie', params)
        if search_results:
            return render_template('movie.html', search_results=search_results.get('results', []))
        else:
            return "Failed to retrieve data from TMDB API", 500
    else:
        return "No movie name provided", 400

if __name__ == '__main__':
    app.run(debug=True)
