#!/bin/python
# pylint: disable=too-few-public-methods, missing-docstring, C0413
# -----------------------------------------------------------------------------
# Darkstorm Library
# Copyright (C) 2021 Martin Slater
# Created : Wednesday, 01 December 2021 09:06:27 AM
# -----------------------------------------------------------------------------
"""
Paralenz movie combiner command line tool.
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import argparse
import codecs
import datetime
import glob
import os

import ffmpeg
from pymediainfo import MediaInfo
from datetime import timedelta
from datetime import datetime

# -----------------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------------


class ParalenzRecombine(object):
    """ MapCreate """

    def __init__(self, args):
        """ Constructor """
        self.source_dir = os.path.abspath(args.source_dir)
        pass

    def run(self):
        filenames = [f for f in glob.glob(
            f'{self.source_dir}/*.mp4') if 'LOWRES' not in f]

        # filenames.sort()
        # for f in filenames:
        #     print(f)

        files = []
        for f in filenames:
            media_info = MediaInfo.parse(f)
            duration_in_ms = media_info.tracks[0].duration
            if duration_in_ms is not None and len(media_info.general_tracks):
                encoded_date = datetime.strptime(
                    media_info.general_tracks[0].encoded_date[4:], '%Y-%m-%d %H:%M:%S')
                files.append(
                    {
                        'name': f,
                        'mtime': datetime.utcfromtimestamp(os.stat(f).st_mtime),
                        'stime': encoded_date,
                        'duration': duration_in_ms // 1000,
                        'media_info': media_info,
                        'etime': encoded_date + timedelta(seconds=duration_in_ms // 1000)
                    })

        groups = []
        last_file = None
        for f in files:
            # print(f['stime'], f['etime'], "" if not last_file else (
            #     f['stime'] - last_file['etime']).seconds)
            new_group = False
            if len(groups) == 0 or last_file == None:
                new_group = True
            elif last_file != None and (f['stime'] - last_file['etime']).seconds > 300:
                new_group = True

            if new_group:
                groups.append([f])
            else:
                groups[-1].append(f)
            last_file = f

        fname_index = 0
        for g in groups:
            len_mins = int(
                (g[-1]['etime'] - g[0]['stime']).total_seconds() // 60)
            print(
                f'Processing group {fname_index} : {len(g)} files : {len_mins} mins ')
            group_file = 'filelist.txt'
            with codecs.open(group_file, 'w', 'utf-8') as of:
                for f in g:
                    name = f['name'].replace('\\', '\\\\')
                    of.write(f"file '{name}'\n")

            output_dir = os.path.join(self.source_dir, "grouped")
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            output_name = str(g[0]['stime']).replace(':', '.')
            output_file = os.path.join(output_dir, f'{output_name}.mp4')
            if os.path.exists(output_file):
                os.remove(output_file)
            ffmpeg.input(group_file, format='concat', safe=0).output(
                output_file, c='copy').run(quiet=True)
            fname_index += 1

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    """ Main script entry point """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_dir', metavar='D', type=str,
                        help='Input source directory. Should be the sdcard/DCIM/100PRLNZ directory.')
    args = parser.parse_args()
    ParalenzRecombine(args).run()


if __name__ == "__main__":
    main()
