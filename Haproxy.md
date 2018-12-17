- http://www.haproxy.org/
- Tested version - 1.8

## Basics
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
Cache's been partly implemented in this version of HAproxy. It was not tested. [Nuster](nuster) was tested instead
