#!/usr/bin/env python3
#(C) Copyright Syd Logan 2026
#(C) Copyright Thousand Smiles Foundation 2026
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

"""Stream a mysqldump and omit log tables (schema + data).

Only log/audit tables are skipped; the application remains unchanged.
Skipped tables are created empty later via Django migrate.
"""
from __future__ import annotations

import re
import sys

# Log tables commonly omitted from restore (too large or not needed).
SKIP_TABLES = frozenset(
    {
        "requestlog_requestlog",  # API request log (very large)
        "django_admin_log",       # Django admin action history
    }
)

TABLE_STRUCTURE_RE = re.compile(r"Table structure for table `([^`]+)`")


def filter_sql(lines):
    skip_section = False

    for line in lines:
        structure_match = TABLE_STRUCTURE_RE.search(line)
        if structure_match:
            table = structure_match.group(1)
            skip_section = table in SKIP_TABLES
            if skip_section:
                continue

        if skip_section:
            if "UNLOCK TABLES" in line:
                skip_section = False
            continue

        yield line


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} dump.sql", file=sys.stderr)
        return 1

    print(
        f"# Skipping log tables: {', '.join(sorted(SKIP_TABLES))}",
        file=sys.stderr,
    )

    with open(sys.argv[1], "r", encoding="utf-8", errors="replace") as infile:
        sys.stdout.writelines(filter_sql(infile))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
