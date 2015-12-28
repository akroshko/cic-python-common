#!/usr/bin/env python
#####################################################################################
## Support for a hybrid command line argument parser/function call that runs commands
import string
import argparse

def main_command(subcommand_prefix,global_variables):
    # build the arguments
    parser = argparse.ArgumentParser(description='')
    subparser = parser.add_subparsers(help='',dest='command')
    subparsers = {}
    for subcommand_name in get_subcommands(subcommand_prefix,global_variables):
        subcommand = global_variables[subcommand_name]()
        subparsers[subcommand_name] = subparser.add_parser(
                                        remove_subcommand_prefix(
                                          subcommand_name,
                                          subcommand_prefix),
                                        help = subcommand.help)
        # add the individual subcommand arguments
        for argument in subcommand.arguments:
            subparsers[subcommand_name].add_argument(
                                          argument['name'],
                                          nargs=argument['nargs'],
                                          default=argument['default'],
                                          type=argument['process'],
                                          help=argument['help'])
        # add the individual subcommand options
        for option in subcommand.options:
            if option['nargs'] == None:
                subparsers[subcommand_name].add_argument(
                                              add_option_prefix(option['name']),
                                              action = 'store_true',
                                              help=option['help'])
            else:
                subparsers[subcommand_name].add_argument(
                                              add_option_prefix(option['name']),
                                              nargs=option['nargs'],
                                              default=option['default'],
                                              type=option['process'],
                                              help=option['help'])
    # parse the arguments
    parsed = parser.parse_args()
    # process the subcommand into args and kwds
    subcommand = global_variables[add_subcommand_prefix(getattr(parsed,'command'),
                                                        subcommand_prefix)]()
    args = []
    for argument in subcommand.arguments:
        name = argument['name'].strip()
        args.append(getattr(parsed,name))
    args = tuple(args)
    kwds = {}
    for option in subcommand.options:
        name = option['name'].strip().translate(DASH_TRANSLATE)
        kwds[name] = getattr(parsed,name)
    # call the command
    ret = subcommand(*args,**kwds)
    # TODO: better way of returning
    print ret

def get_subcommands(prefix,global_variables):
    """
    Get the list of subcommands from the current script.
    """
    subcommands = []
    # gets the subcommands from globals
    for item in global_variables:
        if item.startswith(prefix):
            subcommands.append(item)
    # TODO: test if callable
    return subcommands

def subcommand_to_argument(subcommand,prefix):
    """
    Convert the function for a subcommand to the name of the command-line
    argument used.

    **Arguments**:
      subcommand : string
        The subcommand to convert to an arguments.
      prefix : string
        The prefix to add.

    **Return**:
      string:
        The subcommand as an argument.
    """
    return remove_subcommand_prefix(subcommand,prefix)

def add_subcommand_prefix(subcommand,prefix):
    """
    Add the prefix to a command-line argument to convert into a function name
    for a subcommand.

    **Arguments**:
      subcommand : string
        The subcommand to add the prefix to.
      prefix : string
        The prefix to add.

    **Return**:
      string:
        The subcommand as an argument.
    """
    return prefix + subcommand

def remove_subcommand_prefix(subcommand,prefix):
    """
    Remove the prefix form the subcommand function name.

    **Arguments**:
      subcommand : string
        The subcommand to remove the prefix from.
      prefix : string
        The prefix to add.

    **Return**:
      The subcommand as an argument.
    """
    return subcommand[len(prefix):]

def add_option_prefix(option):
    """
    Add the prefix used for command-line options.

    **Arguments**:
      option : string
        The option to add the prefix to.

    **Return**:
      string:
        The subcommand as an argument.
    """
    return '--' + option

def remove_option_prefix(option):
    """
    Remove the prefix used for command-line options.

    **Arguments**:
      option : string
        The option to remove the prefix from.

    **Return**:
      string:
        The subcommand as an argument.
    """
    return option[2:]
