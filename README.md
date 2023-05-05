# echo

## usage
return path and method and heads and data

## other usage
### /status/[status-code]
got http status code as your wish

### /raise_exception
raise an exception and return http status 500

### /sys-status/
print system status

## docker run

docker run -d \
  -p 8008:80 \
  registry.cn-hangzhou.aliyuncs.com/endlessstudio/echo:latest

## docker-compose

```yaml
version: '3'
services:
  echo:
    image: registry.cn-hangzhou.aliyuncs.com/endlessstudio/echo:latest
    restart: always
    ports:
    - 8008:80
    environment:
    - DEBUG=False
```