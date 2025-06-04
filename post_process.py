"""This goes on the shelf tool:"""
import hou
import os
import glob
import sys
import re
import gzip

def __tnamecomponent(node, index):
    try:
        return node.type().nameComponents()[index]
    except AttributeError:
        return node.nameComponents()[index]

def coretname(node):
    return __tnamecomponent(node, 2)

selected = hou.selectedNodes()
for node in selected:
    if coretname(node) == "smart_ass":
        node.parm('postframe').set('/psyop/pfs/projects/drmgamsroyal2023_42330P/code/primary/addons/houdini/scripts/post_process.py')

"""This goes in the py file:"""

import gzip
import sys

import hou


def _set_scene_scale_in_ass_file(ass_file_path, meters_per_unit="0.01"):
    """Replace the `meters_per_unit` value in the metadata header of the ass file.

    The `meters_per_unit` metadata line is expected to be found within the first
    50 lines of data.

    """
    NB_HEADER_LINES = 50
    SCENE_SCALE_TOKEN = b"### meters_per_unit: "
    patched_scene_scale = f"### meters_per_unit: {meters_per_unit}\n".encode("utf-8")

    file_open = gzip.open if ass_file_path.lower().endswith(".gz") else open

    header_lines = []
    with file_open(ass_file_path, "rb") as f:
        for _ in range(NB_HEADER_LINES):
            line = f.readline()
            if line.startswith(SCENE_SCALE_TOKEN):
                header_lines.append(patched_scene_scale)
                break
            header_lines.append(line)

        remaining_data = f.read()

    with file_open(ass_file_path, "wb") as f:
        for line in header_lines:
            f.write(line)
        f.write(remaining_data)


def _log_line(line):
    """Log a message to stderr."""
    sys.stderr.write(f"Arnold ROP Post Process: {line}\n")


def main():
    """"""
    ass_file_path = hou.pwd().evalParm("ar_ass_file")
    _log_line(f"Setting 'meters_per_unit' to \"0.01\" for: '{ass_file_path}'")

    _set_scene_scale_in_ass_file(
        ass_file_path,
        meters_per_unit="0.01",
    )

    _log_line("Done")


main()
