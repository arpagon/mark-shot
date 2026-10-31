#!/usr/bin/python3
"""Apply narrowly scoped packaging fixes to official v0.1.61 sources."""

import pathlib
import shutil
import sys
import textwrap

source = pathlib.Path(sys.argv[1])
shutil.copyfile(pathlib.Path(__file__).with_name("v0.1.61-smoke"), source / "debian/tests/smoke")
(source / "debian/tests/smoke").chmod(0o755)

rules = source / "debian/rules"
old = "\trm -f debian/mark-shot/usr/share/doc/mark-shot/CHANGELOG.md"
new = (
    "\tchmod 644 debian/mark-shot/usr/libexec/mark-shot/lib/mark_shot_window_detection/*.py\n"
    "\trm -f debian/mark-shot/usr/share/doc/mark-shot/CHANGELOG.md \\\n"
    "\t\tdebian/mark-shot/usr/share/doc/mark-shot/LICENSE"
)
contents = rules.read_text(encoding="utf-8")
if contents.count(old) != 1:
    raise SystemExit("Unexpected v0.1.61 debian/rules layout")
rules.write_text(contents.replace(old, new), encoding="utf-8")

changelog = source / "debian/changelog"
lines = changelog.read_text(encoding="utf-8").splitlines()
changelog.write_text(
    "\n".join(
        textwrap.fill(line[4:], width=79, initial_indent="  * ", subsequent_indent="    ")
        if line.startswith("  * ") and len(line) > 79 else line
        for line in lines
    ) + "\n",
    encoding="utf-8",
)
