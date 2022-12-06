# Weird Proxies

It's a cheat sheet about behaviour of various reverse proxies and related attacks.

It is a result of analysis of various reverse proxies, cache proxies, load balancers, etc.
The article (https://www.acunetix.com/blog/articles/a-fresh-look-on-reverse-proxy-related-attacks/) describes the goals of the research and how you can use the cheat sheet.
 
Analyzed stuff:
- [Nginx](Nginx.md)
- [Apache](Apache.md)
- [Haproxy/Nuster](Haproxy-and-Nuster.md)
- [Varnish](Varnish.md)
- [Traefik](Traefik.md)
- [Envoy](Envoy.md)
- [Caddy](Caddy.md)
- [AWS](AWS.md)
- [Cloudflare](Cloudflare.md)
- [Stackpath](Stackpath.md)
- [Fastly](Fastly.md)

Additional:
- [Test Labs](labs)

Related articles/white papers/presentations:
- [Reverse proxies & Inconsistency](https://speakerdeck.com/greendog/reverse-proxies-and-inconsistency)
- [Weird proxies/2 and a bit of magic](https://speakerdeck.com/greendog/2-and-a-bit-of-magic)
- [Attacking Secondary Contexts in Web Applications](https://docs.google.com/presentation/d/1N9Ygrpg0Z-1GFDhLMiG3jJV6B_yGqBk8tuRWO1ZicV8/mobilepresent?slide=id.p)
- [Hacking Starbucks and Accessing Nearly 100 Million Customer Records](https://samcurry.net/hacking-starbucks/)
- [Middleware, middleware everywhere - and lots of misconfigurations to fix](https://labs.detectify.com/2021/02/18/middleware-middleware-everywhere-and-lots-of-misconfigurations-to-fix/)
- [ParseThru – Exploiting HTTP Parameter Smuggling in Golang](https://www.oxeye.io/blog/golang-parameter-smuggling-attack)
- [HTTP.ninja](https://github.com/irsdl/httpninja)
- [Server Technologies - Reverse Proxy Bypass](https://www.contextis.com/en/blog/server-technologies-reverse-proxy-bypass)
- [Cracking the lens: targeting HTTP's hidden attack-surface](https://portswigger.net/research/cracking-the-lens-targeting-https-hidden-attack-surface)
- [Abusing HTTP hop-by-hop request headers](https://nathandavison.com/blog/abusing-http-hop-by-hop-request-headers)
- [The perils of the “real” client IP](https://adam-p.ca/blog/2022/03/x-forwarded-for/)
- [Smuggling HTTP headers through reverse proxies](http://github.security.telekom.com/2020/05/smuggling-http-headers-through-reverse-proxies.html)
- [At Home Among Strangers](https://speakerdeck.com/bo0om/at-home-among-strangers)
- [h2c Smuggling: Request Smuggling Via HTTP/2 Cleartext (h2c)](https://labs.bishopfox.com/tech-blog/h2c-smuggling-request-smuggling-via-http/2-cleartext-h2c)
- [H2C Smuggling in the Wild](https://blog.assetnote.io/2021/03/18/h2c-smuggling/)
- [A story of leaking uninitialized memory from Fastly](https://medium.com/@emil.lerner/leaking-uninitialized-memory-from-fastly-83327bcbee1f)
- [What’s wrong with WebSocket APIs? Unveiling vulnerabilities in WebSocket APIs](https://www.slideshare.net/0ang3el/whats-wrong-with-websocket-apis-unveiling-vulnerabilities-in-websocket-apis)
- [HTTP Desync Attacks: Request Smuggling Reborn](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn)
- [HTTP Request Smuggling via higher HTTP versions](https://www.slideshare.net/neexemil/http-request-smuggling-via-higher-http-versions)
- [HTTP/2: The Sequel is Always Worse](https://portswigger.net/research/http2)
- [Response Smuggling:Exploiting HTTP/1.1 Connections](https://media.defcon.org/DEF%20CON%2029/DEF%20CON%2029%20presentations/Martin%20Doyhenard%20-%20Response%20Smuggling-%20Pwning%20HTTP-1.1%20Connections.pdf)
- [Browser-Powered Desync Attacks: A New Frontier in HTTP Request Smuggling](https://portswigger.net/research/browser-powered-desync-attacks)
- [Making HTTP header injection critical via response queue poisoning](https://portswigger.net/research/making-http-header-injection-critical-via-response-queue-poisoning)
- [Cache poisoning and other dirty tricks](https://lab.wallarm.com/cache-poisoning-and-other-dirty-tricks-120468f1053f/)
- [Practical Web Cache Poisoning](https://portswigger.net/research/practical-web-cache-poisoning)
- [Web Cache Entanglement: Novel Pathways to Poisoning](https://i.blackhat.com/USA-20/Wednesday/us-20-Kettle-Web-Cache-Entanglement-Novel-Pathways-To-Poisoning-wp.pdf)
- [HTTP Caching Tests](https://cache-tests.fyi/)
- [CPDoS: Cache Poisoned Denial of Service](https://cpdos.org/)
- [The Case of the Missing Cache Keys](https://enumerated.wordpress.com/2020/08/05/the-case-of-the-missing-cache-keys/)
- [Responsible denial of service with web cache poisoning](https://portswigger.net/research/responsible-denial-of-service-with-web-cache-poisoning)
- [Cache Poisoning Denial-of-Service Attack Techniques](https://www.acunetix.com/blog/web-security-zone/cache-poisoning-dos-attack-techniques/)
- [Cache-Key Normalization DoS](https://iustin24.github.io/Cache-Key-Normalization-Denial-of-Service/)
- [Web Cache Deception Attack](https://omergil.blogspot.com/2017/02/web-cache-deception-attack.html)
- [Cached and Confused: Web Cache Deception in the Wild](https://sajjadium.github.io/files/usenixsec2020wcd_paper.pdf)
- [Let's Dance in the Cache - Destabilizing Hash Table on Microsoft IIS!](https://blog.orange.tw/2022/08/lets-dance-in-the-cache-destabilizing-hash-table-on-microsoft-iis.html)
