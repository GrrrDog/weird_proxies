# Stackpath
- Tested version: in the beginning of 2019

## Basics
- similar to [Nginx](Nginx.md)
- doesn't allow in the path: `%00 0x00 % space`
- doesn't allow `%2f` as the first slash (400)
- doesn't allow `/../` higher the root (400)
- doesn't allow `/../` or `%2f%2e%2e%2f` (403, WAF)
- doesn't normalize `/..`, `/./`
- normalizes `//` to `/` 
- `%0a` doesn't cut the path
- it forwards the normalized path
 - ``/!"$&'()*+,-./:;<=>@[\]^_`{|}~?a#z`` -> ``/!"$&'()*+,-./:;<=>@[\]^_`{|}~?a#z``
  - `%01-%FF` -> `%01-%FF`
- strict case-sensitive list of verbs: OPTIONS,GET,HEAD,POST
- doesn't support TRACE
- doesn't support Max-Forwards
- doesn't support HTTP/0.9
- set HTTP/1.1 for the backend by default
- doesn't allow >1 `Host` header
- adds headers to the request to origin: `X-Forwarded-For`, `x-sp-edge-host`, `x-sp-edge-scheme`,`x-fb-host`, `x-sp-forwarded-ip`
   - in case of `X-Forwarded-For`, it will be added to proxy's request (`examplezzz.com, example2.com`)
   - doesn't allow to overide `x-sp-edge-host`, `x-sp-edge-scheme`,`x-fb-host`, `x-sp-forwarded-ip`
- forwards headers with underscore `_` in name 
- doesn't forward headers with trailing space `Header :zzz`
- support line folding for headers (` Header:zzz`-> it is concatenated with the previous header)
- automatically adds `Access-Control-Allow-Origin: *` to all responses by default(?)

## Absolute-URI 
- supports Absolute-URI with higher priority under host header
- any scheme in Absolute-URI
- doesn't allow `@` in Absolute-URI

## Fingerprint 
- Headers
```
Server: fbs
X-HW: 1552411092.cds068.fr8.h2,1552411092.cds028.fr8.sc,1552411092.cdn2-wafbe03-fra1.stackpath.systems.-.wx,1552411092.cds028.fr8.p
Set-Cookie: SPSI=1bf36dd5f9856283ece2beb57e430268; Path=/
Set-Cookie: spcsrf=6781b2b0cb8ad015471150714fe5e9a7; Expires=Tue, 12-Mar-19 19:19:15 GMT; Path=/; HttpOnly; SameSite=Strict
Set-Cookie: adOtr=obsvl; Expires=Thu, 2 Aug 2001 20:47:11 UTC; Path=/
Set-Cookie: UTGv2=D-h4b6fb871b7fdfabdd42b406a4db100f3671; Expires=Wed, 11-Mar-20 17:19:15 GMT; Path=/
```
- 400 error
```
HTTP/1.1 400 Bad Request
```

- 403
```
<h1>StackPath</h1> <hr> <h2>Sorry, you have been blocked.</h2>
```

## Caching
- key is normalized (without `//` and Absolute-URI) case-insensitive path and host (?)
- includes query string (`Standart` behaviour)
  - https://support.stackpath.com/hc/en-us/articles/360001212783-CDN-Caching-Explained
- it caches depending on extension (`.zip,.js,.css,.webp,.doc,.csv,.pdf,.pls,.ls,.ppt,.ps,.class,.jar,.swf,.ejs,.fav,*.*ls,*.*ls*,.txt,.m3u8,.jpg,.jpeg,.gif,.ico,.png,.bmp,.pict,.tif,.tiff,.webp,.eps,.ttf,.eot,.woff,.woff2,.otf,.svg,.svgz,mp4,.m4a,.m4v,.mov,.ts,.wav,.mp3,.wma,.ogg,.midi,.mid`)
- it also check Content-Type for some extensions
- doesn't cache files in Webpage root (?)
- honors on Cache-Control from response
- honors the Vary header from the response (default)
- Supports `Range` for forwarded and cached values
- Returns full response for `206` 
- adds `Expires:` and `Pragma: no-cache` for the response which is not cached
- Doesn't add `Set-Cookie` to the cached values
- with `Edge rules` it's possible to cache anything (even with restrictive Cache-Control)
- Edge rules
  - https://support.highwinds.com/customer/en/portal/articles/2558868-filters?b_id=15425
  - are applied on urlencoded value
  - case sensitive

### Caching detection
- Doesn't cache `Date` header
- `1552582220.cds081.fr8.h2,1552582220.cds063.fr8.sc,1552582220.cdn2-wafbe03-fra1.stackpath.systems.-.wx,1552582220.cds063.fr8.p` or `1552582977.cds061.fr8.h2,1552582977.cds053.fr8.c`
  - `p` 	Indicates the request was proxied from the origin. 
  - `c` -	Indicates the request was served from cache.
