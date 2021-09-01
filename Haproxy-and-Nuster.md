- http://www.haproxy.org/
- Tested version - 1.8.14-52e4d43
- https://github.com/jiangwenyuan/nuster

## Basics
- case-insensitive for verb
- allows any path/query values (except 0x00-0x20, >0x80): 
  - `GET !i?lala=#anything HTTP/1.1`
- doesn't url-decode and normalize the path before applying rules
- support converters:
  - url_dec - url decodes (but sends undecoded to origin server), but spoils path_begin
- path_* extracts the path, which starts at the first slash and ends before the first question mark 
- allows >1 `Host:`
  - forwards all of them
- doesn't forward `AnyHeader :` - 400 error
- support line folding for headers (` Header:zzz`-> concatenate with previous header)
- no additional headers to backend

## Fingerprint
- no special headers
- 400 error:
```
<html><body><h1>400 Bad request</h1>
Your browser sent an invalid request.
</body></html>
```
- 403 error:
```
<html><body><h1>403 Forbidden</h1>
Request forbidden by administrative rules.
</body></html>
```

## Absolute-URI
- doesn't support (parse) Absolute-URI
- forwards it as is
  - `GET http://backend.com/q?name=X&type=Y HTTP/1.1` -> `GET http://backend.com/q?name=X&type=Y HTTP/1.1`

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

# HTTP/2
- Tested version - 2.4.0
- **Header Names:**

    Allowed:``-.|'^_`+~!#$%^&*``

    Restricted(from \x00-\x20):`\x00-\x20` (protocol error)

    Restricted(\x7F-\xFF):`\x7F-\xFF` (protocol error)

    Only in lower case

- **Header Value:**

    Restricted(\x00-\x20):`\x00 \x0a \x0d`

    Allowed:``[]{}:;.,<>?|"'\/^_`=+~!@#$%^&*()-``

- **Verb:**

    Allowed:``[]{}:;.,<>?|"'\/^_`=+~!@#$%^&*()-``

    Restricted(\x00-\x20):`\x00 \x0a \x0d`

    Any case allowed

    No value allowed

- **Path:**

    Allowed:``[]{}:;.,<>?|"'\/^_`=+~!@#$%^&*()-``

    Restricted(\x00-\x20):`\x00-\x20` (`\x00 \x0a \x0d` - protocol error)

    It cuts prefix:`anything/path` → `/path`

    - doesn't support Absolute URI
- **Authority:**

    Allowed:``[]{}:;.,<>?|"'\/^_`=+~!@#$%^&*()-`` 

    Restricted(\x00-\x20):`\x00-\x20` (`\x00 \x0a \x0d` - protocol error)

    `host` rewrites `:authority`

    No value allowed

- **Scheme:**

    Allowed:``[]{}:;.,<>?|"'\/^_`=+~!@#$%^&*()-`` 

    Restricted(\x00-\x20):`\x00-\x20` (`\x00 \x0a \x0d` - protocol error)

    `:scheme` adds before `:authority` and `:path`:

    - `:scheme:https\x3a//localhost/admin?` → `GET https://localhost/?://lab.io/testhere66idhere HTTP/1.1`

    No value → `GET ://lab.io/testhere1idhere HTTP/1.1`

    It applies rules after concatenation `:scheme` `:authority` `:path`
