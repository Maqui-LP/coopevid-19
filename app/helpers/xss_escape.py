from flask import escape

def escape_xss(data):
    escaped_data = data
    for field in data:
        if type(data[field]) is str:
            escaped_data[field]=str(escape(data[field]))

    return escaped_data