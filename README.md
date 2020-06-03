# PlayMo Tidal Cloud Function

Tidal API implementation

## Getting Started

- Create a virtual environment `python3 -m venv venv`

- Activate the virtual environment `. venv/bin/activate`

- Install all the dependecies `pip install -r requirements.txt`

- Create a **.env** file and add the values from **.env_example**

- Source your environment variables `source .env`

- To run the Cloud Function locally `functions-framework --target tidal --debug`

## Routes

- **GET**

  - Endpoint: `/?link=tidal_playlist_link`

- **DELETE**

  - Endpoint: `/?link=tidal_playlist_link`

- **POST**

  - Endpoint: `/`

  - Body:

    ```json
    {
      "name": "string", // The playlist name
      "description": "string", // The playlist description
      // List of tracks to add to playlist. Maximum of 10 tracks.
      "tracks": [
        {
          "title": "string", // Track title
          "artist": "string", // Track artist
          "album": "string", // Track album
          "contributors": ["string"], // Track contributors. Must have atleast one value i.e. the track artist
          "duration": "integer" // The track duration in seconds
        }
      ]
    }
    ```
