import os
import shutil

from .execute import execute_in_subprocess

SHORTCUT_FILE = '[Desktop Entry]\nName={name}\nExec={command}\nType=Application\n'
PATH = os.getenv('ACTIVITY_PATH') or os.path.expanduser('~/.local/share/kactivitymanagerd/activities')
ACTIVITY_STATE = {
    '2': 'Activated',
    '4': 'Deactivated'
}


class Activity:
    def __init__(self, id_):
        self.id = id_
        self._name = None
        self._description = None
        self._icon = None
        self._state = None
        self._activated = None
        self._deactivated = None
        self._started = None
        self._stopped = None

    @property
    def name(self):
        if not self._name:
            self._name = execute_in_subprocess(['qdbus', 'org.kde.ActivityManager',
                                                '/ActivityManager/Activities',
                                                'org.kde.ActivityManager.Activities.ActivityName',
                                                self.id])[0]
        return self._name

    @name.setter
    def name(self, name):
        execute_in_subprocess(['qdbus', 'org.kde.ActivityManager', '/ActivityManager/Activities',
                               'org.kde.ActivityManager.Activities.SetActivityName',
                               self.id, name])
        self._name = name

    @property
    def description(self):
        if not self._description:
            self._description = execute_in_subprocess(['qdbus', 'org.kde.ActivityManager',
                                                       '/ActivityManager/Activities',
                                                       'org.kde.ActivityManager.Activities.ActivityDescription',
                                                       self.id])[0] or 'No description'
        return self._description

    @description.setter
    def description(self, description):
        execute_in_subprocess(['qdbus', 'org.kde.ActivityManager', '/ActivityManager/Activities',
                               'org.kde.ActivityManager.Activities.SetActivityDescription', self.id,
                               description])
        self._description = description

    @property
    def icon(self):
        if not self._icon:
            self._icon = execute_in_subprocess(['qdbus', 'org.kde.ActivityManager', '/ActivityManager/Activities',
                                                'org.kde.ActivityManager.Activities.ActivityIcon', self.id])[
                             0] or 'No icon'
        return self._icon

    @icon.setter
    def icon(self, icon):
        execute_in_subprocess(['qdbus', 'org.kde.ActivityManager', '/ActivityManager/Activities',
                               'org.kde.ActivityManager.Activities.SetActivityIcon', self.id, icon])
        self._icon = icon

    @property
    def state(self):
        if not self._state:
            self._state = execute_in_subprocess(['qdbus', 'org.kde.ActivityManager',
                                                 '/ActivityManager/Activities',
                                                 'org.kde.ActivityManager.Activities.ActivityState', self.id])[0]
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
        self._create_activity_script('activated', command)
        self._activated = command

    @property
    def deactivated(self):
        if not self._deactivated:
            self._deactivated = self._command_in_activity_script('deactivated')
        return self._deactivated

    @deactivated.setter
    def deactivated(self, command):
        self._create_activity_script('deactivated', command)
        self._deactivated = command

    @property
    def stopped(self):
        if not self._stopped:
            self._stopped = self._command_in_activity_script('stopped')
        return self._stopped

    @stopped.setter
    def stopped(self, command):
        self._create_activity_script('stopped', command)
        self._stopped = command

    @property
    def started(self):
        if not self._started:
            self._started = self._command_in_activity_script('started')
        return self._started

    @started.setter
    def started(self, command):
        self._create_activity_script('started', command)
        self._started = command

    def _create_directory(self):
        path = os.path.join(PATH, self.id)
        if not os.path.isdir(path):
            for p in ['', '/activated', '/deactivated', '/started', '/stopped']:
                os.mkdir(path + p)

    def _delete_directory(self):
        shutil.rmtree(os.path.join(PATH, self.id))

    def _create_activity_script(self, action, command):
        self._create_directory()
        path = '{path}/{id}/{action}/{name}.desktop'.format(path=PATH, id=self.id, action=action, name=self.name)
        with open(path, 'w') as f:
            f.write(SHORTCUT_FILE.format(name=self.name, command=command))

    def _command_in_activity_script(self, action):
        path = '{path}/{id}/{action}/{name}.desktop'.format(path=PATH, id=self.id, action=action, name=self.name)
        try:
            with open(path, 'r') as f:
                for line in f:
                    if line.startswith('Exec='):
                        if line.endswith('\n'):
                            line = line[:-1]
                        return line[5:]
        except FileNotFoundError:
            return 'No command'

    def delete(self):
        execute_in_subprocess(['qdbus', 'org.kde.ActivityManager', '/ActivityManager/Activities',
                               'org.kde.ActivityManager.Activities.RemoveActivity', self.id])
        self._delete_directory()

    def activate(self):
        execute_in_subprocess(['qdbus', 'org.kde.ActivityManager', '/ActivityManager/Activities',
                               'org.kde.ActivityManager.Activities.SetCurrentActivity', self.id])

    def start(self):
        execute_in_subprocess(['qdbus', 'org.kde.ActivityManager', '/ActivityManager/Activities',
                               'org.kde.ActivityManager.Activities.StartActivity', self.id])

    def stop(self):
        execute_in_subprocess(['qdbus', 'org.kde.ActivityManager', '/ActivityManager/Activities',
                               'org.kde.ActivityManager.Activities.StopActivity', self.id])

    @classmethod
    def create(cls, name, args):
        activity_id = execute_in_subprocess(['qdbus', 'org.kde.ActivityManager', '/ActivityManager/Activities',
                                             'org.kde.ActivityManager.Activities.AddActivity', args.name])[0]
        activity = Activity(activity_id)
        activity._create_directory()
        activity._name = name

        if args.icon:
            activity.icon = args.icon
        if args.description:
            activity.description = args.description
        if args.activated:
            activity.activated = args.activated
        if args.deactivated:
            activity.deactivated = args.deactivated
        if args.started:
            activity.started = args.started
        if args.stopped:
            activity.stopped = args.stopped

        return activity
