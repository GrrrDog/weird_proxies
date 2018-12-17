- http://www.haproxy.org/
- Tested version - 1.8
- https://github.com/jiangwenyuan/nuster
- Tested version:

## Basics
- case-insensitive for verb (get == GET)
- allows any path/query values (except 0x00-0x20, >0x80): 
  - `GET !i?lala=#anything HTTP/1.1`
- doesn't url-decode, normalize the path before applying rules
- support converters:
  - url_dec - url decodes (but send undecoded to origin server), but spoils path_begin
- path_* extracts the path, which starts at the first slash and ends before the question mark 
- allows >1 `Host:`
- doesn't resend `AnyHeader :` - 400 error
- support line folding for headers (` Header:zzz`-> concatenate with previous header)
- no additional headers to backend

## Fingerprint
- no
- 400 error:

## Absolute-URI
- doesn't support Absolute-URI
- forwards it as is

## Caching
Cache's been partly implemented in this version of HAproxy. It was not tested. [Nuster](https://github.com/jiangwenyuan/nuster) was tested instead

- default key of CACHE: method.scheme.host.uri
- default key of NoSQL: GET.scheme.host.uri
  - `http://www.example.com/q?name=X&type=Y -> GET.http.www.example.com./q?name=X&type=Y`
- only 200 response is cached
- doesn't respect Cache-Control, Expire headers from the origin
- Does not honor the Pragma and the client's Cache-Control 

## Vulnerable configs
- Bypass `//admin/` `/Admin/` `/%61dmin/`
```
acl restricted_page path_beg /admin
```
- Bypass `/log/` - any trailing symbol (e.g. /)
```
acl restricted_page path_beg,url_dec  /log
```