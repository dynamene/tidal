from flask import jsonify

from tidal import create_playlist, delete_playlist, get_playlist_info
from utils import validate_playlist


def tidal(request):
    """Responds to HTTP requests
    GET:
        Returns playlist info and a list of tracks on the playlist.
    POST:
        Creates a playlist for with given track details and returns playlist link.
    DELETE:
        Deletes playlist of provided link and returns success message.
    """
    if request.method == 'GET':
        playlist_link = request.args.get('link')
        response = get_playlist_info(playlist_link)
        return jsonify(response), 200

    elif request.method == 'POST':
        data = request.get_json()

        # Validate data
        result = validate_playlist(data)
        if not result['is_valid']:
            return jsonify({'message': 'Invalid values', 'errors': result['errors']}), 400

        playlist_info = {'name': data['name'],
                         'description': data['description']}
        tracks = data['tracks']
        response = create_playlist(
            track_list=tracks, playlist_info=playlist_info)

        return jsonify(response), 201

    elif request.method == 'DELETE':
        playlist_link = request.args.get('link')
        delete_playlist(playlist_link)
        return jsonify({'message': 'Done'}), 200

    else:
        return jsonify({'message': 'Try again'}), 400
