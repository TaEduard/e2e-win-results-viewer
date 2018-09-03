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


def create_job_summary_matrix_custom_acs(job):
    summary_res_path = os.path.join(config['outputFolder'], "custom_acs", job['jobName'], "summary_raw_res")
    summary_files = []
    for path in os.listdir(summary_res_path):
        summary_files.append(os.path.join(summary_res_path, path))
    matrix_output_dir = os.path.join(
        config['outputFolder'], 'custom_acs', job["jobName"], 'summary_matrix'
    )
    matrix_output_name = JOB_SUMMARY_MATRIX_NAME % {"job_name": job["jobName"]}
    create_matrix(summary_files, os.path.join(matrix_output_dir, matrix_output_name))


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

def copy_job_summaries_custom_acs(job):
    destination_dir = os.path.join(config["outputFolder"], "custom_acs" , job["jobName"], "summary_raw_res")
    for pr in os.listdir(job["jobResultsDir"]):
        job_path = os.path.join(job["jobResultsDir"], pr, job["jobName"])
        if os.path.exists(job_path):
            for job_id in os.listdir(job_path):
                for build in os.listdir(os.path.join(job_path, job_id)):
                    summary_path = os.path.join(job_path, job_id, build, "artifacts", "junit_runner.xml")
                    destination_path = os.path.join(destination_dir, "%s-%s-%s.xml" % (pr, job_id, build))
                    if os.path.exists(summary_path):
                        copy_ensure_path(summary_path, destination_path)

def copy_job_test_results_custom_acs(job):
    regex = re.compile(JOB_BUILD_TEST_REGEX)
    destination_dir = os.path.join(config['outputFolder'],"custom_acs", job["jobName"], "test_raw_results")
    for pr in os.listdir(job["jobResultsDir"]):
        job_path = os.path.join(job["jobResultsDir"], pr, job["jobName"])
        if os.path.exists(job_path):
            for job_id in os.listdir(job_path):
                for build in os.listdir(os.path.join(job_path, job_id)):
                    build_test_results = []
                    source_path = os.path.join(job_path, job_id, build, "artifacts")
                    if not os.path.exists(source_path):
                        continue
                    for junit_file in os.listdir(source_path):
                        m = regex.match(junit_file)
                        if m:
                            build_test_results.append(os.path.join(source_path, junit_file))
                    merge_path = os.path.join(destination_dir, "%s-%s-%s.xml" % (pr, job_id, build))
                    merge_test_cases(build_test_results, merge_path, show_skipped=False)

def create_job_results_matrix_custom_acs(job):
    source_path = os.path.join(config['outputFolder'],"custom_acs", job["jobName"], "test_raw_results")
    reports = [report for report in os.listdir(source_path) if report.endswith("xml")]
    reports_paths = [os.path.join(source_path, report) for report in reports]
    matrix_output_dir = os.path.join(
        config['outputFolder'], 'custom_acs', job["jobName"], 'test_matrix'
    )
    matrix_output_name = JOB_TEST_MATRIX_NAME % {"job_name": job["jobName"]}
    create_matrix(reports_paths, os.path.join(matrix_output_dir, matrix_output_name))


def process_custom():
    # acs engine jobs don't have the folder struct like presubmits
    for job in config["jobs"]["custom_acs"]:
        copy_job_summaries_custom_acs(job)
        copy_job_test_results_custom_acs(job)
        create_job_summary_matrix_custom_acs(job)
        create_job_results_matrix_custom_acs(job)

job_handler_map = {
    'periodic': process_periodics,
    'presubmit': process_presubmits,
    'postsubmit': process_postsubmits,
    'custom_acs': process_custom
}

def process_jobs():
    for job_type in JOB_TYPES:
        job_handler_map[job_type]()

def main():
    process_jobs()
    pl = create_landing_page(config["jobs"])
    write_with_ensure_path(pl, os.path.join(config["outputFolder"], LANDING_PAGE_NAME))


main()