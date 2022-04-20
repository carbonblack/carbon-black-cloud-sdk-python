# *******************************************************
# Copyright (c) VMware, Inc. 2021-2022. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""
The following API calls are tested in this script.

For the validation CBC SDK Select are used.

To execute, a profile must be provided using the standard CBC Credentials.

Reputation Override:
* Configure Reputation Override
* Get Reputation Override
* Delete Reputation Override
* Search Reputation Overrides
* Bulk Delete Reputation Overrides

"""

# Standard library imports
import pytest
import sys

# Internal library imports
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import ReputationOverride
from cbc_sdk.errors import ObjectNotFoundError


def main():
    """Script entry point"""
    global ORG_KEY
    global HOSTNAME
    parser = build_cli_parser()
    args = parser.parse_args()
    print_detail = args.verbose

    if print_detail:
        print(f"profile being used is {args.__dict__}")

    cb = get_cb_cloud_object(args)

    ReputationOverride.create(cb, {
        "description": "An override for a sha256 hash",
        "override_list": "BLACK_LIST",
        "override_type": "SHA256",
        "sha256_hash": "af62e6b3d475879c4234fe7bd8ba67ff6544ce6510131a069aaac75aa92aee7a",
        "filename": "foo.exe"
    })

    sha256_override = cb.select(ReputationOverride) \
                        .where("foo*") \
                        .set_override_list("BLACK_LIST") \
                        .set_override_type("SHA256") \
                        .sort_by("create_time", "desc") \
                        .first()

    assert sha256_override.sha256_hash == "af62e6b3d475879c4234fe7bd8ba67ff6544ce6510131a069aaac75aa92aee7a"
    assert sha256_override.filename == "foo.exe"
    print('Configure Reputation Override - SHA256 .......OK')
    print('Search Reputation Overrides - SHA256 .........OK')

    override_by_id = cb.select(ReputationOverride, sha256_override.id)

    assert override_by_id.id == sha256_override.id
    assert override_by_id.sha256_hash == sha256_override.sha256_hash
    print('Get Reputation Override ......................OK')

    sha256_override.delete()

    delete_query = cb.select(ReputationOverride) \
                     .where("foo") \
                     .set_override_list("BLACK_LIST") \
                     .set_override_type("SHA256") \
                     .sort_by("create_time", "desc")

    assert len(delete_query) == 0
    print('Delete Reputation Override ...................OK')

    caught = False
    try:
        sha256_override.delete()
    except ObjectNotFoundError:
        caught = True
    assert caught
    print('Delete Reputation Override - 404 .............OK')

    ReputationOverride.create(cb, {
        "description": "Approved IT Tools",
        "override_list": "WHITE_LIST",
        "override_type": "IT_TOOL",
        "path": "C://tools//*.exe",
        "include_child_processes": True
    })

    it_tool_override = cb.select(ReputationOverride) \
                         .set_override_list("WHITE_LIST") \
                         .set_override_type("IT_TOOL") \
                         .sort_by("create_time", "desc") \
                         .first()

    assert it_tool_override.path == "C://tools//*.exe"
    assert it_tool_override.include_child_processes
    print('Configure Reputation Override - IT_TOOL ......OK')
    print('Search Reputation Overrides - IT_TOOL ........OK')

    ReputationOverride.create(cb, {
        "description": "Approved Certificate",
        "override_list": "WHITE_LIST",
        "override_type": "CERT",
        "signed_by": "VMware Inc.",
        "certificate_authority": "VMware"
    })

    cert_override = cb.select(ReputationOverride) \
                      .set_override_list("WHITE_LIST") \
                      .set_override_type("CERT") \
                      .sort_by("create_time", "desc") \
                      .first()

    assert cert_override.signed_by == "VMware Inc."
    assert cert_override.certificate_authority == "VMware"
    print('Configure Reputation Override - CERT .........OK')
    print('Search Reputation Overrides - CERT ...........OK')

    ReputationOverride.bulk_delete(cb, [it_tool_override.id, cert_override.id])

    with pytest.raises(ObjectNotFoundError):
        cb.select(ReputationOverride, it_tool_override.id)
    with pytest.raises(ObjectNotFoundError):
        cb.select(ReputationOverride, cert_override.id)
    print('Bulk Delete Reputation Overrides .............OK')


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
