#!/usr/bin/env python
import re


def get_bare_principal(normalized_principal_name):

    bare_principal = None

    if normalized_principal_name:
        match = re.match(r"([^/@]+)(?:/[^@])?(?:@.*)?",
                         normalized_principal_name)

    if match:
        bare_principal = match.group(1)

    return bare_principal
