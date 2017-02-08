# Installation

## Pydbus

Pytivity rely on `pydbus` which requires additional packages. 
See `pydbus` [documentation](https://github.com/LEW21/pydbus).

For ubuntu you need to install `python3-gi`: 
```bash
$ apt-get install python3-gi
```

## System wide

```bash
$ pip3 install pytivity
```

## Virtual environment

### Python 3.5

1. Install the additional packages required by `pydbus`
2. Create a virtual environment with `--system-site-packages` and activate it

```bash
$ python3.5 -m venv .env --system-site-packages
```

```bash
$ source .env/bin/activate
```

3. Install pip

```bash
$ curl https://bootstrap.pypa.io/3.2/get-pip.py | python
```
4. Install pytivity

```bash
$ pip install pytivity
```