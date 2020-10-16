# Authorizer Challanger

## Dependencies
You could run this applications only using the:
- [Docker]()
Also, you can run it with:
- Python 3.8+ installed in your system

## Installing the dependencies

You can install the test dependencies running the following command:
```shell
> make test.install
```

## Running tests
You can run all the tests running the following command:
```shell
> make test.all
```

## Running the application
For running the application as streaming you can use the input redirection operator `<` as the following example:
```shell
> make run < operations
```
