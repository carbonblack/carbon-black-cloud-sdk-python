#!/usr/bin/env python
# *******************************************************
# Copyright (c) VMware, Inc. 2020-2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# usage: BiosVerification.py [-h] [-m MACHINENAME] [-g] [-o ORGPROFILE]
# optional arguments:
#   -h, --help            show this help message and exit
#   -m MACHINENAME, --machinename MACHINENAME
#                         machinename to run host bios forensics on
#   -g, --get           Get BIOS images
#
#   --profile ORGPROFILE
#                         Select your cbc credential profile

"""Example command-line interface to Live Response."""

import sys
from cbc_sdk.platform import Device
from cbc_sdk.live_response_api import LiveResponseError
from cbc_sdk.helpers import get_cb_cloud_object, build_cli_parser


def live_response(cb, host=None, response=None):
    """Live Response"""
    # Select the device you want to gather forensic data from
    query_hostname = "name:{}".format(host)
    print("[ * ] Establishing LiveResponse Session with Remote Host:")

    # Create a new device object to launch LR on
    device = cb.select(Device).where(query_hostname).first()
    print("     - Hostname: {}".format(device.name))
    print("     - OS Version: {}".format(device.os))
    print("     - Sensor Version: {}".format(device.sensor_version))
    print("     - AntiVirus Status: {}".format(device.av_status))
    print("     - Internal IP Address: {}".format(device.last_internal_ip_address))
    print("     - External IP Address: {}".format(device.last_external_ip_address))
    print()

    # Execute our LR session
    with device.lr_session() as lr_session:
        print("[ * ] Uploading scripts to the remote host")
        # upload the file
        lr_session.put_file(open("dellbios.bat", "rb"), "C:\\Program Files\\Confer\\temp\\dellbios.bat")

        if response == "get":
            print("[ * ] Getting the images")
            result = lr_session.create_process("cmd.exe /c .\\dellbios.bat",
                                               wait_for_output=True,
                                               remote_output_file_name=None,
                                               working_directory="C:\\Program Files\\Confer\\temp\\",
                                               wait_timeout=120,
                                               wait_for_completion=True).decode("utf-8")
            print()
            print("{}".format(result))

            print("[ * ] Removing scripts")
            lr_session.create_process("powershell.exe del .\\dellbios.bat",
                                      wait_for_output=False,
                                      remote_output_file_name=None,
                                      working_directory="C:\\Program Files\\Confer\\temp\\",
                                      wait_timeout=30,
                                      wait_for_completion=False)

            print("[ * ] Downloading images")
            try:
                zipdata = lr_session.get_file("C:\\Program Files\\Confer\\temp\\BiosImages.zip")
                print("[ * ] Writing out " + host + "-BiosImages.zip")
                zipfile = open(host + "-BiosImages.zip", "wb")
                zipfile.write(zipdata)
                print()
            except LiveResponseError as ex:
                if 'ERROR_FILE_NOT_FOUND' in str(ex):
                    print('[ * ] No such file. Skipping get file...')
        else:
            print("[ * ] Nothing to do")

        print("[ * ] Cleaning up")
        lr_session.create_process("powershell.exe del .\\BiosImages.zip",
                                  wait_for_output=False,
                                  remote_output_file_name=None,
                                  working_directory="C:\\Program Files\\Confer\\temp\\",
                                  wait_timeout=30,
                                  wait_for_completion=False)
        lr_session.create_process("powershell.exe del C:\\tmpbios\\*.*",
                                  wait_for_output=False,
                                  remote_output_file_name=None,
                                  working_directory="C:\\Program Files\\Confer\\temp\\",
                                  wait_timeout=30,
                                  wait_for_completion=False)
        print()


def main():
    """Script entry point"""
    parser = build_cli_parser()
    parser.add_argument("-m", "--machinename", help="machinename to run host forensics recon on")
    parser.add_argument("-g", "--get", help="Get the Dell BIOS Verification images", action="store_true")
    args = parser.parse_args()

    # Create the CBCloud
    cb = get_cb_cloud_object(args)

    if args.machinename:
        if args.get:
            live_response(cb, host=args.machinename, response="get")
        else:
            print("Nothing to do...")
    else:
        print("[ ! ] You must specify a machinename with a --machinename parameter."
              " IE ./BiosVerification.py --machinename cheese")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
