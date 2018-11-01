Pytivity
========

Pytivity is a python 3.5 command line manager for your KDE activities.

Installation
------------

.. code::

    $ pip3 install pytivity

Pytivity rely on the `pydbus` module to connect to dbus which requires additional packages, `pydbus installation instruction <https://github.com/LEW21/pydbus>`_.

Quickstart
----------

Pytivity enables you to easily create, update, delete, start, stop or activate an activity from the command line.

.. code::

    $ pytivity create/update/delete/start/stop/activate {name}

And set commands to be run when an activity is started, stopped, activated or deactivated.

.. code::

    $ pytivity create/update {name} --activated {command} --deactivated {command} --started {command} --stopped {command}

All commands have help message that explains the available arguments.

.. code::

    $ pytivity {command} -h

Changelog
---------

0.0.5
`````

* Bugfixes
* Add `--stop` argument to `activate` command 

0.0.4
`````

* Use `pydbus`
* Desktop notification

0.0.3
`````

* Initial release

Contributing
------------

All contribution are welcome !
