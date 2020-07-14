#!/usr/bin/env python3

from __future__ import absolute_import
import sys


def convert_query_params(qd):
    o = []
    for k, v in iter(qd.items()):
        if type(v) == list:
            for item in v:
                o.append((k, item))
        else:
            o.append((k, v))

    return o
