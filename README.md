# Adherium ETL Tool

The HGE `adherium-etl` tool is a Python-based application that processes data from a dedicated SFTP server with Adherium study data.

## Usage

Requires Python 3.7.x and Make. All dependencies (including dev deps) are installed in a virtualenv along with the `covid` module in editable mode.

```
$ make env
$ make test
$ source .venv/bin/activate
$ python -m covid
```

## Build

```
$ make build
```

TODO
