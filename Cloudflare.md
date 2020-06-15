# Cloudflare
- Tested version: in the beginning of 2019
- HTTP proxying: 80 8080 8880 2052 2082 2086 2095
- HTTPS proxying: 443 2053 2083 2087 2096 8443
- others with the Enterprise plan

## Basics
- similar to [Nginx](Nginx.md)
- `#` - is in request, but everything after it is skiped
- `/../` higher then root - 400
- doesn't support TRACE
- doesn't allow lowercase in Method (not GEt)
- forward Headers by default
- forwards Range header
- doesn't forward ` AnyHeader:` or `AnyHeader :` or ` AnyHeader :`
- adds headers to reqs to the origin server (by default), but doesn't allow to rewrite them 
```
    CF-IPCountry: MT
    X-Forwarded-For: 1.1.1.1,22.22.22.22
    CF-RAY: 4769ea42a630be43-MXP
    X-Forwarded-Proto: http
    CF-Visitor: {"scheme":"http"}
    CF-Connecting-IP: 22.22.22.22
    Accept-Encoding: gzip
```
- we can send our values in `X-Forwarded-For` and it will be prepand to CF's request (`ip_from_us, real_ip`)
- doesn't allow rewrite `CF-Connecting-IP` (403)

## Absolute-URI
- support Absolute-URI, but requires it be the same with Host
- any scheme in Absolute-URI
- doesn't like @ in Absolute-URI

### Fingerprint
- Headers: 
```
  Set-Cookie: __cfduid=d9c4915b5b8aeacdb2a7dfe21abc12b571541699773; expires=Fri, 08-Nov-19 17:56:13 GMT; path=/; domain=.cacheme.tk; HttpOnly
  Server: cloudflare
  CF-RAY: 4769ea42a630be43-MXP
```  
- 400 error
```
<html>
<head><title>400 Bad Request</title></head>
<body bgcolor="white">
<center><h1>400 Bad Request</h1></center>
<hr><center>cloudflare</center>
</body>
</html>
```

## Caching
- When Cloudflare caches static content, the default behaviour is to strip away any cookies coming from the server (Set-Cookie) if the file is going to end up in cache - this is a security safeguard to prevent customers accidentally caching private session cookies. 
- Cloudflare only caches resources served directly from your website (not imges from other resources)
- Status codes cached: 200, 206, 301, 302, 404, 501 ??? (what else?) (https://support.cloudflare.com/hc/en-us/articles/115003014432-HTTP-Status-Codes)
- By default, Cloudflare does not cache HTML content 
    - [How do I cache static HTML?](https://support.cloudflare.com/hc/en-us/articles/200172256)
- it caches files with extenstions - case insensitive (static file extensions):  
    - bmp ejs jpeg pdf ps ttf class eot jpg pict svg webp css eps js pls svgz woff  csv gif mid png swf woff2 doc ico midi ppt tif xls docx jar otf pptx tiff xlsx
- case sensitive when compare key
- `#` - ordinary symbol
- just search for `.jpeg` before `?A`
- key - just a string
- Cache Everything Page Rule - forces caching for other extensions of files
- doesn't care about Cookies
- If the Cache-Control header is set to "private", "no-store", "no-cache",  or "max-age=0", or if there is a cookie in the response, then Cloudflare will not cache the resource, unless a Page Rule is set to cache everything and an Edge Cache TTL is set.
- Caching level (https://support.cloudflare.com/hc/en-us/articles/200168256-What-are-CloudFlare-s-caching-levels-)
    - No Query String: Only delivers files from cache when there is no query string.
    - Ignore Query String: Delivers the same resource to everyone independent of the query string. The Ignore Query String setting only applies to static file extensions
    - Standard: Delivers a different resource each time the query string changes. (default)
- if CF sees `?any=params`, it caches response after several requests
- Cache Deception Armor Page Rule: compares extension and Content-Type from response (jpg must have image/* not text/html)
- it caches 206, but returns the  whole body from cache

- https://support.cloudflare.com/hc/en-us/articles/115003206852-Origin-Cache-Control
- https://support.cloudflare.com/hc/en-us/articles/202775670-How-Do-I-Tell-CloudFlare-What-to-Cache-

### Caching detections
- `CF-Cache-Status: HIT` (`MISS`)
- When Cache Everything is turned on
  - it sets next headers for all responses (including 404)
```
CF-Cache-Status: MISS
Expires: Mon, 24 Dec 2018 00:30:37 GMT
Cache-Control: public, max-age=14400
```
- Didn't find a way to detect Edge Cache TTL (it doesn't set/change headers)
