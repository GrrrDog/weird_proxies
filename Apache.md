- https://httpd.apache.org/
- Tested version: 2.4

## Basics
- case-sensitive for verb  (`get != GET`)
  - insensitive with PHP
- treats // as a directory (`/images/1.jpg/..//../2.jpg` -> `/images/2.jpg`)
- doesn't allow in path: `# %`
- doesn't allow `%2f` in path (default config: `AllowEncodedSlashes Off`)
  - %2f is always 404 (`/%2f/../index.php/` or `/index.php/%2f`)
- can be the forward-proxy
- support this request (points to root) `GET ? HTTP/1.1`
- cares about cache check headers (If-Range/Match/*) 
  - doesn't care in case of PHP
- If-Range + Range -> returns part of content only if If-Range correct
- No `Accept-Ranges: bytes` in case of php

### Fingerprint
- `Server: apache`

### Absolute-URI
- supports Absolute-URI with higher priority under host header
- any scheme in Absolute-URI
- doesn't like @ in Absolute-URI

## Location match rules (the same works for ProxyPass)
http://httpd.apache.org/docs/current/mod/core.html#location
- Every type is case-sensitive
- `<Directory>`
Is used to enclose a group of directives that will apply only to the named directory, sub-directories of that directory, and the files within the respective directories. Any directive that is allowed in a directory context may be used. Directory-path is either the full path to a directory, or a wild-card string using Unix shell-style matching. In a wild-card string, ? matches any single character, and * matches any sequences of characters. You may also use [] character ranges. 

- `<Location "/private1">`
The specified location matches exactly the path component of the URL.
The specified location, which ends in a forward slash, is a prefix of the path component of the URL (treated as a context root). The specified location, with the addition of a trailing slash, is a prefix of the path component of the URL (also treated as a context root).
  - `/private1` -> `/private1`, `/private1/` and `/private1/file.txt`
  - `/private2/` ->  `/private2/` , `/private2/file.txt`

- The `<LocationMatch>` directive and the regex version of `<Location>` require you to explicitly specify multiple slashes if that is your intention.
  - `<LocationMatch>` ==  `<Location ~ "/(extra|special)/data"> `
  - Location with support of RegExps
  - `<LocationMatch "^/abc">` would match the request URL `/abc` but not the request URL `//abc`. The (non-regex) `<Location>` directive behaves similarly when used for proxy requests. But when (non-regex) `<Location>` is used for non-proxy requests it will implicitly match multiple slashes with a single slash. For example, if you specify `<Location "/abc/def">` and the request is to `/abc//def` then it will match.
- FilesMatch and Files to set rules for extensions, but works for only inside current location (`<FilesMatch \.php$>` in virt host -> `/test.php` - OK,  `/anything/test.php` - no)

### ProxyPass
- backend (URL to origin) is controllable 
- parses, url-decodes, normalizes, finds location, url-encodes
  - /.. - > /../
  - // -> // (except the first / symbol)
    - `//path` -> `/path`
    - `/path//` -> `/path//`
- doesn't allow >1 `Host` header
- doesn't forward with trailing space `AnyHeader :`
- support line folding for headers (` Header:zzz`-> concatenate with previous header)
- adds headers to request to origin: `X-Forwarded-For: , X-Forwarded-Host: , X-Forwarded-Server: `
  - we can send our values in request and it will be added to proxy's request (`examplezzz.com, example2.com`)
- adds Content-Type depending on extension, if there is no CT from origin server

### Rewrite
- flags https://httpd.apache.org/docs/2.4/rewrite/flags.html
- similar to ProxyPas, but:
- url decodes values, flag B encode them again
- urldecodes, normalizes, then put in url and parse it
  - `%3f` decoded to `?`, but `%3faa=1?bb=2 -> ?aa=1`
  - inside (.*), `/lala/path/%2e%2e -> /path/..` (it's not normalized, but `/path/%2e%2e/` - is)
```
<VirtualHost *:80>
  ServerName example1.com
    RewriteEngine On
    RewriteRule /lala/(.*)  http://192.168.78.111:9999/$1 [P,L]
</VirtualHost>
```


## Vulnerable configs
- multiple / bypass  
  - `http://lab.io:8080/asdasd/..///../neighborhood/a/feed -> //neighborhood/a/feed`
```
RewriteEngine On
RewriteCond %{REQUEST_URI} ^/neighborhood/[^/]+/feed$ [NC]
RewriteRule ^.*$ - [F,L]
```

- No ending slash SSRF (incorrect config)
  - `/@evil.com/index.php`
  - `/.evil.com/index.php`
```
<VirtualHost *:80>
  ServerName example0.com
  ProxyPass / http://192.168.78.111
</VirtualHost>
```

## Caching
not tested
