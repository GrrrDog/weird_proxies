
# Fastly
- Tested version: in the beginning of 2019
- based on [Varnish](Varnish.md) 2.1 
- proxies only 80 and 443 (?)

## Basics
- similar to [Varnish](Varnish.md) 
- allows any path/query values (except 0x00-0x20): GET !i?lala=#anything HTTP/1.1
- doesn't normalize request before applying rules
- doesn't url-decode request before applying rules
- doesn't forward `AnyHeader :` - 400
- support line folding for headers (` Header:zzz`-> concatenate with previous header)
- doesn't allow >1 `Host:`
- headers (req.header) case-insensitive
- req includes query string (no other properties)
  - `req.url ~ "\.jpg$"` == `?random=.jpg`
- adds headers to req to the origin server (by default)
```
    Fastly-Orig-Accept-Encoding: gzip, deflate
    Fastly-Client-IP: 213.165.190.50
    X-Timer: S1542133246.162954,VS0
    X-Varnish: 2429674486
    X-Varnish: 1846707052
    Fastly-Client: 1
    Fastly-FF: 4D8lKmpzU60D/ZSEGjdK5r2C9uuDCPe0KsjM4dmJxjg=!HHN!cache-hhn1543-HHN, 4D8lKmpzU60D/ZSEGjdK5r2C9uuDCPe0KsjM4dmJxjg=!HHN!cache-hhn1544-HHN
    CDN-Loop: Fastly
```
  - `Fastly-FF: .*` shows Fastly-Debug-Path, Fastly-Debug-TTL, Fastly-Debug-Digest
  - allows rewriting them 

## Absolute-URI
- similar to [Varnish](Varnish.md) 
- we can rewrite host header 
```
    GET httpa://localhost/ HTTP/1.1
    Host: valid.com
```

## Fingerprint
- fingerprint default: 
```
    Via: 1.1 varnish
    Age: 0
    X-Served-By: cache-fra19143-FRA
    X-Cache: MISS
    X-Cache-Hits: 0
    X-Timer: S1542130425.787081,VS0,VE95
    X-Fastly-Request-ID: ceb40030fac03f7a0c16e7d095002a350bef0059 (sometimes)
```

## Caching
https://docs.fastly.com/guides/tutorials/cache-control-tutorial
- the host header and the URI - the default key
- Status codes cached: 200, 203, 300, 301, 302, 404, 410
- It doesn't care about Cookies
- It doesn't care about client CC headers 
- Cares cache Cache-Control: private  
- Cares max-age and Expires, but can be overidden with cache custom TTL
- Also cares `Surrogate-Control: max-age=\d+` (This header gets stripped)
- Fastly does not currently respect `no-store` or `no-cache` directives
- doesn't cache resp with Set-Cookie (default)

### Caching detection
- `X-Cache: MISS` (HIT)

### Vuln config
- similar to [Varnish](Varnish.md) 
- Web cache deception.  `/images/..%2fauth.php` -> `auth.php` cached  (session_start doesn't add "private" to CC)
```
if req.url ~ "^/images/" set TTL 600
```
