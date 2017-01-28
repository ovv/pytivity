#!/usr/bin/env python

import argparse

from terminaltables import AsciiTable

from .activity import Activity
from .execute import execute_in_subprocess


def main():
    main_parser = argparse.ArgumentParser(description='Pytivity')
    main_parser.set_defaults(func=list_short)
    subparsers = main_parser.add_subparsers(title='subcommands')

    create_parser = subparsers.add_parser('create', help='create a new activity')
    create_parser.set_defaults(func=create)

    update_parser = subparsers.add_parser('update', help='update an activity')
    update_parser.set_defaults(func=update)

    delete_parser = subparsers.add_parser('delete', help='delete an activity')
    delete_parser.set_defaults(func=delete)

    list_parser = subparsers.add_parser('list', help='list activites')
    list_parser.set_defaults(func=list_act)

    start_parser = subparsers.add_parser('start', help='start an activity')
    start_parser.set_defaults(func=start)

    stop_parser = subparsers.add_parser('stop', help='stop an activity')
    stop_parser.set_defaults(func=stop)

    activate_parser = subparsers.add_parser('activate', help='activate an activity')
    activate_parser.set_defaults(func=activate)

    create_parser.add_argument('name', help='name of the activity')
    create_parser.add_argument('-d', '--description', help='description of the activity')
    create_parser.add_argument('-i', '--icon', help='icon of the activity')
    create_parser.add_argument('--activated', help='command to execute when activating activity',
                               dest='activated')
    create_parser.add_argument('--deactivated', help='command to execute when deactivating activity',
                               dest='deactivated')
    create_parser.add_argument('--started', help='command to execute when starting activity',
                               dest='started')
    create_parser.add_argument('--stopped', help='command to execute when stopping activity',
                               dest='stopped')

    update_parser.add_argument('name', help='name of the activity')
    update_parser.add_argument('-n', '--name', help='new name of the activity', dest='new_name')
    update_parser.add_argument('-d', '--description', help='description of the activity')
    update_parser.add_argument('-i', '--icon', help='icon of the activity')
    update_parser.add_argument('--activated', help='command to execute when activating activity',
                               dest='activated')
    update_parser.add_argument('--deactivated', help='command to execute when deactivating activity',
                               dest='deactivated')
    update_parser.add_argument('--started', help='command to execute when starting activity',
                               dest='started')
    update_parser.add_argument('--stopped', help='command to execute when stopping activity',
                               dest='stopped')

    delete_parser.add_argument('name', help='name of the activity')

    list_parser.add_argument('-v', '--verbose', help='display more information', action='count', dest='verbose',
                             default=0)
    list_parser.add_argument('-c', '--commands', help='display executed commands for all actions', action='store_true',
                             dest='commands')
    list_parser.add_argument('--icon', help='display the icon', action='store_true')
    list_parser.add_argument('--description', help='display the description', action='store_true')
    list_parser.add_argument('--id', help='display the activity(ies) id(s)', action='store_true')
    list_parser.add_argument('--raw', help='display raw data', action='store_true')
    list_parser.add_argument('-n', '--name', help='display only the named activity')

    start_parser.add_argument('name', help='name of the activity')

    stop_parser.add_argument('name', help='name of the activity')

    activate_parser.add_argument('name', help='name of the activity')

    args = main_parser.parse_args()

    activities = _activities()

    if args.func in [create, delete, list_act, update, start, stop, activate, list_short]:
        args.func(activities, args)
    else:
        main_parser.print_help()


def _activities():
    activities_id = execute_in_subprocess(['qdbus', 'org.kde.ActivityManager', '/ActivityManager/Activities',
                                           'org.kde.ActivityManager.Activities.ListActivities'])
    return [Activity(id_) for id_ in activities_id]


def create(activities, args):
    activities = [activity for activity in activities if activity.name == args.name]

    if activities:
        print('An activity already exist with this name ({name}). ID: {id}'.format(name=args.name, id=activities[0].id))
        return

    activity = Activity.create(args.name, args)
    print('New activity ({name}) created. ID: {id}'.format(name=activity.name, id=activity.id))


def update(activities, args):
    activities = [activity for activity in activities if activity.name == args.name]

    if not activities:
        print('No activity found with this name: {}'.format(args.name))
        return

    for activity in activities:
        if args.new_name:
            activity.name = args.new_name
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
        print('Activity ({name}) updated ID: {id}'.format(name=args.name, id=activity.id))


def delete(activities, args):
    activities = [activity for activity in activities if activity.name == args.name]

    if not activities:
        print('No activity found with this name: {}'.format(args.name))
        return

    for activity in activities:
        activity.delete()
        print('Activity ({name}) successfully deleted. ID: {id}'.format(name=args.name, id=activity.id))


def list_short(activities, args):
    output = [['Name', 'State']]
    for activity in activities:
        output.append([activity.name, activity.state])
    table = AsciiTable(table_data=output, title='Activities')
    print(table.table)


def list_act(activities, args):

    output = list()
    header = ['Name', 'State']

    if args.id or args.verbose > 2:
        header = ['ID'] + header
    if args.commands or args.verbose > 0:
        header += ['Cmd Activated', 'Cmd Deactivated', 'Cmd started', 'Cmd stopped']
    if args.icon or args.verbose > 1:
        header += ['Icon']
    if args.description or args.verbose > 1:
        header += ['Description']

    if args.name:
        activities = [activity for activity in activities if activity.name == args.name]

    for activity in activities:
        if args.id or args.verbose > 2:
            data = [activity.id, activity.name, activity.state]
        else:
            data = [activity.name, activity.state]

        if args.commands or args.verbose > 0:
            data += [activity.activated, activity.deactivated, activity.started, activity.stopped]

        if args.icon or args.verbose > 1:
            data.append(activity.icon)
        if args.description or args.verbose > 1:
            data.append(activity.description)

        output.append(data)

    if not args.raw:
        output.insert(0, header)
        table = AsciiTable(table_data=output, title='Activities')
        print(table.table)
    else:
        for activity in output:
            print(', '.join(activity))


def start(activities, args):
    activities = [activity for activity in activities if activity.name == args.name]

    for activity in activities:
        activity.start()
        print('Activity ({name}) started. ID: {id}'.format(name=args.name, id=activity.id))


def stop(activities, args):
    activities = [activity for activity in activities if activity.name == args.name]

    for activity in activities:
        activity.stop()
        print('Activity ({name}) stopped. ID: {id}'.format(name=args.name, id=activity.id))


def activate(activities, args):
    activities = [activity for activity in activities if activity.name == args.name]

    for activity in activities:
        activity.activate()
        print('Activity ({name}) activated. ID: {id}'.format(name=args.name, id=activity.id))


if __name__ == '__main__':
    main()
