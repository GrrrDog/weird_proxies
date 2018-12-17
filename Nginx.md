- https://www.nginx.com/
- Tested version:

## Basics
- case-sensitive for verb 
- doesn't treat // as a directory (/images/1.jpg/..//../1.jpg -> /1.jpg)

## Fingerprint
- `Server: nginx`

## Absolute-URI
- support Absolute-URI with higher priority under host header
- any scheme in Absolute-URI
- doesn't like @ in Absolute-URI

## location match rules
- (none): If no modifiers are present, the location is interpreted as a prefix match. This means that the location given will be matched against the beginning of the request URI to determine a match.
- =: If an equal sign is used, this block will be considered a match if the request URI exactly matches the location given.
- ~: If a tilde modifier is present, this location will be interpreted as a case-sensitive regular expression match.
- ~*: If a tilde and asterisk modifier is used, the location block will be interpreted as a case-insensitive regular expression match.
- ^~: If a carat and tilde modifier is present, and if this block is selected as the best non-regular expression match, regular expression matching will not take place.

https://www.digitalocean.com/community/tutorials/understanding-nginx-server-and-location-block-selection-algorithms

## proxy_pass
- parses, url-decodes, normalizes, finds location
  - cut off #fragment
  - doesn't normalize /..
  - // -> /
- if trailing slash is in proxy_pass, it sends processed request
  - doesn't encode `' " < > /`
  - doesn't encode `%2f` to `/`, which useful for %2f..
- if no trailing slash is in proxy_pass, it sends initial request
- `proxy_pass http://$host/` (with ending `/`) doesn't proxy path-part
  - `proxy_pass http://192.168.78.111:9999 -> http://192.168.78.111:9999/path_from_location/`
- forwards raw bytes (0x01-0x20, > 0x80) in path as-is
- set HTTP/1.0 by default
- `$host` - its value equals the server name in the “Host” request; `$http_host`- An unchanged "Host" request
then forward encoded value
- doesn't forward headers with space symbols in name (` AnyHeader:` or `AnyHeader :`)

### Caching
- Nginx only caches GET and HEAD requests
- It respects the Cache-Control and Expires headers from origin server 
  - It does not cache responses with Cache-Control set to Private, No-Cache, or No-Store or with Set-Cookie in the response header.  
- Does not honor the Pragma and the client's Cache-Control 
- key for cache: host header and path+query 
  - `#`- is ordinary symbol here (?)

### Caching detections
- X-Cache-Status: MISS - custom header which shows caching
- If caching is enabled, the header fields “If-Modified-Since”, “If-Unmodified-Since”, “If-None-Match”, “If-Match”, “Range”, and “If-Range” from the original request are not passed to the origin server.
- doesn't care If-Match for uncached content
- cares If-Match for cached content:
  - W/"0815" - returns 412 Precondition Failed 
  - If-Match: * returns body
- doesn't care Range headers


## Vulnerable configs
- one level traversal `/host_noslash_path../somthing/` -> 
```
location /host_noslash_path {
    proxy_pass http://192.168.78.111:9999/lala/;
}
```
- no first / (absolute uri?) `/without/slash/here` -> `GET without/slash/here HTTP/1.1`
```
rewrite /(.*) $1  break;
```