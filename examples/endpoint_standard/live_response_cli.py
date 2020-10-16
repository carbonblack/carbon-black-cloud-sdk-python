#!/usr/bin/env python

# *******************************************************
# Copyright (c) VMware, Inc. 2020. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Example command-line interface to Live Response."""

import sys
import time
import cmd
import logging
import ntpath
import shutil
import subprocess
from optparse import OptionParser

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.endpoint_standard import Device

log = logging.getLogger(__name__)


class QuitException(Exception):
    pass


class CliArgsException(Exception):
    pass


class CliHelpException(Exception):
    pass


class CliAttachError(Exception):
    pass


def split_cli(line):
    '''
    we'd like to use shlex.split() but that doesn't work well for
    windows types of things.  for now we'll take the easy approach
    and just split on space. We'll then cycle through and look for leading
    quotes and join those lines
    '''

    parts = line.split(' ')
    final = []

    while len(parts) > 0:

        tok = parts.pop(0)
        if (tok[:1] == '"'):
            tok = tok[1:]
            next = parts.pop(0)
            while(next[-1:] != '"' and len(parts) > 0):
                tok += ' ' + next
                next = parts.pop(0)

            if (next[-1:] == '"'):
                tok += ' ' + next[:-1]

        final.append(tok)
    return final


class CliArgs (OptionParser):
    def __init__(self, usage=''):
        OptionParser.__init__(self, add_help_option=False, usage=usage)

        self.add_option('-h', '--help', action='store_true', help='Display this help message.')

    def parse_line(self, line):
        args = split_cli(line)
        return self.parse_args(args)

    def parse_args(self, args, values=None):
        (opts, args) = OptionParser.parse_args(self, args=args, values=values)

        if (opts.help):
            self.print_help()
            raise CliHelpException()

        return (opts, args)

    def error(self, msg):
        raise CliArgsException(msg)


class CblrCli(cmd.Cmd):
    def __init__(self, cb, connect_callback):
        """
        Create a CbLR Command Line class

        :param cb: Connection to the Carbon Black Cloud SDK
        :param connect_callback: Callable to get a sensor object from the ``connect`` command
        :type cb: CbCloudAPI
        :return:
        """
        cmd.Cmd.__init__(self)

        # global variables
        # apply regardless of session state
        self.cb = cb
        self.connect_callback = connect_callback

        lr_session = None
        """:type lr_session: LiveResponseSession"""
        self.lr_session = lr_session

        self.reset()

    @property
    def prompt(self):
        if not self.lr_session:
            return "(unattached)> "
        else:
            return "{0}\\> ".format(self.cwd)

    def emptyline(self):
        pass

    def cmdloop(self, intro=None):
        while True:
            try:
                cmd.Cmd.cmdloop(self, intro)
            except CliHelpException:
                pass
            except QuitException:
                break
            except KeyboardInterrupt:
                break
            except CliAttachError:
                print("You must attach to a session")
                continue
            except CliArgsException as e:
                print("Error parsing arguments!\n %s" % e)
                continue
            except Exception as e:
                print("Error: %s" % e)
                continue

        if self.lr_session:
            self.lr_session.close()

    def _quit(self):
        raise QuitException("quit")

    def _is_path_absolute(self, path):

        if path.startswith('\\\\'):
            return True

        if (path[0].isalpha() and path[1:3] == ':\\'):
            return True

        return False

    def _is_path_drive_relative(self, path):

        if path == '\\':
            return True

        if path[0] == '\\' and path[1] != '\\':
            return True

        return False

    def _file_path_fixup(self, path):
        '''
        We have a pseudo-cwd that we use to
        base off all commands.  This means we
        need to figure out if a given path is relative,
        absolute, or file relative and calculate against
        the pseudo cwd.

        This function takes in a given file path arguemnt
        and performs the fixups.
        '''

        if (self._is_path_absolute(path)):
            return path
        elif (self._is_path_drive_relative(path)):
            return self.cwd[:2] + path
        else:
            return ntpath.join(self.cwd + '\\', path)

    def _stat(self, path):
        '''
        Look to see if a given path exists
        on the sensor and whether that is a
        file or directory.

        :param path: a sensor path
        :return: None, "dir", or "file"
        '''
        if path.endswith('\\'):
            path = path[:-1]

        ret = self.lr_session.list_directory(path)
        if not ret or not len(ret):
            return None

        if 'DIRECTORY' in ret[0]['attributes']:
            return "dir"
        else:
            return "file"

    ################################
    # pseudo commands and session commands
    #
    # they don't change state on the sensor
    # (except start a session)
    #####################

    def _needs_attached(self):
        if not self.lr_session:
            raise CliAttachError()

    def do_cd(self, line):
        '''
        Pseudo Command: cd

        Description:
        Change the psuedo current working directory

        Note: The shell keeps a pseudo working directory
        that allows the user to change directory without
        changing the directory of the working process on sensor.

        Args:
        cd <Directory>
        '''
        self._needs_attached()

        path = self._file_path_fixup(line)
        path = ntpath.abspath(path)
        type = self._stat(path)
        if (type != "dir"):
            print("Error: Path %s does not exist" % path)
            return
        else:
            self.cwd = path

        # cwd never has a trailing \
        if self.cwd[-1:] == '\\':
            self.cwd = self.cwd[:-1]

        log.info("Changed directory to {0}".format(self.cwd))

    def do_cat(self, line):
        self._needs_attached()
        gfile = self._file_path_fixup(line)
        shutil.copyfileobj(self.lr_session.get_raw_file(gfile), sys.stdout)

    def do_pwd(self, line):
        '''
        Pseudo Command: pwd

        Description:
        Print the pseudo current working directory

        Note: The shell keeps a pseudo working directory
        that allows the user to change directory without
        changing the directory of the working process on sensor.

        Args:
        pwd

        '''

        self._needs_attached()

        if (len(self.cwd) == 2):
            # it's c: - put a slash on the end
            print(self.cwd + '\\')
        else:
            print(self.cwd)
        print("")

    def do_connect(self, line):
        """
        Command: connect

        Description:
        Connect to a sensor given the sensor ID or the sensor hostname.

        Args:
        connect SENSOR_ID | SENSOR_HOSTNAME
        """
        if not line:
            raise CliArgsException("Need argument: sensor ID or hostname")

        sensor = self.connect_callback(self.cb, line)
        self.lr_session = sensor.lr_session()

        print("Session: {0}".format(self.lr_session.session_id))
        print("  Available Drives: %s" % ' '.join(self.lr_session.session_data.get('drives', [])))

        # look up supported commands
        print("  Supported Commands: %s" % ', '.join(self.lr_session.session_data.get('supported_commands', [])))
        print("  Working Directory: %s" % self.cwd)

        log.info("Attached to sensor {0}".format(sensor._model_unique_id))

    def do_detach(self, line):
        self.reset()

    def reset(self):
        self.cwd = "c:"

        if not self.lr_session:
            return

        self.lr_session.close()
        self.lr_session = None

    #############################
    # real commands
    #
    # these change state on the senesor
    ##############################

    def do_archive(self, line):
        filename = line
        shutil.copyfileobj(self.lr_session.get_session_archive(), open(filename, "wb+"))

    def do_ps(self, line):
        '''
        Command: ps

        Description:
        List the processes running on the sensor.

        Args:
        ps [OPTIONS]

        OPTIONS:
        -v  - Display verbose info about each process
        -p <Pid> - Display only the given pid
        '''
        self._needs_attached()

        p = CliArgs(usage='ps [OPTIONS]')
        p.add_option('-v', '--verbose', default=False, action='store_true',
                     help='Display verbose info about each process')
        p.add_option('-p', '--pid', default=None, help='Display only the given pid')
        (opts, args) = p.parse_line(line)

        if opts.pid:
            opts.pid = int(opts.pid)

        processes = self.lr_session.list_processes()

        for p in processes:
            if (opts.pid and p['pid'] == opts.pid) or opts.pid is None:
                if opts.verbose:
                    print("Process: %5d : %s" % (p['pid'], ntpath.basename(p['path'])))
                    print("  Guid:        %s" % p['proc_guid'])
                    print("  CreateTime:  %s (GMT)" % self._time_dir_gmt(p['create_time']))
                    print("  ParentPid:   %d" % p['parent'])
                    print("  ParentGuid:  %s" % p['parent_guid'])
                    print("  SID:         %s" % p['sid'].upper())
                    print("  UserName:    %s" % p['username'])
                    print("  ExePath:     %s" % p['path'])
                    print("  CommandLine: %s" % p['command_line'])
                    print("")
                else:
                    print("%5d  %-30s %-20s" % (p['pid'], ntpath.basename(p['path']), p['username']))

        if not opts.verbose:
            print("")

    def do_exec(self, line):
        '''
        Command: exec

        Description:
        Execute a process on the sensor.  This assumes the executable is
        already on the sensor.

        Args:
        exec [OPTS] [process command line and arguments]

        where OPTS are:
         -o <OutputFile> - Redirect standard out and standard error to
              the given file path.
         -d <WorkingDir> - Use the following directory as the process working
              directory
         -w - Wait for the process to complete execution before returning.
        '''

        self._needs_attached()
        # note: option parsing is VERY specific to ensure command args are left
        # as untouched as possible

        OPTS = ['-o', '-d', '-w']
        optOut = None
        optWorkDir = None
        optWait = False

        parts = line.split(' ')
        doParse = True
        while (doParse):
            tok = parts.pop(0)
            if (tok in OPTS):
                if tok == '-w':
                    optWait = True
                if tok == '-o':
                    optOut = parts.pop(0)
                if tok == '-d':
                    optWorkDir = parts.pop(0)
            else:
                doParse = False

        exe = tok

        # ok - now the command (exe) is in tok
        # we need to do some crappy path manipulation
        # to see what we are supposed to execute
        if (self._is_path_absolute(exe)):
            pass
            # do nothing
        elif (self._is_path_drive_relative(exe)):
            # append the current dirve
            exe = self.cwd[:2] + exe
        else:
            # is relative (2 sub-cases)
            ret = self._stat(ntpath.join(self.cwd, exe))
            if (ret == "file"):
                # then a file exist in the current working
                # directory that matches the exe name - execute it
                exe = ntpath.join(self.cwd, exe)
            else:
                # the cwd + exe does not exist - let windows
                # resolve the path
                pass

        # re-format the list and put tok at the front
        if (len(parts) > 0):
            cmdline = exe + ' ' + ' '.join(parts)
        else:
            cmdline = exe

        if not optWorkDir:
            optWorkDir = self.cwd

        ret = self.lr_session.create_process(cmdline, wait_for_output=optWait, remote_output_file_name=optOut,
                                             working_directory=optWorkDir)

        if (optWait):
            print(ret)

    def do_get(self, line):
        '''
        Command: get

        Description:
        Get (copy) a file, or parts of file, from the sensor.

        Args:
        get [OPTIONS] <RemotePath> <LocalPath>

        where OPTIONS are:
        -o, --offset : The offset to start getting the file at
        -b, --bytes : How many bytes of the file to get.  The default is all bytes.
        '''
        self._needs_attached()

        p = CliArgs(usage='get [OPTIONS] <RemoteFile> <LocalFile>')
        (opts, args) = p.parse_line(line)

        if len(args) != 2:
            raise CliArgsException("Wrong number of args to get command")

        with open(args[1], "wb") as fout:
            gfile = self._file_path_fixup(args[0])
            shutil.copyfileobj(self.lr_session.get_raw_file(gfile), fout)

    def do_del(self, line):
        '''
        Command: del

        Description:
        Delete a file on the sensor

        Args:
        del <FileToDelete>
        '''

        self._needs_attached()

        if line is None or line == '':
            raise CliArgsException("Must provide argument to del command")

        path = self._file_path_fixup(line)
        self.lr_session.delete_file(path)

    def do_mkdir(self, line):
        '''
        Command: mkdir

        Description:
        Create a directory on the sensor

        Args:
        mdkir <PathToCreate>
        '''

        self._needs_attached()

        if line is None or line == '':
            raise CliArgsException("Must provide argument to mkdir command")

        path = self._file_path_fixup(line)
        self.lr_session.create_directory(path)

    def do_put(self, line):
        '''
        Command: put

        Description
        Put a file onto the sensor

        Args:
        put <LocalFile> <RemotePath>
        '''
        self._needs_attached()

        argv = split_cli(line)

        if len(argv) != 2:
            raise CliArgsException("Wrong number of args to put command (need 2)")

        with open(argv[0], "rb") as fin:
            self.lr_session.put_file(fin, argv[1])

    def _time_dir_gmt(self, unixtime):
        return time.strftime("%m/%d/%Y %I:%M:%S %p", time.gmtime(unixtime))

    def do_dir(self, line):
        self._needs_attached()

        if line is None or line == '':
            line = self.cwd + "\\"

        path = self._file_path_fixup(line)

        if path.endswith('\\'):
            path += '*'

        ret = self.lr_session.list_directory(path)

        print("Directory: %s\n" % path)
        for f in ret:
            timestr = self._time_dir_gmt(f['create_time'])
            if ('DIRECTORY' in f['attributes']):
                x = '<DIR>               '
            else:
                x = '     %15d' % f['size']
            print("%s\t%s %s" % (timestr, x, f['filename']))

        print("")

    def do_kill(self, line):
        '''
        Command: kill

        Description:
        Kill a process on the sensor

        Args:
        kill <Pid>
        '''

        if line is None or line == '':
            raise CliArgsException("Invalid argument passed to kill (%s)" % line)

        self.lr_session.kill_process(line)

    # call the system shell
    def do_shell(self, line):
        '''
        Command: shell

        Description:
        Run a command locally and display the output

        Args:
        shell <Arguments>
        '''
        print(subprocess.Popen(line, shell=True, stdout=subprocess.PIPE).stdout.read())

    # quit handlers
    def do_exit(self, line):
        return self._quit()

    def do_quit(self, line):
        return self._quit()

    def do_EOF(self, line):
        return self._quit()


def connect_callback(cb, line):
    try:
        sensor_id = int(line)
    except ValueError:
        sensor_id = None

    if not sensor_id:
        q = cb.select(Device).where("hostNameExact:{0}".format(line))
        sensor = q.first()
    else:
        sensor = cb.select(Device, sensor_id)

    return sensor


def main():
    parser = build_cli_parser("Carbon Black Cloud Live Response CLI")
    parser.add_argument("--log", help="Log activity to a file", default='')
    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    if args.log:
        file_handler = logging.FileHandler(args.log)
        file_handler.setLevel(logging.DEBUG)
        log.addHandler(file_handler)

    cli = CblrCli(cb, connect_callback)
    cli.cmdloop()


if __name__ == "__main__":
    sys.exit(main())
