import argparse
import time
import os
import subprocess
import sys
import logging

CC = "gcc"
CFLAGS = ["-Wall", "-Wno-endif-labels", "-lpcap"]

rel_loc = "../../resources/course/DevOps/sniffex.c"


parser = argparse.ArgumentParser("python3 compile_sniffex.py",
        usage="[-o filename] [--clean]")

parser.add_argument("-d", "--debug", action="store_true", help="compile with debugging")

parser.add_argument("-v", "--valgrind", action="store_true", help="compile and then check with valgrind")

parser.add_argument("-o", "--output", type=str, metavar="", help="output filename", default="sniffex.x")

parser.add_argument("--clean", action="store_true", help="wipe all *.x files and log files")

args = parser.parse_args()

if args.clean:
    os.system("rm ./*x")
    os.system("rm -r ./logs")
    sys.exit(0)

val_status = None

status=0
err_msg=None

try: 
    build_status = subprocess.run([
        CC,
        "-o",
        args.output,
        rel_loc,
    ] + CFLAGS, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    status = build_status.returncode

    if status == 0 and args.valgrind:
        val_status = subprocess.run([
            "valgrind",
            "--tool=memcheck",
            "--leak-check=yes",
            "--show-reachable=yes",
            "--num-callers=20",
            "--track-fds=yes",
            args.output
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = val_status.returncode
except Exception as ex:
    status = -1
    err_msg = repr(ex)

if not os.path.isdir("./logs"):
    os.mkdir("./logs")
with open('./logs/log_'+str(int(time.time())), mode='w') as log_file:
    for val in dir(args):
        if val[0] != '_':
            log_file.write("{}: {}\n".format(val, getattr(args, val)))
    log_file.write("result: {}\n".format(status))
    if status != 0:
        if err_msg:
            log_file.write("\n{}\n".format(err_msg))
        else:
            log_file.write("\n{}\n{}\n{}\n{}\n".format(
            build_status.stderr.decode('ascii'),
            build_status.stdout.decode('ascii'),
            val_status.stderr.decode('ascii') if val_status else "",
            val_status.stdout.decode('ascii') if val_status else ""))
