import os
from shutil import copy
from subprocess import call
import errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def copy_ensure_path(src, dst):
    mkdir_p(os.path.dirname(dst))
    copy(src, dst)

def create_matrix(reports, matrix_path):
    # ensure destination
    mkdir_p(os.path.dirname(matrix_path))
   # print "calling with args %s %s" % (reports, matrix_path)
    call(["junit2html", "--report-matrix=%s" % matrix_path ] + reports)

def write_with_ensure_path(content, dst):
    mkdir_p(os.path.dirname(dst))
    with open(dst, "w+") as filedesc:
        filedesc.write(content)