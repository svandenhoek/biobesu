#!/user/bin/env python3

from shutil import which
from os.path import isfile
from os.path import isdir


def program(cmd):
    """
    Checks whether the command line (which should contain an application name) refers to a valid path. If it is an
    existing application, does nothing. If the path is not valid, exits with an OSError indicating there is a missing
    application.
    :param cmd: the name of the application as how it would be called using the command line
    """

    if not which(cmd):
        exit(OSError("Error: " + cmd + " is not available on this system."))


def file(parser, file_string, expected_extension):
    """
    Checks whether given path goes to a valid file. If not, throws a parser error.
    :param parser: the parser used to throw an error
    :param file_string: file path to check
    :param expected_extension: the expected file extension
    """

    if not file_string.endswith(expected_extension):
        parser.error('"' + file_string.split('/')[-1] + '" is not a .tsv file')
    if not isfile(file_string):
        parser.error('"' + file_string.split('/')[-1] + '" is not an existing file')


def directory(parser, dir_string):
    """
    Checks whether given path goes to an existing directory. If not, throws a parser error.
    :param parser: the parser used to throw an error
    :param dir_string: directory path to check
    """

    # Strips slash on the end of an url.
    dir_string = dir_string.rstrip("/")

    if not isdir(dir_string):
        parser.error('"' + dir_string.split('/')[-1] + '" is not a valid directory')

    return dir_string
