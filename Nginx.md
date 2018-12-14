## Nginx
- support Absolute-URI with higher priority under host header
- any scheme in Absolute-URI
- doesn't like @ in Absolute-URI
- doesn't treats // as a directory (/images/1.jpg/..//../1.jpg will be /1.jpg)
- case-sensitive for methods (get != GET)

### location match
https://www.digitalocean.com/community/tutorials/understanding-nginx-server-and-location-block-selection-algorithms
  (none): If no modifiers are present, the location is interpreted as a prefix match. This means that the location given will be matched against the beginning of the request URI to determine a match.
  =: If an equal sign is used, this block will be considered a match if the request URI exactly matches the location given.
  ~: If a tilde modifier is present, this location will be interpreted as a case-sensitive regular expression match.
  ~*: If a tilde and asterisk modifier is used, the location block will be interpreted as a case-insensitive regular expression match.
  ^~: If a carat and tilde modifier is present, and if this block is selected as the best non-regular expression match, regular expression matching will not take place.

### proxy_pass
- forward Headers by default
- set HTTP/1.0 by default
- $host - its value equals the server name in the “Host” request; $http_host- An unchanged “Host” request
- at first, urldecode (path+query string), then finds location, then forward encoded value
- doesn't forward ` AnyHeader:` or `AnyHeader :`
- proxy_pass http://$host/ (with ending `/`) doesn't proxy path-part
  - proxy_pass http://192.168.78.111:9999 -> http://192.168.78.111:9999/path_from_location/
- location  /foo works lite `startswith` (== /fooanythinghere)
- ! location ~ \.php { - all phpsomething is PHP?
- ! it normalizes (///, /./, ../../) and urldecodes path, but sends unnormalized to backend if proxy_path is without trailing slash
  - /securedared/%3f/../../zazaza.php?zzzz=asdasd ???
  - but also resends raw bytes to backend
- it normalizes and urldecodes (///, /./, ../../) path and sends unnormalized to backend
  - but decodes ' " < >, etc which makes possible XSS
  - decode %2f to /, which useful for %2f.. (nginx+apache)
  - but also resends raw bytes to backend
  - but also support no HTTP/1.1
- ! rewrite /(.*) $1  break; - GET without/slash/here HTTP/1.1
- ! vulnerable configuration to /host_noslash_path../
    location /host_noslash_path {
        proxy_pass http://192.168.78.111:9999/lala/;
    }
- It respects the Cache-Control headers from origin servers. 
  - It does not cache responses with Cache-Control set to Private, No-Cache, or No-Store, Expires or with Set-Cookie in the response header.  NGINX only caches GET and HEAD client requests. 
  - NGINX does not honor the Pragma header by default
- X-Cache-Status: MISS - common header which shows caching
- If caching is enabled, the header fields “If-Modified-Since”, “If-Unmodified-Since”, “If-None-Match”, “If-Match”, “Range”, and “If-Range” from the original request are not passed to the proxied server.
- whole query string is used as a key for cache without urldecode and normalization (# - is ordinary symbol)
- doesn't care If-Match for uncached content
- cares If-Match for cached content: W/"0815" - returns 412 Precondition Failed and If-Match: * returns body
- doesn't care Range headers
- case sensitive for location
