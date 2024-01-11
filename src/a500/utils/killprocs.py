#!/usr/bin/env python
"""
   example:

   killprocs python

   will kill all processes with python in the name

   requires:
      
      conda install psutil
"""
import psutil
from .helper_funs import make_tuple

import argparse
import textwrap


def on_terminate(proc):
    print("process {} terminated with exit code {}".format(
               proc, proc.returncode))

def make_parser():
    linebreaks = argparse.RawTextHelpFormatter
    descrip = textwrap.dedent(globals()['__doc__'])
    parser = argparse.ArgumentParser(formatter_class=linebreaks,
                                     description=descrip)
    parser.add_argument('snip', type=str, help='string in processname')
    return parser

def main(args=None):
    """
    args: optional -- if missing then args will be taken from command line
          or pass [snippet] -- string to search for in processes
    """
    parser = make_parser()
    args = parser.parse_args(args)
    keepit = {}
    keys = ['time', 'name', 'cmdline', 'proc']
    for proc in psutil.process_iter():
        try:
            the_dict = dict(zip(keys, (proc.create_time(), proc.exe(),
                                       proc.cmdline(), proc)))
            keepit[proc.pid] = make_tuple(the_dict)
        except (psutil.ZombieProcess, psutil.AccessDenied,
                psutil.NoSuchProcess):
            pass
        except FileNotFoundError:
            pass
    print(f'in killprocs, looking for {args.snip}')
    #
    # don't kill this process or the emacs python parser
    #
    proclist = []
    cmdlist = []
    for the_tup in keepit.values():
        string_cmd = ' '.join(the_tup.cmdline)
        if string_cmd.find(args.snip) > -1 and \
           string_cmd.find('killprocs') == -1 and \
           string_cmd.find('elpy') == -1:
            proclist.append(the_tup)
            cmdlist.append(string_cmd)

    proconly = [item.proc for item in proclist]
    good_procs=[]
    for the_proc,the_cmd in zip(proconly,cmdlist):
        try:
            the_proc.terminate()
            good_procs.append(the_proc)
            cmd_string = ' '.join(the_proc.cmdline())
            print(f'terminating: {the_cmd}')
        except:
            pass

    gone, alive = psutil.wait_procs(good_procs, timeout=3, callback=on_terminate)

    for p in alive:
        p.kill()


if __name__ == "__main__":

    main()
    
