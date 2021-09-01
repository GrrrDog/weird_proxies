# Envoy
https://www.envoyproxy.io/
- Tested version: v1.14.4

## Basics
- case-sensitive for verbs
- doesn't support HTTP/0.9
- set HTTP/1.1 for the backend by default
- doesn't support Max-Forwards

## Headers
- doesn't allow >1 `Host` header if it has a strict list of values (returns 404)
- allow >1 `Host` header if `domains: ["*"]` (values concatinated `Host: hostheadervalue1,hostheadervalue2`)
  - the same for `Origin`, but not for all headers
- allow multiple headers with the same name (it forwards all of them keeping the order)
- allow underscore (`_`) in the header name (if no `headers_with_underscores_action`)
- adds headers to the request to the back end (`use_remote_address: false`): `x-forwarded-proto`, `x-request-id`, `x-envoy-expected-rq-timeout-ms:`
  - allow to rewrite `x-request-id` and `x-forwarded-proto` headers 
- adds headers to the request to the back end (`use_remote_address: true`): `x-forwarded-for`, `x-envoy-external-address`, `x-forwarded-proto`, `x-request-id`, `x-envoy-expected-rq-timeout-ms:`
  - in case of `x-forwarded-for`, it will be added to proxy's request (`examplezzz.com, example2.com`)
- adds `x-envoy-original-path` if `prefix_rewrite` or `regex_rewrite` is used
- it converts req header names to lower case before sending to the back end server (`User-Agent:` -> `user-agent:`)
- before <1.9.1 (CVE-2019-9900), it allows Null byte in headers (https://github.com/envoyproxy/envoy/blob/master/security/postmortems/cve-2019-9900.md)

## Req processing
- doesn't normalize the path (depends on configuration)
- ``/!"$&'()*+,-./:;<=>@[\]^_`{|}~#?a``  -> ``/!"$&'()*+,-./:;<=>@[\]^_`{|}~#?a``
- `%00-%FF` -> `%00-%FF`
- doesn't urldecode the path before applying rules (depends on configuration)
- doesn't forward raw bytes (0x01-0x20, > 0x80) in path (400 error)
- before <1.9.1 (CVE-2019-9901), it doesn't normalize path (https://github.com/envoyproxy/envoy/blob/master/security/postmortems/cve-2019-9900.md)

## Absolute-URI
- supports Absolute-URI with higher priority under host header
- any scheme in Absolute-URI
- allows `@` in Absolute-URI

## Fingerprint
- Some headers are changed to lower case
- Additional headers
```
server: envoy
x-envoy-upstream-service-time: 33
```
- 400 error
```
HTTP/1.1 400 Bad Request
content-length: 0
connection: close
```
- 404 error
```
HTTP/1.1 404 Not Found
date: Mon, 13 Jul 2020 09:15:24 GMT
server: envoy
connection: close
content-length: 0
```

### vuln config
! Bypass //cors/disabled/ //Cors/disabled/ /%63ors/disabled/
https://www.envoyproxy.io/docs/envoy/latest/start/sandboxes/cors (with Apache as the backend)

```yaml
- match:
    prefix: "/cors/disabled"
  route:
    cluster: backend_service
    cors:
      filter_enabled:
        default_value:
          numerator: 0
          denominator: HUNDRED
```

! "Bypass" rev proxy-based auth if username passes in headers to the backend
https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_authz_filter (with Apache as the back end)
`x-current-user: asdasd\r\nx-current-user: ADMIN` -> `x-current-user: User_from_ext_auth\r\nx-current-user: ADMIN`
```

```yaml
- name: envoy.filters.http.ext_authz
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz
    http_service:
      server_uri:
        uri: ext_authz
        cluster: ext_authz-http-service
        timeout:  0.250s
      authorization_response:
        allowed_upstream_headers:
          patterns:
          - exact: x-current-user
```

# HTTP/2
- Tested version - 1.18.3

- **Header Names:**

    Allowed:``-|^.'_~`+!#$%&*``

    Restricted(from \x00-\x20):`\x00-\x20` 

    Only in lower case

- **Header Value:**

    Restricted(\x00-\x20):`\x00 \x0a \x0d`

    Allowed:``[]{}:;.,<>?|"\'/_`=+~!@#$%^&*()-``

- **Verb:**

    Allowed:``[]{};.,<>?|"'\/_`=+~!@#$%^&*()-``

    Restricted(\x00-\x20): except`\x09 \x20`

- **Path:**

    Must start with `/`

    Allowed:``[]{}:;.,<>?|"\'/_`=+~!@#$%^&*()-``

    Restricted(\x00-\x20): except`\x09 \x20` (encoded)

    doesn't support **Absolute URI**

- **Authority:**

    Allowed:``[]:;.,'_=+~!@$%&*()-`` 

    Restricted(\x00-\x20):`\x00-\x20`

    `host` is allowed, it's concat with `:authority` 

    - `:authority:lab.io` `host:evilhost.com` → `host: lab.io,evilhost.com`
- **Scheme:**

    Allowed:``+.-`` 

    Restricted(\x00-\x20):`\x00-\x20`

    Doesn't proxy`scheme`
