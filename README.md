# Pytivity

Pytivity is a python3 command line manager for your KDE activities.

## Installation

```bash
pip install pytivity
```

Pytivity rely on `pydbus` to connect to dbus. See `pydbus` [documentation](https://github.com/LEW21/pydbus) for installation instruction.

## Basic usage

Pytivity enables you to easily create, update, delete, start, stop or activate an activity from the command line.

```bash
pytivity create/update/delete/start/stop/activate {name}
```

And set commands to be run when an activity is started, stopped, activated or deactivated.

```bash
pytivity create/update {name} --activated {command} --deactivated {command} --started {command} --stopped {command}
```

## Usage

```bash
pytivity {main arguments} {command} {command arguments}
```

### Main arguments

- `-h` Show help message and exit
- `-v` Show Pytivity version
- `-n` Display a system notification

### commands

- `create`: Create a new activity
- `update`: Update an existing activity
- `delete`: Delete an activity
- `list`: List activities
- `start`: Start an activity
- `stop`: Stop an activity
- `activate`: Activate an activity

All commands have help message that explains the available arguments.

```bash
pytivity {command} -h
```

## Contributing

All contribution are welcome !