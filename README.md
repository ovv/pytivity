# Pytivity

Pytivity is a python3 command line manager for your KDE activities.

## Installation

```bash
pip install pytivity
```

## Basic usage

It enables you to easily create, update, delete, start, stop or activate an activity from the command line.

```bash
pytivity create/update/delete/start/stop/activate {name}
```

You can also set commands to be run when an activity get started, stopped, activated or deactivated.

```bash
pytivity create {name} --activated {command} --deactivated {command} --started {command} --stopped {command}
```
