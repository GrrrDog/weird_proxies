# Caddy
https://caddyserver.com
- Tested version: v2.4.0

## Basics
- case-insensitive for verbs (?)
- doesn't support HTTP/0.9
- set HTTP/1.1 for the backend by default
- doesn't support Max-Forwards

## Headers
- doesn't allow >1 `Host` header if it has a strict list of values (returns `400 Bad Request: too many Host headers`)
- allow multiple headers with the same name (it forwards all of them keeping the order)
- allow underscore (`_`) in the header name (including fastcgi)
- doesn't allow 0x00-0x1f, 0x7f
- support line folding for headers (` Header:zzz`-> it is concatenated with the previous header)
- adds headers to the request to the back end: `x-forwarded-proto`,  `x-forwarded-for`
  - allow to rewrite `x-forwarded-proto` header
  - in case of `x-forwarded-for`, it will be added to proxy's request (`examplezzz.com, example2.com`)
- doesn't allow rewriting of headers set by RP (`header_up`) 

## Absolute-URI
- supports Absolute-URI with higher priority under host header
- only supporting scheme in Absolute-URI
  - https sends https to backend (?)
- doesn't allows `@` in Absolute-URI

## Req processing
- doesn't normalize the path
- case-insensitive  (it depends on a matcher/directive)
- urldecode the path before applying rules (it depends on a matcher/directive)
  - path, file, respond - urldecoded 
  - route - not urldecoded
- no req splitting from proxy to origin/crlf inj
  - path, file, dir - decodes %0a%0d to \r\n, but they are urlencoded or coverted to whitespaces on "output"
- ``/!"$&'()*+,-./:;<=>@[\]^_`{|}~#?a#a``  -> ``/%21%22$&%27%28%29%2A+,-./:;%3C=%3E@%5B%5C%5D%5E_%60%7B%7C%7D~%23?a#a``
- `%00-%FF` -> `%00-%FF`
- some symbols changes logic how caddy forwards urlencoded path
  - symbols(may be more): ```"{|}`^\<>#```
  - `/%00%01%02%03%04%05%06%07%08%09%0b%0c%0d%0e%0f%10%11%12%13%14%15%16%17%18%19%1a%1b%1c%1d%1e%1f%20%21%22%23%24%25%26%27%28%29%2a%2b%2c%2d%2e%30%31%32%33%34%35%36%37%38%39%3a%3b%3c%3d%3e%3f%40%41%42%43%44%45%46%47%48%49%4a%4b%4c%4d%4e%4f%50%51%52%53%54%55%56%57%58%59%5a%5b%5c%5d%5e%5f%60%61%62%63%64%65%66%67%68%69%6a%6b%6c%6d%6e%6f%70%71%72%73%74%75%76%77%78%79%7a%7b%7c%7d%7e%7f%80%81%82%83%84%85%86%87%88%89%8a%8b%8c%8d%8e%8f%90%91%92%93%94%95%96%97%98%99%9a%9b%9c%9d%9e%9f%a0%a1%a2%a3%a4%a5%a6%a7%a8%a9%aa%ab%ac%ad%ae%af%b0%b1%b2%b3%b4%b5%b6%b7%b8%b9%ba%bb%bc%bd%be%bf%c0%c1%c2%c3%c4%c5%c6%c7%c8%c9%ca%cb%cc%cd%ce%cf%d0%d1%d2%d3%d4%d5%d6%d7%d8%d9%da%db%dc%dd%de%df%e0%e1%e2%e3%e4%e5%e6%e7%e8%e9%ea%eb%ec%ed%ee%ef%f0%f1%f2%f3%f4%f5%f6%f7%f8%f9%fa%fb%fc%fd%fe%ff^` -> `/%00%01%02%03%04%05%06%07%08%09%0B%0C%0D%0E%0F%10%11%12%13%14%15%16%17%18%19%1A%1B%1C%1D%1E%1F%20%21%22%23$%25&%27%28%29%2A+,-.0123456789:;%3C=%3E%3F@ABCDEFGHIJKLMNOPQRSTUVWXYZ%5B%5C%5D%5E_%60abcdefghijklmnopqrstuvwxyz%7B%7C%7D~%7F%80%81%82%83%84%85%86%87%88%89%8A%8B%8C%8D%8E%8F%90%91%92%93%94%95%96%97%98%99%9A%9B%9C%9D%9E%9F%A0%A1%A2%A3%A4%A5%A6%A7%A8%A9%AA%AB%AC%AD%AE%AF%B0%B1%B2%B3%B4%B5%B6%B7%B8%B9%BA%BB%BC%BD%BE%BF%C0%C1%C2%C3%C4%C5%C6%C7%C8%C9%CA%CB%CC%CD%CE%CF%D0%D1%D2%D3%D4%D5%D6%D7%D8%D9%DA%DB%DC%DD%DE%DF%E0%E1%E2%E3%E4%E5%E6%E7%E8%E9%EA%EB%EC%ED%EE%EF%F0%F1%F2%F3%F4%F5%F6%F7%F8%F9%FA%FB%FC%FD%FE%FF%5E`
- doesn't forward raw bytes (0x00-0x20, %, 0x7f) in path (400 error)

## Fingerprint
- Additional headers
```
Server: Caddy
```
- 400 error
```
HTTP/1.1 400 Bad Request: too many Host headers
Content-Type: text/plain; charset=utf-8
Connection: close

400 Bad Request: too many Host headers
```
- 404 error
```
HTTP/1.1 404 Not Found
Content-Type: text/plain; charset=utf-8
X-Content-Type-Options: nosniff
Date: Wed, 19 May 2021 15:07:05 GMT
Content-Length: 19
Connection: close

404 page not found
```
- 505 error
```
HTTP/1.1 505 HTTP Version Not Supported: unsupported protocol version
Content-Type: text/plain; charset=utf-8
Connection: close

505 HTTP Version Not Supported: unsupported protocol version
```

## Matchers and Modifiers
- case sensitive (by default)
- `prefix`  the prefix must match the beginning of the :path header.
- `path` the path must exactly match the :path header once the query string is removed.
- `safe_regex` the regex must match the :path header once the query string is removed
- `prefix_rewrite` the matched prefix (or path) should be swapped with this value
- `regex_rewrite` portions of the path that match the pattern should be rewritten, even allowing the substitution of capture groups from the pattern into the new path as specified by the rewrite substitution string -->

### vuln config
! Bypass //blocked/  /./blocked/ paths (Apache as the backend)
```
@notblacklisted {
    not {
        path /blocked* 
    }
}
reverse_proxy  @notblacklisted 192.168.78.111:9999
```

! Misrouting
`GET /prefix3/http://absoluteuri.hosthere/path HTTP/1.1` -> `GET http://absoluteuri.hosthere/path HTTP/1.1`
```
route /prefix3/* {
    uri strip_prefix /prefix3/
    reverse_proxy 192.168.78.111:9999
    }
```

# HTTP/2
- Tested version - 2.4.0
- **Header Names:**

    Allowed:``-.|'^_`+~!#$%^&*``

    Restricted(from \x00-\x20):`\x00-\x20` 

    Only in lower case

- **Header Value:**

    Allowed(\x00-\x20):`\x09 \x20`

    Allowed:``[]{}:;.,<>?|"\'/^_`=+~!@#$%^&*()-``

- **Verb:**

    Allowed:``-.|'^_`+~!#$%^&*``

    Restricted(\x00-\x20):`\x00-\x20`

    Any case allowed

- **Path:**

    Must start with `/`

    Allowed:``[]{}:;.,<>?|"\'\\/^_`=+~!@#$%^&*()-`` 

    Restricted(\x00-\x20): `\x00-\x19` (`\x20` → `%20`)

    supports **Absolute URI** http://evilhost.com/pathtest →`GET /pathtest HTTP/1.1`

    doesn't rewrite `Host`
- **Authority:**

    Allowed:``[]{};.,<>?|"'\/_`=+~!@#$%^&*()-``

    Restricted(\x00-\x20): except`\x09 \x20`

    `host` is allowed, but doesn't rewrite `:authority`/`Host`

- **Scheme:**

    Strict list of values: `http` `https` (more?)
