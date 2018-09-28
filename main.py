import config_parser
import os
from utils import *
from junit import *
from landingpage import *
import re

LANDING_PAGE_NAME = "index.html"

config = config_parser.readConfig()

def format_path(job,job_counter):
    job_keys = format_list(re.findall("\%\(.*?\)s", job["jobResultsDir"]))
    job_keys_dict = {}
    for key in job_keys:
        if key not in job:
            print("".join(["\n For job: ", str(job_counter), " no key: ", key, " was declared."]))
            return None, None, None
        if isinstance(job[key], list):
             job_keys_dict[key] = convert_list_to_regex(job[key])
        else:
             if "uid" in job and key in job["uid"]:
                 job_keys_dict[key] = "".join(["(", job[key], ")"])
             else:
                 job_keys_dict[key] = job[key]
    path = regex = job["jobResultsDir"] % job_keys_dict
    path = path.split("*")[0]
    path = path.split("(")[0]
    return regex, path, job_keys

def walk_path(job, outputfolder, counter, matrix_dict, job_counter):
    regex, path, keys = format_path(job, job_counter)
    if path is None:
        return matrix_dict
    path_list=[]
    for root, dirs, files in os.walk(path, topdown=False):
        files_in_current_dir = '\n'.join(files)
        file_matches = re.findall(format_regex(get_file_name_regex(job, keys)), files_in_current_dir)
        path_match = re.match(format_regex(regex.replace(get_file_name_regex(job, keys), "")), root)
        if path_match and file_matches:
            if len(file_matches)>1:
                tbm_list=[]
                for match in file_matches:
                    tbm_list.append(os.path.join(root, match))
                if counter>0:
                    file_path=os.path.join(root, create_file_name(file_matches[0], path_match, counter, job_counter))
                    counter+=1
                else:
                    file_path=os.path.join(root, create_file_name(file_matches[0], path_match, job["uid"], job_counter))
                merge_test_cases(tbm_list, file_path, show_skipped=False)
                del tbm_list
                path_list.append(file_path)
            else:
                if counter>0:
                    file_path=os.path.join(root, create_file_name(file_matches[0], path_match, counter, job_counter))
                    counter+=1
                else:
                    file_path=os.path.join(root, create_file_name(file_matches[0], path_match, job["uid"], job_counter))
                copy_ensure_path(os.path.join(root, file_matches[0]), file_path)
                path_list.append(file_path)
    if path_list:
        if "id" in job and job["id"]:
            matrix_output_name_path = matrix_output_name = "".join([job["id"], "matrix.html"])
        else:
            matrix_output_name = "".join([str(job_counter), path, "matrix.html"])
            matrix_output_name_path = matrix_output_name.replace("/", "_")
        if "outputFolder" in job and job["outputFolder"]:
            create_matrix(path_list, os.path.join(job["outputFolder"], matrix_output_name_path))
            relative_path = os.path.join(job["outputFolder"], matrix_output_name_path)
            matrix_dict = add_matrix_to_dict(os.path.join(job["outputFolder"], matrix_output_name_path),
                                              matrix_output_name, matrix_dict)
        elif outputfolder:
            create_matrix(path_list, os.path.join(outputfolder, matrix_output_name_path))
            matrix_dict = add_matrix_to_dict(os.path.join(outputfolder, matrix_output_name_path),
                                              matrix_output_name, matrix_dict)
        else:
            print("".join(["\n For job: ", str(job_counter), "no outputFolder provided"]))
    else:
        print("".join(["\n For job: ", str(job_counter), " bad path"]))
    delete_files(path_list)
    return matrix_dict

def process_jobs(matrix_dict, job_counter):
    for job in config["jobs"]:
        job_counter+=1
        counter = 0
        if "uid" not in job:
            counter+=1
        matrix_dict = walk_path(job, config["outputFolder"], counter, matrix_dict, job_counter)
    return matrix_dict

def main():
    matrix_dict = {}
    job_counter = 0
    matrix_dict = process_jobs(matrix_dict, job_counter)
    lp = create_landing_page(matrix_dict, config)
    write_with_ensure_path(lp, os.path.join(config["outputFolder"], LANDING_PAGE_NAME))

main()
