- https://github.com/jiangwenyuan/nuster
- Based on [Haproxy](haproxy)
- Tested version:

## Caching
- default key of CACHE: method.scheme.host.uri
- default key of NoSQL: GET.scheme.host.uri
  - `http://www.example.com/q?name=X&type=Y -> GET.http.www.example.com./q?name=X&type=Y`
- only 200 response is cached
- doesn't respect Cache-Control, Expire headers
- Does not honor the Pragma and the client's Cache-Control 