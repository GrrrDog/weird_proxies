- https://varnish-cache.org/
- Tested version: 5.0.0 revision 99d036f

## Basics
- backend (URL to origin) is uncontrollable 
- allows any value for the verb
- allows any path/query values (except 0x00-0x20): GET !i?lala=#anything HTTP/1.1
- doesn't normalize, url-decode request before applying rules
- doesn't forward `AnyHeader :` - 400
- support line folding for headers (` Header:zzz`-> concatenate with previous header)
- doesn't allow >1 `Host:`
- forwards `Host:` header
- adds `X-Forwarded-For:` to req to the origin server 
    - we can send our values in request and it will be added to proxy's request (`examplezzz.com, example2.com`)
- req includes query string (no path part)
  - `req.url ~ "\.jpg$" == ?random=.jpg`

## Fingerprint
- `Via: 1.1 varnish (Varnish/5.0)`
- `X-Varnish: 7`
- `X-Varnish-Host: ip-address-here`
- `X-Varnish-Backend: ip address`
- `X-Varnish-Esi-Method`
- `Accept-Range: bytes`   (for all requests)
- 400 error: `HTTP/1.1 400 Bad Request`

## Absolute-URI
- support Absolute-URI with higher priority under host header
- "http" only in Absolute-URI

## Caching
- it caches GET and HEAD requests
- key for cache: host header and uri 
- status codes cached: 200, 203, 300, 301, 302, 307, 404, 410
- doesn't cache reqs with cookie(!) or Authorization header, or Set-Cookie (default)
  - often practice to cut all cookie headers before sending to origin
- It respects the Cache-Control and Expires headers from origin server (depending on version)
  - it respects CC flags
  - it cares about the max-age parameter and uses it to calculate the TTL for an object.
  - it ignores "Cache-Control: no-cache" by default, but cares about "max-age" (Before V4.0.0?)
- Does not honor the Pragma and the client's Cache-Control 
- doesn't care about Vary, by default

### Caching detection
- X-Varnish: has two figures in case of hit, and one in case of miss. Age is also changed (0 -> \d+ )
```
  X-Varnish: 65563 29 
  X-Varnish: 65563
```
- `Age: 0`
- doesn't care about If-* headers
- support Range header
- If-Range + Range -> returns part of content only (always)

## Vulnerable configs
- Misrouting `/../admin/`
```
if (req.http.host == "sport.example.com") {
        set req.http.host = "example.com";
        set req.url = "/sport" + req.url;
     }
```

- Blacklist bypass `Post //wp-login.php HTTP/1.1`
```
if(req.method == "POST" || req.url ~ "^/wp-login.php$" || req.url ~ "^/wp-admin") {
        return(synth(503));
    }
```