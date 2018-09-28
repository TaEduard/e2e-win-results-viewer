import os
from shutil import copy
from subprocess import call
import errno
import re

def delete_files(file_lst):
    for file in file_lst:
        os.remove(file)

def create_file_name(file_name, reg_match, uid, job_counter):
    name_elements = []
    name_elements.append(str(job_counter))
    if isinstance(uid, int):
        name_elements.append(str(uid))
        name_elements.append(file_name)
        name = "_".join(name_elements)
        return name
    if isinstance(uid, list):
        for i in range(len(uid)):
            name_elements.append(reg_match.group(i+1))
    else:
        name_elements.append(reg_match.group(1))
    name_elements.append(file_name)
    name = "_".join(name_elements)
    return name

def find_first(regex_pattern, s):
    result = re.findall(regex_pattern, s)
    if len(result)>0:
       return result[0]

def format_regex(regex_string):
    if regex_string[len(regex_string)-1] == "/":
       regex_string = regex_string[:-1]
    return regex_string.replace("/","\/").replace(".","\.").replace("*",".*")

def format_list(lst):
    for index, item in enumerate(lst):
        lst[index] = item.replace("%(","").replace(")s","")
    return lst

def convert_list_to_regex(lst):
    regex_str = "|".join(lst)
    regex_str = "".join(["(", regex_str, ")"])
    regex_str = format_regex(regex_str)
    return regex_str

def get_file_name_regex(job, path_cotained_keys):
    if isinstance(job[path_cotained_keys[len(path_cotained_keys)-1]], list):
        return convert_list_to_regex(job[path_cotained_keys[len(path_cotained_keys)-1]])
    return job[path_cotained_keys[len(path_cotained_keys)-1]]

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
