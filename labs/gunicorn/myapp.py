def app(environ, start_response):
    data = ""
    for key in environ:
        data = data + str(key) + '->' + str(environ[key]) + "\n"
    data = str.encode(data)

    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])