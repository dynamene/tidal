from cerberus import Validator


def validate_playlist(data):
    """Validate playlist
    """
    schema = {
        "name": {"type": "string", "required": True},
        "description": {"type": "string", "empty": True, "required": True},
        "tracks": {
            "type": "list",
            "empty": False,
            "required": True,
            "maxlength": 20,
            "schema": {
                "type": "dict",
                "required": True,
                "require_all": True,
                "allow_unknown": True,
                "schema": {
                    "title": {"type": "string"},
                    "artist": {"type": "string"},
                    "contributors": {"type": "list", "minlength": 1, "schema": {"type": "string"}},
                    "duration": {"type": "integer"},
                    "album": {"type": "string"}
                }
            }
        }
    }

    v = Validator(schema)
    v.allow_unknown = True
    v.validate(data)
    if v.errors:
        return {"is_valid": False, "errors": v.errors}

    return {"is_valid": True}
