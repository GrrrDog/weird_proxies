
AWS services were tested in 2019-2020

# AWS ELB (ALB)
https://docs.aws.amazon.com/en_us/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html


## Basics
- looks like [Nginx](Nginx.md) without trailing slash
- `Both Application Load Balancers and Classic Load Balancers use HTTP/1.1 on back-end connections (load balancer to registered target). Keep-alive is supported on back-end connections by default. For HTTP/1.0 requests from clients that do not have a host header, the load balancer generates a host header for the HTTP/1.1 requests sent on the back-end connections.`
- it partly supports HTTP/0.9 (proxy forwards the request, but doesn't return the response from a server)
- ! route by ip 
  - doesn't care about Host header
- case-sensitive for verb (400 error)
- doesn't allow `%2f` as the first slash (400)
- doesn't allow `/../` higher the root (400)
- doesn't allow in the path: `%00 0x00 %`
- doesn't normalize /..
- doesn't normalize // (with exception below)
- `%0a` doesn't cut the path
- set HTTP/1.1 to the origin 
- allows >1 `Host` header
  - forwards only the first one
- forward headers with space symbols in name (` AnyHeader:` and `AnyHeader :`)
- adds headers to request to origin(by default): `X-Forwarded-For: , X-Forwarded-Port: , X-Forwarded-Proto: , X-Amzn-Trace-Id: `
  - we can send our values in request `X-Forwarded-For:, X-Amzn-Trace-Id: `  and it will be added to the forwarded header (`examplezzz.com, example2.com`)
  - doesn't allow 0x0d in value (400)
- it allows/forwards `_` in header name (`X_Forwarded_Port`)
- forward unprocessed path
  - ``/!"$&'()*+,-./:;<=>@[\]^_`{|}~?a#z%``  -> ``/!"$&'()*+,-./:;<=>@[\]^_`{|}~?a#z%``
  - `%01-%FF` -> `%01-%FF`
- proxing the space (to fake HTTP version?)
  - `/lala1/aa/as? http/1.0 HTTP/1.1` -> `/lala1/aa/as? http/1.0 HTTP/1.1` (doesn't allow (400) in capital case `HTTP`)
  - `/lala1/aa/as http/1.11 ?` -> `GET /lala1/aa/as%20http/1.11%20 HTTP/1.1`
- `/aaa aaa/` - this combination (space) changes how ELB works
  - it forwards the processed path 
- TRACE is not allowed (405)
  
## Fingerprint
- Headers
`Server: awselb/2.0`
- 400 error
```
<html>
<head><title>400 Bad Request</title></head>
<body bgcolor="white">
<center><h1>400 Bad Request</h1></center>
</body>
</html>
```
- 403 error (AWS WAF blocked)
```
<html>
<head><title>403 Forbidden</title></head>
<body bgcolor="white">
<center><h1>403 Forbidden</h1></center>
</body>
</html>
```
- When `Stickiness` is turned on 
`Set-Cookie: AWSALB=HCfc9WL09fNBfzI+jcw5U/1QSnQT5TmeFuESVjI3WPIMQHPR9NKgaQzxufDwAhowY6p5dn80s4dn2vP/7iN4UwCkqdrrHP2ALFlQaUdrn1GTF3Zg1xK2ZhAqHg68`

### Absolute-URI
- supports Absolute-URI with higher priority under host header
- any scheme in Absolute-URI
- doesn't like @ in Absolute-URI

### Listener Rules
- path-based (*- any)
  - /lala/* -> target2/lala/
  - case-sensitive
  - parses, url-decodes, path-normalize (partly normalize `//`)
  - still, it forwards the initial path (?)
- host-based
  - case-insensitive
  - takes first Host header or Absolute URI value
  - skips port part

- It can:
  - Return fixed response
  - Forward
  - Redirect

### Vuln config
- Misrouting  `/lala2///../xss.php` (but `/lala2//../xss.php` doesn't work)
`/lala2/* -> target2/lala/`

- Bypass path rule `//lala1/`
`/lala1/* -> target1/lala/`

# AWS WAF 
- with ELB (URI type rule)
  - it applies rules on unprocessed path (does include query)
  - only zero or one transofrmation is allowed (url decode or low case)
  - Bypass `starts with /login` from https://aws.amazon.com/waf/faq/ - `//login`

# AWS CloudFront
## Basics
- routing depends on Host-header (not SNI)
- case-sensitive for verb (400 error)
- doesn't allow `%2f` as the first slash (400)
- doesn't allow `/../` higher the root (400)
- doesn't allow in the path: `%00 0x00` (`%` is allowed only in the end of path)
- doesn't normalize /..
- normalizes //, but forwards the initial path (with exception above)
- `%0a` doesn't cut the path
- set HTTP/1.1 to the origin 
- it partly supports HTTP/0.9 (proxy forwards the request, but doesn't return the response from a server)
  - use Absolute-URI (due to Host header routing )
- allows >1 `Host` header
  - forwards only the first one
- forward headers with space symbols in name
  - ` AnyHeader:` -> ` AnyHeader:`,
  - `AnyHeader :`-> `AnyHeader:`
- adds headers to request to origin: `X-Amz-Cf-Id: , User-Agent: , Via: , X-Forwarded-For: `
  - we can send our values in `X-Forwarded-For:, Via: `  and it will be added to the forwarded header (`examplezzz.com, example2.com`)
  - doesn't allow 0x0d in value (400)
- it allows/forwards `_` in header name (`X_Forwarded_Port`)
- doesn't forward Cookie, but can be bypassed with `Cookie :` (space)
- forward unprocessed path (but cuts off the fragment part)
  - ``/!"$&'()*+,-./:;<=>@[\]^_`{|}~a#z%``  -> ``/!"$&'()*+,-./:;<=>@[\]^_`{|}~a``
  - `%01-%FF` -> `%01-%FF`
- `/aaa aaa/` - this combination (space) changes how CF works
  - CF forwards the processed path
  - processed path is used as a cache key
- it deletes spaces
  - `/lala1/aa/as http/1.11 ?` -> `GET /lala1/aa/ashttp/1.11 HTTP/1.1`
- TRACE is not allowed (405)
- `Origin Path` - CF appends the path to this value 
  
## Absolute-URI
- supports Absolute-URI, but with lower priority than host header
- any scheme in Absolute-URI
- doesn't like @ in Absolute-URI

## Fingerprint
- Headers
```
X-Cache: Miss from cloudfront
Via: 1.1 d2625240b33e8b85b3cbea9bb40abb10.cloudfront.net (CloudFront)
X-Amz-Cf-Id: I5olhEiuAzfTiLWKpztI_EVwj0L-ZPbFF4Avev98ytlEsAyQUuMklg==
```
- 400 error
```
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML><HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">
<TITLE>ERROR: The request could not be satisfied</TITLE>
</HEAD><BODY>
<H1>400 ERROR</H1>
<H2>The request could not be satisfied.</H2>
<HR noshade size="1px">
Bad request.

<BR clear="all">
<HR noshade size="1px">
<PRE>
Generated by cloudfront (CloudFront)
Request ID: D5IaOJeKch31FI0FCz3Q4WqAkGt3jF_7Ka8i1UR1WZujefb5t5icrg==
</PRE>
<ADDRESS>
</ADDRESS>
</BODY></HTML>
```
- 403 error (AWS WAF blocked)
```
``` 
- adds headers to req to the origin server (by default):
```
X-Amz-Cf-Id: ZvMe27mnOtLdMtvZG014LKfNITRcHFEVskqE_U-Znjs9EaYw0n_NKg==
User-Agent: Amazon CloudFront
Via: 1.1 c76a5a41a8483a9e5dcccdfeb87a16ca.cloudfront.net (CloudFront)
X-Forwarded-For: 213.217.243.126
```

## Caching
https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html

- Forward Cookies - None (doesn't forward cookie header) / Whitelist / All
- Query String Forwarding - None (doesn't forward query) / Whitelist (forwards all, cache whitelisted) / All

- caches GET and HEAD requests (default)
- it respects the response Cache-Control (no-cache, no-store, private, max-age, s-maxage) and Expires 
- Status codes cached: 200, 3xx, 400, 403, 404, 405, 414, 500, 501, 502, 503, 504
- `206` trick doesn't work
- Does not honor the Pragma and the client's Cache-Control 
- Doesn't care about `Vary` header
- key for cache: host header (?) and path (without fragment)
- If you set the TTL for a particular origin to 0, CloudFront will still cache the content from that origin. It will then make a GET request with an If-Modified-Since header, thereby giving the origin a chance to signal that CloudFront can continue to use the cached content if it hasn’t changed at the origin.
- Minimum TTL overrides a value of the Cache-Control response header

- Cache Behavior `images/*.jpg`
  - `/images` == `images`, but `/lala/images` != `images`
  - rules are applied to processed path (urldecoded, normalized), but sends to the origin partly processed
    - `///images` 
    - `/lala/../images/`
    - `/%69mages`

### Possible misusing
- CF + WL /something/index.jsp;//../../images/////../1.jpg
- CF + Apache/PHP /coco//index.php///../../images.jpg (?)
- CF + Flask /endpoing/something_with*///../../images.jpg (?)

### Caching detections
- X-Cache: Hit from cloudfront (Miss from cloudfront) - shows caching
- Age: \d - for cached objects 
