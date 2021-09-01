- https://traefik.io/
- Tested version: 1.7

## Basics
- backend (URL to origin) is uncontrollable 
- doesn't care about the verb 
- doesn't support TRACE
- doesn't support  Max-Forwards
- doesn't support HTTP/0.9
- set HTTP/1.1 for the backend by default
- doesn't allow >1 `Host` header (`400 Bad Request: too many Host headers`)
- doesn't allow 0x0d in header value
- adds headers to the request to origin: `X-Forwarded-For`, `X-Forwarded-Host`, `X-Forwarded-Port`,` X-Forwarded-Proto`, `X-Forwarded-Server`, `X-Real-Ip`
  - if we send our headers with the same names (`X-Forwarded-Host`, `X-Forwarded-Port`,` X-Forwarded-Proto`, `X-Real-Ip`), we overrides values of proxy's request
  - in case of `X-Forwarded-For`, it will be added to proxy's request (`examplezzz.com, example2.com`)
  - in case of `X-Replaced-Path` (see below), there will be two header with `X-Replaced-Path` name
- forwards headers with underscore `_` in name
- forwards headers with trailing space, but deletes the space (`AnyHeader :`->`AnyHeader:`)
- support line folding for headers (` Header:zzz`-> it is concatenated with the previous header)
- doesn't allow `%2f` as the first slash. It must be `/` or `*` only
- doesn't allow space (` `) in the path
- doesn't normalize the path
- url decodes before applying matchers, forwards url encoded version to backend
- ``/!"$&'()*+,-./:;<=>@[\]^_`{|}~#?``  -> ``$&+,s-./:;=@_~?``, `%21%22%27%28%29%2A%3C%3E%5B%5C%5D%5E%60%7B%7C%7D%23`
- `0x00-0x19` -> `%00-%19`,  >`0x80` -> >`%80`
- `%00-%FF` -> `%00-%FF`

## Fingerprint
- no specific headers
- 400 error
```
400 Bad Request
```
`Host: /` -> `400 Bad Request: malformed Host header`
## Absolute-URI
- supports Absolute-URI with higher priority under host header
- any scheme in Absolute-URI
- allows `@` in Absolute-URI

## Matchers and Modifiers
- Use `Path` if your backend listens on the exact path only (allows query string)
- Use a `*Prefix*` (`PathPrefix`) matcher if your backend listens on a particular base path but also serves requests on sub-paths
- Use a `*Strip` (`PathPrefixStrip`) matcher if your backend listens on the root path (`/`) but should be routeable on a specific prefix
- `AddPrefix`: /products: Add path prefix to the existing request path prior to forwarding the request to the backend.
- `ReplacePath`: /serverless-path: Replaces the path and adds the old path to the X-Replaced-Path header. Useful for mapping to AWS Lambda or Google Cloud Functions.
- `ReplacePathRegex`: ^/api/v2/(.*) /api/$1: Replaces the path with a regular expression and adds the old path to the X-Replaced-Path header. Separate the regular expression and the replacement by a space.

https://docs.traefik.io/basics/#modifiers

# HTTP/2
- Tested version - 1.7.30
- **Header Names:**

    Allowed:``-|^.'_~`+!#$%&*``

    Restricted(from \x00-\x20):`\x00-\x20` 

    Only in lower case

- **Header Value:**

    Allowed(\x00-\x20):`\x09 \x20`

    Allowed:``[]{}:;.,<>?|"\'/^_`=+~!@#$%&*()-``

- **Verb:**

    Allowed:`-.|'^_`+~!#$%^&*`

    Restricted(\x00-\x20):`\x00-\x20`

    Any case allowed

- **Path:**

    Must start with `/`

    Allowed:``[]{}:;.,<>?|"\'/_`=+~!@#$%^&*()-`` 

    Restricted(\x00-\x20): `\x00-\x19` (`\x20` → `%20`)

    supports **Absolute URI** http://evilhost.com/pathtest →`GET /pathtest HTTP/1.1`

    doesn't rewrite `Host`
- **Authority:**

    Allowed:``[]{};.,<>?|"'\/_`=+~!@#$%^&*()-``

    Restricted(\x00-\x20): except`\x09 \x20`

    `host` is allowed, but doesn't rewrite `:authority`/`Host`

- **Scheme:**

    Strict list of values: `http` `https` (more?)
