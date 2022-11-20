# pydatascience Template

A basic openfaas-template aimed at Python oriented data scientist.

The Docker image is based on Python3 and uses Conda for installing packages.

## Build Args
1.`ADDITIONAL_PACKAGE`: can be a list of additional packages that will be installed using apt-get
2. `CHANNEL`: specifies an additional Conda channel that will be searched when installing python package


## How to use

```shell
faas template pull https://github.com/roolio/pydatascience-template
faas new my_function --lang=pydatascience
# code the handler.py version
faas up -f test.yml
```

If you have a _Post "http://192.168.64.2:8080/system/functions": context deadline exceeded (Client.Timeout exceeded while awaiting headers)_ message, 
that means that retrieval from ghcri.io image to faasd containerd was too long. You can retry by deploying with that command : 

```shell
faas deploy -f test.yml
```

(up is a shortcut for several actions : build + deploy)

Test : exemple with json input : 
```shell 
curl http://$OPENFAAS_URL/function/test --data '{"msg" : "Hello"}'
```
