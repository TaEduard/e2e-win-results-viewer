import os
from constants import *


def add_matrix_to_dict(path, name, dict):
    if name not in dict:
        dict[name] = path
    return dict

def add_job(name, matrix_dict, config):
    output = "<span style=' margin-left: 10px;' ><a>%s</a></span>" % name
    output += "<span style=' margin-left: 10px;'><a href=%s>MATRIX</a></span>" % os.path.relpath(
            matrix_dict[name], config["outputFolder"])
    return output

def add_jobs(matrix_dict, config):
    output = "<li><ul>"
    for name in matrix_dict:
        output += "<li>%s</li>" % add_job(name, matrix_dict, config)
    output += "</ul></li>"
    return output

def create_landing_page(matrix_dict, config):
    output = "<html><body>Test reports<ul>"
    output += add_jobs(matrix_dict,config)
    output += "</ul></body></html>"
    return output

