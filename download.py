# coding: UTF-8
import os
import sys
import argparse
import subprocess
import glob

from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed

import csv

def s2m(s):

    hour = s // 3600
    min = (s+3600) % 3600 // 60
    sec = s % 60

    return "{0:02d}:{1:02d}:{2:02d}".format(hour, min, sec)

def trim(basename, name, start, end):

    t  = start
    ss = end - start

    t = s2m(t)
    ss = s2m(ss)

    ff_code = 'ffmpeg -ss ' + ss + ' -t ' + t + ' -strict -2 -i ' + basename + '.mp4 ' + name
    print(ff_code)
    subprocess.call(ff_code, shell=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='download-youtube-movie')
    parser.add_argument('-csv', '-c', type=str, required=True)
    parser.add_argument('-output_all', '-oa', type=str, required=True)
    parser.add_argument('-output_trim', '-ot', type=str, required=True)
    args = parser.parse_args()

    os.makedirs(args.output_all, exist_ok=True)
    os.makedirs(args.output_trim, exist_ok=True)

    # open csv file
    csv_file = open(args.csv, "r", encoding="UTF-8", errors="", newline="" )
    f = csv.reader(csv_file, delimiter=",", doublequote=True, skipinitialspace=True)
    header = next(f)
    print(header)
    for row in f:
        dl_basename = os.path.join(args.output_all, "{0:04d}".format(int(row[0])))
        dl_trimname = os.path.join(args.output_trim, "{0:04d}".format(int(row[0])))
        dl_url = row[1]
        times = [int(x.split(":")[0])*60+int(x.split(":")[1]) for x in row[4:] if x]

        base_movies = glob.glob(args.output_all + "/*")
        if not (dl_basename+".mp4") in base_movies:
            code = "youtube-dl "
            code += dl_url
            code += " -f mp4 -i -o "
            code += "{}".format(dl_basename)
            code += ".mp4"
            print(code)
            try:
                subprocess.call(code, shell=True)
            except:
                print(sys.exc_info())
        else:
            print('-------------------------------------------')
            print('/// skip download: ', dl_basename+".mp4")

        for idx in range(len(times)//2):
            start = times[2*idx]
            end = times[2*idx+1]

            dl_name = "{0}_{1}.mp4".format(dl_trimname, idx+1)

            trim_movies = glob.glob(args.output_trim + "/*")
            if not dl_name in trim_movies:
                try:
                    trim(dl_basename, dl_name, start, end)
                except:
                    print(sys.exc_info())
            else:
                print('-------------------------------------------')
                print('/// skip trim: ', dl_name)

            print('-------------------------------------------')
            print("/// downloaded:", dl_url)
            print("/// file_path:", dl_name)

