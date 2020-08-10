import json
import os
import html

import tidalapi

# Tidal playlist link format
# https://tidal.com/browse/playlist/f91b5fe5-b760-4053-9521-14b27cbffd39
# Track ID: 117801256

username = os.getenv("TIDAL_USERNAME")
password = os.getenv("TIDAL_PASSWORD")

session = tidalapi.Session()
session.login(username, password)


def get_playlist_info(playlist_link):
    """Get playlist info
    """
    playlist_id = playlist_link.split("/")[-1]
    try:
        playlist = session.get_playlist(playlist_id)
    except:
        return {"message": "Invalid Link", "isValid": False, "playlist": {}}

    if playlist.creator["id"] == 0:
        return {"message": "Can't use Tidal auto-generated playlists.", "isValid": False, "playlist": {}}

    playlist_tracks = session.get_playlist_tracks(playlist_id)[0:20]
    tracks = []
    for track in playlist_tracks:
        tracks.append({"title": track.name, "artist": track.artist.name, "contributors": [
            artist.name for artist in track.artists], "duration": track.duration,
            "album": track.album.name, "trackCover": track.album.picture(320, 320)})

    description = ""
    if playlist.description:
        description = playlist.description

    playlist_info = {"name": playlist.name, "numTracks": len(tracks),
                     "description": description, "playlistCover": playlist.picture(320, 320), "tracks": tracks}
    return {"isValid": True, "playlist": playlist_info}


def find_song(track_info):
    """Find track info based on information provided
    """
    results = session.search(
        "track", f"{track_info['title']} {track_info['artist']}")
    track_id = ""

    for track in results.tracks:
        score = 0

        # Check that the title and artist are the same as the ones provided
        if track.name == track_info["title"] and track.artist.name == track_info["artist"]:
            score += 2

        # Check if album is the same as provided
        if track.album.name == track_info["album"]:
            score += 1

        # Check if track contributors is the same
        if set([artist.name for artist in track.artists]) == set(track_info["contributors"]):
            score += 1

        # Check if the duration of the songs match
        if track.duration == track_info["duration"]:
            score += 1

        # Check the track score
        if score >= 4:
            track_id = track.id
            break

    return track_id


def create_playlist(track_list, playlist_info):
    """Create playlist
    """
    track_id_list = []
    missing_tracks = []
    for track in track_list:
        track_id = find_song(track)
        if track_id:
            track_id_list.append(str(track_id))
        else:
            missing_tracks.append(track)

    # Create Playlist
    user_id = session.user.id
    result = session.request("POST", f"users/{user_id}/playlists", data={
                             "title": playlist_info["name"], "description": playlist_info["description"]})
    playlist_id = json.loads(result.content.decode("utf-8"))["uuid"]

    # Add tracks to playlist
    etag = session.request("GET", f"playlists/{playlist_id}").headers["ETag"]
    headers = {"if-none-match": etag}
    data = {"trackIds": ",".join(track_id_list), "toIndex": 0}
    session.request(
        "POST", f"playlists/{playlist_id}/tracks", data=data, headers=headers)

    link = f"https://tidal.com/browse/playlist/{playlist_id}"

    return {"link": link, "missingTracks": missing_tracks, "numMissingTracks": len(missing_tracks)}


def delete_playlist(playlist_link):
    """Delete playlist
    """
    # Get playlist id
    playlist_id = playlist_link.split("/")[-1]

    # Delete playlist
    etag = session.request("GET", f"playlists/{playlist_id}").headers["ETag"]
    headers = {"if-none-match": etag}
    session.request("DELETE", f"playlists/{playlist_id}", headers=headers)

    return True


if __name__ == "__main__":
    # https://tidal.com/browse/playlist/0c922ce1-0e63-46bb-a58f-24f547c419b1
    # http://images.osl.wimpmusic.com/im/im?w=320&h=320&uuid=0c922ce1-0e63-46bb-a58f-24f547c419b1
    # https://resources.tidal.com/images/9e04048c/47f1/4493/8803/b3ef380f2ba7/320x320.jpg

    playlist = get_playlist_info(
        "https://tidal.com/browse/playlist/f91b5fe5-b760-4053-9521-14b27cbffd39")
    track_list = playlist["playlist"]["tracks"]

    playlist_info = {"name": "Tidal API",
                     "description": "Automated playlist creation"}

    # Create playlist
    playlist_link = create_playlist(
        track_list=track_list, playlist_info=playlist_info)
    print(playlist_link)

    # Delete playlist
    print(delete_playlist(playlist_link))
