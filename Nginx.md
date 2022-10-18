- https://www.nginx.com/
- Tested version: 1.15.3

## Basics
- case-sensitive for verb (400 error)
- doesn't treat // as a directory (`/images/1.jpg/..//../1.jpg` -> `/1.jpg`)
- doesn't allow in the path: `%00 0x00 %`
- doesn't allow `%2f` as the first slash
- doesn't path normalize `/..`
- doesn't allow underscore (`_`) in header name (doesn't forward it)
- doesn't allow 0x0d in header value

## Fingerprint
- `Server: nginx`
- 400 error
```
<html>
<head><title>400 Bad Request</title></head>
<body bgcolor="white">
<center><h1>400 Bad Request</h1></center>
<hr><center>nginx/1.15.3</center>
</body>
</html>
```
- 403
```
<html>
<head><title>403 Forbidden</title></head>
<body bgcolor="white">
<center><h1>403 Forbidden</h1></center>
<hr><center>nginx</center>
</body>
</html>
```

## Absolute-URI
- supports Absolute-URI with higher priority under host header
- any scheme in Absolute-URI
- doesn't allow `@` in Absolute-URI (400 error)

## location match rules
- (none): If no modifiers are present, the location is interpreted as a prefix match. This means that the location given will be matched against the beginning of the request URI to determine a match.
- =: If an equal sign is used, this block will be considered a match if the request URI exactly matches the location given.
- ~: If a tilde modifier is present, this location will be interpreted as a case-sensitive regular expression match.
- ~*: If a tilde and asterisk modifier is used, the location block will be interpreted as a case-insensitive regular expression match.
- ^~: If a caret and tilde modifier is present, and if this block is selected as the best non-regular expression match, regular expression matching will not take place.

https://www.digitalocean.com/community/tutorials/understanding-nginx-server-and-location-block-selection-algorithms

## proxy_pass
- backend (URL to origin) is uncontrollable
- parses, url-decodes, normalizes, finds location
  - cut off `#fragment`
  - doesn't normalize `/..`
  - // -> /
- if trailing slash is in proxy_pass(`proxy_pass http://backend/`), it forwards the processed request(path)
  - `%01-%FF` in path -> ``!"$&'()*+,-./:;<=>@[\]^_`{|}~``, 0-9, a-Z, `%23 %25 %3F`, `%01-20`, =>`%7F`
    - `%2f` to `/`, which useful for %2f..
    - `<> ' " ` - useful for xss
- if no trailing slash is in proxy_pass (`proxy_pass http://backend`), it forwards the initial request(path)
  - ``/!"$&'()*+,-./:;<=>@[\]^_`{|}~?a#z``  -> ``/!"$&'()*+,-./:;<=>@[\]^_`{|}~?a#z``
  - `%01-%FF` -> `%01-%FF`
- `proxy_pass http://$host/` (with ending `/`) doesn't proxy path-part
  - `proxy_pass http://192.168.78.111:9999 -> http://192.168.78.111:9999/path_from_location/`
- forwards raw bytes (0x01-0x20, > 0x80) in path as-is
- set HTTP/1.0 by default
- `$host` - from the request's `Host` header ; `$http_host`- host from config (default)
- allows >1 `Host` header
  - forwards only the first one
  - in case of `fastcgi_pass` or `uwsgi_pass`, the app gets the second `Host` header
- doesn't forward headers with space symbols in name (` AnyHeader:` or `AnyHeader :`)
- no additional headers to backend

## rewrite
- similar to proxy_pass with trailing slash
- `%0a` cuts the path
  - `/rewrite_slash/123%0a456?a=b` -> `/rewrite_slash/123?a=b`
```
location  /rewrite_slash/ {
   rewrite /rewrite_slash/(.*) /$1  break;
   proxy_pass         http://backend:9999/;
}
```

## Caching
- Nginx only caches GET and HEAD requests
- It respects the Cache-Control and Expires headers from origin server
  - It does not cache responses with Cache-Control set to Private, No-Cache, or No-Store or with Set-Cookie in the response header.  
- Does not honor the `Pragma` and the client's `Cache-Control`
- Doesn't care about `Vary` header
- key for cache: host header and path+query
  - `#`- is ordinary symbol here

### Caching detections
- X-Cache-Status: MISS - custom header which shows caching
- If caching is enabled, the header fields “If-Modified-Since”, “If-Unmodified-Since”, “If-None-Match”, “If-Match”, “Range”, and “If-Range” from the original request are not passed to the origin server.
- doesn't care If-Match for uncached content
- cares If-Match for cached content:
  - W/"0815" - returns 412 Precondition Failed
  - If-Match: * returns body
- doesn't care Range headers


## Vulnerable configs
- one level traversal
  - `/host_noslash_path../something/` -> `/lala/../something/`
```
location /host_noslash_path {
    proxy_pass http://192.168.78.111:9999/lala/;
}
```
- no first /
  - `/without/slash/here` -> `GET without/slash/here HTTP/1.1`
  - (absolute uri?)
```
rewrite /(.*) $1  break;
```
- other examples
  - https://github.com/yandex/gixy

### Dangerous whitespaces
- Nginx allows whitespace symbols in path part
- it forwards them unprocessed
- some backend servers can interpret such a path incorrectly
- Example Nginx(no trailing slash) + gunicorn:
```
location /public/path { proxy_pass http://backend_gunicorn;}
```
  - request to Nginx `GET /private/path/<TAB>HTTP/1.1/../../../../public/path HTTP/1.1`
  - gunicorn reads until first whitespace with `HTTP/1.1`. It sees `GET /private/path/<TAB>HTTP/1.1` and skips rest of the path

## Port in redirect
- port_in_redirect is turned on by default
- when non-default http port is used in listen argument - ```listen 127.0.0.1:12345```
- happens when URL is without trailing slash
- http://example.com/ -> http://example.com/ --> OK
- http://example.com/js -> http://example.com:12345/js --> BAD
- http://example.com/js/ -> http://example.com/js/ --> OK
- observed in setup where nginx web server is behind another reverse proxy that translates port 80 to internal 12345
- Doesn't remove custom hop-by-hop headers listed in `Connection` header.
- Passes value of `Connection` header as is when acting as a proxy.

This section is based on [Abusing HTTP hop-by-hop request headers](https://nathandavison.com/blog/abusing-http-hop-by-hop-request-headers).

# HTTP/2
- Tested version - 1.18
- **Header Names:**
    
    Allowed:`-`
   
    Restricted:`\x00 \x0a \x0d :`   (protocol error)
    
    It removes (doesn't proxy) header with all other symbols
    
    Only in lower case

- **Header Value:**

    Restricted(\x00-\x20):`\x00 \x0a \x0d`

    Allowed:``[]{}:;.,<>?|"\'/_`=+~!@#$%^&*()-``

- **Verb:**

    Uppercase only

    Allowed:`_-`

    Restricted(\x00-\x20):`\x00-\x20` (`\x00 \x0a \x0d` - protocol error)

- **Path:**

    Must start with `/`

    Allowed:``[]{}:;.,<>?|"\'/_`=+~!@#$%^&*()-``

    Restricted(\x00-\x20): `\x00 \x0a \x0d` (protocol error)

    Doesn't support Absolute URI

- **Authority:**

    Allowed:``[]{};.,<>?|"'\_`=+~!@#$%^&*()-`` (without `/`)

    Cannot start with `:`

    Restricted(\x00-\x20):`\x00-\x20` (`\x00 \x0a \x0d` - protocol error)

    With `host` returns 400

- **Scheme:**

    Allowed:`+.:` 

    Restricted(\x00-\x20):`\x00-\x20` (`\x00 \x0a \x0d` - protocol error)

    Doesn't proxy`scheme`
