import config_parser
import os
from constants import *
from utils import *
from junit import *
from landingpage import *
import re

config = config_parser.readConfig()

def get_job_builds(job):
    job_path = job["jobResultsDir"]
    return [path for path in os.listdir(job_path) if os.path.isdir(os.path.join(job_path, path))]


def copy_job_summaries(job):
    for build in get_job_builds(job):
        source_path = os.path.join(job['jobResultsDir'],
                                   JOB_BUILD_SUMMARY_SOURCE_PATH % {"build": build})
        destination_path = os.path.join(config['outputFolder'],
                                        JOB_SUMMARY_RAW_RESULTS_PATH % {"job_name": job["jobName"]},
                                        "%s.xml" % build )
        if os.path.exists(source_path):
            copy_ensure_path(source_path, destination_path)

def create_job_summary_matrix(job):
    job_report_path = os.path.join(config['outputFolder'],
                                   JOB_SUMMARY_RAW_RESULTS_PATH % {"job_name": job['jobName']})
    reports = [report for report in os.listdir(job_report_path) if report.endswith("xml")]
    reports_paths = [os.path.join(job_report_path, report) for report in reports]
    matrix_output_dir = os.path.join(
        config['outputFolder'], JOB_SUMMARY_MATRIX_PATH % {"job_name": job["jobName"]}
    )
    matrix_output_name = JOB_SUMMARY_MATRIX_NAME % {"job_name": job["jobName"]}
    create_matrix(reports_paths, os.path.join(matrix_output_dir, matrix_output_name))

def copy_job_test_results(job):
    regex = re.compile(JOB_BUILD_TEST_REGEX)
    for build in get_job_builds(job):
        source_dir = os.path.join(job['jobResultsDir'],
                                   JOB_BUILD_TEST_SOURCE_DIR % {"build": build})
        destination_dir = os.path.join(config['outputFolder'],
                                     JOB_TEST_RAW_RESULTS_PATH % {"job_name": job["jobName"]})
        build_test_results = []
        for path in os.listdir(source_dir):
            m = regex.match(path)
            if m:
                build_test_results.append(os.path.join(source_dir, path))
        merge_path = os.path.join(destination_dir, "%s.xml" % build)
        merge_test_cases(build_test_results, merge_path, show_skipped=False)

def create_job_test_matrix(job):
    job_report_path = os.path.join(config['outputFolder'],
                                   JOB_TEST_RAW_RESULTS_PATH % {"job_name": job['jobName']})
    reports = [report for report in os.listdir(job_report_path) if report.endswith("xml")]
    reports_paths = [os.path.join(job_report_path, report) for report in reports]
    matrix_output_dir = os.path.join(
        config['outputFolder'], JOB_TEST_MATRIX_PATH % {"job_name": job["jobName"]}
    )
    matrix_output_name = JOB_TEST_MATRIX_NAME % {"job_name": job["jobName"]}
    create_matrix(reports_paths, os.path.join(matrix_output_dir, matrix_output_name))


def process_postsubmits():
    pass

def process_presubmits():
    pass

def process_periodics():
    for job in config["jobs"]["periodics"]:
        copy_job_summaries(job)
        copy_job_test_results(job)
        create_job_summary_matrix(job)
        create_job_test_matrix(job)

job_handler_map = {
    'periodic': process_periodics,
    'presubmit': process_presubmits,
    'postsubmit': process_postsubmits
}

def process_jobs():
    for job_type in JOB_TYPES:
        job_handler_map[job_type]()

def main():
    #process_jobs()
    pl = create_landing_page(config["jobs"])
    write_with_ensure_path(pl, os.path.join(config["outputFolder"], LANDING_PAGE_NAME))


main()