# -*- coding: utf-8 -*-
# 
# # MIT License
# 
# Copyright (c) 2019 Mike Simms
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import sys
import xml.etree.ElementTree as ET
import ZwoTags

class ZwoReader():

    def __init__(self):
        self.author = ""
        self.name = ""
        self.description = ""
        self.sport_type = ""
        self.tags = []
        self.workout = []

    def parse_tags(self, node):
        for item in node.getchildren():
            self.tags.append(item.attrib)

    def parse_workout(self, node):
        for item in node.getchildren():
            attributes = {}
            attributes['workout type'] = item.tag
            for subitem in item.items():
                attributes[subitem[0]] = subitem[1]
            children = []
            for child in item.getchildren():
                children.append(child.attrib)
            attributes['children'] = children
            self.workout.append(attributes)

    def parse_workout_file(self, node):
        """Parses the workout file starting from the root node."""
        for item in node.getchildren():
            if item.tag == ZwoTags.ZWO_TAG_NAME_AUTHOR:
                self.author = node.text
            elif item.tag == ZwoTags.ZWO_TAG_NAME_NAME:
                self.name = node.text
            elif item.tag == ZwoTags.ZWO_TAG_NAME_DESCRIPTION:
                self.description = node.text
            elif item.tag == ZwoTags.ZWO_TAG_NAME_SPORT_TIME:
                self.sport_type = node.text
            elif item.tag == ZwoTags.ZWO_TAG_NAME_TAGS:
                self.parse_tags(item)
            elif item.tag == ZwoTags.ZWO_TAG_NAME_WORKOUT:
                self.parse_workout(item)

    def read_file(self, file_name):
        """Parses the file specified by the given name."""
        tree = ET.parse(file_name)
        root = tree.getroot()
        if root.tag == ZwoTags.ZWO_TAG_NAME_FILE:
            self.parse_workout_file(root)

def main():
    """Entry point when running the application from the command line."""

    # Parse command line options.
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="", help="File to parse", required=True)

    try:
        args = parser.parse_args()
    except IOError as e:
        parser.error(e)
        sys.exit(1)

    if len(args.file) == 0:
        sys.exit(1)

    reader = ZwoReader()
    reader.read_file(args.file)
    print(reader.workout)

if __name__ == '__main__':
    main()
