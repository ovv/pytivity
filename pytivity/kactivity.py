import os
import shutil

import xdg

from pydbus import SessionBus

SHORTCUT_FILE = '[Desktop Entry]\nName={name}' \
                '\nExec={command}\nType=Application\n'
PATH = os.path.join(xdg.XDG_DATA_HOME, 'kactivitymanagerd/activities')
ACTIVITY_STATE = {
    2: 'Started',
    4: 'Stopped'
}


class KActivity(object):
    """
    A KDE activity

    This class represent a single kde activity. It can be create by the id or
    the name of the activity.

    Note:
        Attributes are cached in the objects. Use the `refresh` method to
        reset the cache.

        A new activity can be created with the `create` class method

    Args:
        id_or_name (str): Name or ID of the activity
         bus: Proxy dbus object to 'org.kde.ActivityManager
         /ActivityManager/Activities'

    Attributes:
        id (str): Id of the activity
        name (str): Name of the activity
        description (str): Description of the activity
        icon (str): Icon of the activity
        state (str): State of the activity (`Started` or `Stopped`)
        activated (str): Command executed at activation of the activity
        deactivated (str): Command executed at deactivation of the activity
        started (str): Command executed at startup of the activity
        stopped (str): Command executed at shutdown of the activity

    """
    def __init__(self, id_or_name, bus=None):
        if not bus:
            bus = SessionBus()
            self._activity_bus = bus.get('org.kde.ActivityManager',
                                         '/ActivityManager/Activities')
        else:
            self._activity_bus = bus

        if len(id_or_name) != 36:
            self.id = self._find_id(id_or_name)
        else:
            self.id = id_or_name

        self._name = None
        self._description = None
        self._icon = None
        self._state = None
        self._activated = None
        self._deactivated = None
        self._started = None
        self._stopped = None

    def refresh(self):
        """
        Reset the cached attributes

        :return: None
        """
        self._name = None
        self._description = None
        self._icon = None
        self._state = None
        self._activated = None
        self._deactivated = None
        self._started = None
        self._stopped = None

    def delete(self):
        """
        Delete the activity

        :return: None
        """
        self._activity_bus.RemoveActivity(self.id)
        self._delete_directory()

    def activate(self):
        """
        Activate the activity

        :return: None
        """
        self._activity_bus.SetCurrentActivity(self.id)

    def start(self):
        """
        Start the activity

        :return: None
        """
        self._activity_bus.StartActivity(self.id)

    def stop(self):
        """
        Stop the activity

        :return: None
        """
        self._activity_bus.StopActivity(self.id)

    @property
    def name(self):
        if not self._name:
            self._name = self._activity_bus.ActivityName(self.id)
        return self._name

    @name.setter
    def name(self, name):
        self._activity_bus.SetActivityName(self.id, name)
        self._name = name

    @property
    def description(self):
        if not self._description:
            self._description = self._activity_bus.ActivityDescription(self.id)
        return self._description

    @description.setter
    def description(self, description):
        self._activity_bus.SetActivityDescription(self.id, description)
        self._description = description

    @property
    def icon(self):
        if not self._icon:
            self._icon = self._activity_bus.ActivityIcon(self.id)
        return self._icon

    @icon.setter
    def icon(self, icon):
        self._activity_bus.SetActivityDescription(self.id, icon)
        self._icon = icon

    @property
    def state(self):
        self._state = self._activity_bus.ActivityState(self.id)
        return ACTIVITY_STATE.get(self._state, self._state)

    @state.setter
    def state(self):
        raise NotImplementedError

    @property
    def activated(self):
        if not self._activated:
            self._activated = self._command_in_activity_script('activated')
        return self._activated

    @activated.setter
    def activated(self, command):
        if command:
            self._create_activity_script('activated', command)
        else:
            self._delete_activity_script('activated')
        self._activated = command

    @property
    def deactivated(self):
        if not self._deactivated:
            self._deactivated = self._command_in_activity_script('deactivated')
        return self._deactivated

    @deactivated.setter
    def deactivated(self, command):
        if command:
            self._create_activity_script('deactivated', command)
        else:
            self._delete_activity_script('deactivated')
        self._deactivated = command

    @property
    def stopped(self):
        if not self._stopped:
            self._stopped = self._command_in_activity_script('stopped')
        return self._stopped

    @stopped.setter
    def stopped(self, command):
        if command:
            self._create_activity_script('stopped', command)
        else:
            self._delete_activity_script('stopped')
        self._stopped = command

    @property
    def started(self):
        if not self._started:
            self._started = self._command_in_activity_script('started')
        return self._started

    @started.setter
    def started(self, command):
        if command:
            self._create_activity_script('started', command)
        else:
            self._delete_activity_script('started')
        self._started = command

    def _create_directory(self):
        path = os.path.join(PATH, self.id)
        if not os.path.isdir(path):
            for p in ['', '/activated', '/deactivated', '/started',
                      '/stopped']:
                os.mkdir(path + p)

    def _find_id(self, name):
        for activity_id in self._activity_bus.ListActivities(
                2) + self._activity_bus.ListActivities(4):
            if name == self._activity_bus.ActivityName(activity_id):
                return activity_id
        raise ValueError('No activity exist with the name: {}'.format(name))

    def _delete_directory(self):
        shutil.rmtree(os.path.join(PATH, self.id))

    def _create_activity_script(self, action, command):
        self._create_directory()
        path = '{path}/{id}/{action}/{name}.desktop'.format(path=PATH,
                                                            id=self.id,
                                                            action=action,
                                                            name=self.name)
        with open(path, 'w') as f:
            f.write(SHORTCUT_FILE.format(name=self.name, command=command))

    def _delete_activity_script(self, action):
        path = '{path}/{id}/{action}/{name}.desktop'.format(path=PATH,
                                                            id=self.id,
                                                            action=action,
                                                            name=self.name)
        try:
            os.remove(path)
        except IOError:
            pass

    def _command_in_activity_script(self, action):
        path = '{path}/{id}/{action}/{name}.desktop'.format(path=PATH,
                                                            id=self.id,
                                                            action=action,
                                                            name=self.name)
        try:
            with open(path, 'r') as f:
                for line in f:
                    if line.startswith('Exec='):
                        if line.endswith('\n'):
                            line = line[:-1]
                        return line[5:]
        except IOError:
            return ''

    @classmethod
    def create(cls, name, icon=None, description=None, activated=None,
               deactivated=None, started=None, stopped=None, bus=None):
        """
        Create a new activity

        :param name: Name of the activity
        :param icon: Icon of the activity
        :param description: Description of the activity
        :param activated: Command executed at activation of the activity
        :param deactivated: Command executed at deactivation of the activity
        :param started: Command executed at startup of the activity
        :param stopped: Command executed at shutdown of the activity
        :param bus: Proxy dbus object to 'org.kde.ActivityManager
        /ActivityManager/Activities'
        :return: The new activity
        """

        if not bus:
            bus = SessionBus().get('org.kde.ActivityManager',
                                   '/ActivityManager/Activities')

        activity_id = bus.AddActivity(name)

        activity = KActivity(activity_id, bus=bus)
        activity._create_directory()
        activity._name = name

        if icon is not None:
            activity.icon = icon
        if description is not None:
            activity.description = description
        if activated is not None:
            activity.activated = activated
        if deactivated is not None:
            activity.deactivated = deactivated
        if started is not None:
            activity.started = started
        if stopped is not None:
            activity.stopped = stopped

        return activity
