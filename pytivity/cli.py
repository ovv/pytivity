#!/usr/bin/env python

import argparse

from pydbus import SessionBus
from terminaltables import AsciiTable

from .kactivity import KActivity
from .__meta__ import METADATA


def main():
    main_parser = argparse.ArgumentParser(description=METADATA['description'])
    main_parser.set_defaults(func=list_short)
    main_parser.add_argument('-v', '--version', help='show pytivity version',
                             action='store_true')
    main_parser.add_argument('-n', '--notification', action='store_true',
                             help='display a system notification')

    subparsers = main_parser.add_subparsers(title='commands')

    create_parser = subparsers.add_parser('create',
                                          help='create a new activity')
    create_parser.set_defaults(func=create)

    update_parser = subparsers.add_parser('update', help='update an activity')
    update_parser.set_defaults(func=update)

    delete_parser = subparsers.add_parser('delete', help='delete an activity')
    delete_parser.set_defaults(func=delete)

    list_parser = subparsers.add_parser('list', help='list activities')
    list_parser.set_defaults(func=list_act)

    start_parser = subparsers.add_parser('start', help='start an activity')
    start_parser.set_defaults(func=start)

    stop_parser = subparsers.add_parser('stop', help='stop an activity')
    stop_parser.set_defaults(func=stop)

    activate_parser = subparsers.add_parser('activate',
                                            help='activate an activity')
    activate_parser.set_defaults(func=activate)

    create_parser.add_argument('name', help='name of the activity')
    create_parser.add_argument('-d', '--description',
                               help='description of the activity')
    create_parser.add_argument('-i', '--icon', help='icon of the activity')
    create_parser.add_argument('--activated',
                               help='command to execute when activating an '
                                    'activity',
                               dest='activated', nargs='?', const=False)
    create_parser.add_argument('--deactivated',
                               help='command to execute when deactivating an '
                                    'activity',
                               dest='deactivated', nargs='?', const=False)
    create_parser.add_argument('--started',
                               help='command to execute when starting an '
                                    'activity',
                               dest='started', nargs='?', const=False)
    create_parser.add_argument('--stopped',
                               help='command to execute when stopping an '
                                    'activity',
                               dest='stopped', nargs='?', const=False)

    update_parser.add_argument('name', help='name or id  of the activity')
    update_parser.add_argument('-n', '--name', help='new name of the activity',
                               dest='new_name')
    update_parser.add_argument('-d', '--description',
                               help='description of the activity')
    update_parser.add_argument('-i', '--icon', help='icon of the activity')
    update_parser.add_argument('--activated',
                               help='command to execute when activating an '
                                    'activity',
                               dest='activated', nargs='?', const=False)
    update_parser.add_argument('--deactivated',
                               help='command to execute when deactivating an '
                                    'activity',
                               dest='deactivated', nargs='?', const=False)
    update_parser.add_argument('--started',
                               help='command to execute when starting an '
                                    'activity',
                               dest='started', nargs='?', const=False)
    update_parser.add_argument('--stopped',
                               help='command to execute when stopping an '
                                    'activity',
                               dest='stopped', nargs='?', const=False)

    delete_parser.add_argument('name', help='name or id  of the activity')

    list_parser.add_argument('-v', '--verbose',
                             help='display more informations (3 levels)',
                             action='count', dest='verbose',
                             default=0)
    list_parser.add_argument('-c', '--commands',
                             help='display executed commands when activity is '
                                  'activated/deactivated/started/stopped',
                             action='store_true',
                             dest='commands')
    list_parser.add_argument('--icon', action='store_true',
                             help='display the activity(ies) icon(s)',)
    list_parser.add_argument('--description', help='display the activity(ies) '
                                                   'description(s)',
                             action='store_true')
    list_parser.add_argument('--id', help='display the activity(ies) id(s)',
                             action='store_true')
    list_parser.add_argument('--raw', help='output non formatted data',
                             action='store_true')
    list_parser.add_argument('-n', '--name',
                             help='display only the named activity')

    start_parser.add_argument('name', help='name or id  of the activity')

    stop_parser.add_argument('name', help='name or id  of the activity')

    activate_parser.add_argument('name', help='name or id  of the activity')

    args = main_parser.parse_args()

    if args.version:
        print(METADATA['version'])
    elif args.func in [create, delete, list_act, update, start, stop, activate,
                       list_short]:
        bus = SessionBus()
        activity_bus = bus.get('org.kde.ActivityManager',
                               '/ActivityManager/Activities')

        if args.notification:
            notification_bus = bus.get('.Notifications')
        else:
            notification_bus = None

        try:
            args.func(args, activity_bus=activity_bus,
                      notification_bus=notification_bus)
        except ValueError as e:
            print(e)
    else:
        main_parser.print_help()


def create(args, activity_bus, notification_bus=None):
    activity = KActivity.create(args.name, bus=activity_bus)

    if args.icon:
        activity.icon = args.icon
    if args.description:
        activity.description = args.description
    if args.activated or args.activated is False:
        activity.activated = args.activated
    if args.deactivated or args.deactivated is False:
        activity.deactivated = args.deactivated
    if args.started or args.started is False:
        activity.started = args.started
    if args.stopped or args.stopped is False:
        activity.stopped = args.stopped

    if notification_bus:
        _send_notification(notification_bus,
                           '{} created !'.format(activity.name),
                           activity.id,
                           activity.icon)

    print('Activity ({name}) created. ID: {id}'.format(name=args.name,
                                                       id=activity.id))


def update(args, activity_bus, notification_bus=None):
    activity = KActivity(args.name, bus=activity_bus)

    if args.new_name:
        activity.name = args.new_name
    if args.icon:
        activity.icon = args.icon
    if args.description:
        activity.description = args.description
    if args.activated or args.activated is False:
        activity.activated = args.activated
    if args.deactivated or args.deactivated is False:
        activity.deactivated = args.deactivated
    if args.started or args.started is False:
        activity.started = args.started
    if args.stopped or args.stopped is False:
        activity.stopped = args.stopped

    if notification_bus:
        _send_notification(notification_bus,
                           '{} updated !'.format(activity.name),
                           activity.id,
                           activity.icon)

    print('Activity ({name}) updated. ID: {id}'.format(name=args.name,
                                                       id=activity.id))


def delete(args, activity_bus, notification_bus=None):
    activity = KActivity(args.name, bus=activity_bus)
    activity.delete()

    if notification_bus:
        _send_notification(notification_bus,
                           '{} deleted !'.format(activity.name),
                           activity.id,
                           activity.icon)

    print('Activity ({name}) successfully deleted. ID: {id}'.format(
        name=args.name, id=activity.id))


def list_short(args, activity_bus, notification_bus=None):
    output = [['Name', 'State']]
    activities = [KActivity(activity_id, bus=activity_bus) for activity_id in
                  _list_activities(activity_bus=activity_bus)]

    output += [[activity.name, activity.state] for activity in activities]
    table = AsciiTable(table_data=output, title='Activities')
    print(table.table)


def list_act(args, activity_bus, notification_bus=None):
    output = list()
    header = ['Name', 'State']

    if args.name:
        activities = [KActivity(args.name, bus=activity_bus)]
    else:
        activities = [KActivity(activity_id, bus=activity_bus) for activity_id
                      in _list_activities(activity_bus=activity_bus)]

    if args.id or args.verbose > 2:
        header = ['ID'] + header
    if args.commands or args.verbose > 0:
        header += ['Cmd Activated', 'Cmd Deactivated', 'Cmd started',
                   'Cmd stopped']
    if args.icon or args.verbose > 1:
        header += ['Icon']
    if args.description or args.verbose > 1:
        header += ['Description']

    for activity in activities:
        if args.id or args.verbose > 2:
            data = [activity.id, activity.name, activity.state]
        else:
            data = [activity.name, activity.state]

        if args.commands or args.verbose > 0:
            data += [activity.activated, activity.deactivated,
                     activity.started, activity.stopped]

        if args.icon or args.verbose > 1:
            data.append(activity.icon)
        if args.description or args.verbose > 1:
            data.append(activity.description)

        output.append(data)

    if args.raw:
        for activity in output:
            print(', '.join(activity))
    else:
        output.insert(0, header)
        table = AsciiTable(table_data=output, title='Activities')
        print(table.table)


def start(args, activity_bus, notification_bus=None):
    activity = KActivity(args.name, bus=activity_bus)
    activity.start()

    if notification_bus:
        _send_notification(notification_bus,
                           '{} started !'.format(activity.name),
                           activity.id,
                           activity.icon)

    print('Activity ({name}) started. ID: {id}'.format(name=args.name,
                                                       id=activity.id))


def stop(args, activity_bus, notification_bus=None):
    activity = KActivity(args.name, bus=activity_bus)
    activity.stop()

    if notification_bus:
        _send_notification(notification_bus,
                           '{} stopped !'.format(activity.name),
                           activity.id,
                           activity.icon)

    print('Activity ({name}) stopped. ID: {id}'.format(name=args.name,
                                                       id=activity.id))


def activate(args, activity_bus, notification_bus=None):
    activity = KActivity(args.name, bus=activity_bus)
    activity.activate()

    if notification_bus:
        _send_notification(notification_bus,
                           '{} activated !'.format(activity.name),
                           activity.id,
                           activity.icon)

    print('Activity ({name}) activated. ID: {id}'.format(name=args.name,
                                                         id=activity.id))


def _list_activities(activity_bus):
    return activity_bus.ListActivities(2) + activity_bus.ListActivities(4)


def _send_notification(notification_bus, title, body, icon=None):
    if not icon:
        icon = 'dialog-information'
    notification_bus.Notify('Pytivity', 0, icon, title, body, [], {}, 2000)


if __name__ == '__main__':
    main()
