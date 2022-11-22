## To run without Docker
Start the server by simply entering

```sh
$ python server.py -p <port-number>
```

The default port number is 8000.


## To run via Docker
```shell
$ docker pull nabarneeraj/simple-api

$ docker run --rm --name sapi1 -p 8000:8000 nabarneeraj/simple-api
```

## Testing API endpoints
```shell
$ curl http://localhost:8000
Index%

$ curl http://localhost:8000/api/sysinfo
{"name": "2752e0522503", "type": "Linux", "kernel": "#1 SMP Tue Sep 13 07:51:46 UTC 2022", "arch": "x86_64"}%

$ curl -X POST http://localhost:8000/api/setstate \
> -H 'Content-Type:application/json' \
> -d '{"state":1}'
{"state": 1}%

$ curl http://localhost:8000/api/currentstate
{"state": 1}%

$ curl -X POST http://localhost:8000/api/setstate \
-H 'Content-Type:application/json' \
-d '{"state":42}'
{"state": 42}%

$ curl http://localhost:8000/api/currentstate
{"state": 42}%
```