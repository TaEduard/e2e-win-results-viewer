from constants import *
import os

def add_job_name(job):
    job_res_path = job["jobResultsDir"]
    job_name = job['jobName']
    output = "<span style=' margin-left: 10px;' ><a href=%s>%s</a></span>" % (job_res_path, job_name)
    return output

def add_job_summary_matrix(job, job_type):
    job_summary_matrix_path = os.path.join(job_type, job["jobName"], "summary_matrix")
    job_summary_matrix_name = JOB_SUMMARY_MATRIX_NAME % {"job_name": job['jobName']}
    output = "<span style=' margin-left: 10px;'><a href=%s>SUMMARY</a></span>" % (os.path.join(job_summary_matrix_path, job_summary_matrix_name))
    return output

def add_job_test_matrix(job, job_type):
    job_summary_matrix_path = os.path.join(job_type, job["jobName"], "test_matrix")
    job_summary_matrix_name = JOB_TEST_MATRIX_NAME % {"job_name": job['jobName']}
    output = "<span style=' margin-left: 10px;'><a href=%s>TEST MATRIX</a></span>" % (os.path.join(job_summary_matrix_path, job_summary_matrix_name))
    return output


def add_custom_acs_job(job):
    output = "<li><ul>"
    job_test_results_path = os.path.join("custom_acs", job["jobName"], "test_matrix")
    for pr in os.listdir(os.path.join(results, job_test_results_path)):
        pr_matrix_path = os.path.join(job_test_results_path, pr , "%s-%s-test-matrix.html" % (job["jobName"], pr))

        if not os.path.isdir(os.path.join(results, job_test_results_path, pr)):
            continue
        output += "<li><span style=' margin-left: 10px;'><a href=%s>%s : TEST MATRIX</a></span>" % (pr_matrix_path, pr)
        output += "</li>"
    output += "</ul></li>"
    return output

def add_job(job, job_type):
    output = add_job_name(job)
    if job_type == "custom_acs":
        # jobs are per pr
        output += add_job_summary_matrix(job, job_type)
        output += add_job_test_matrix(job, job_type)
        output += add_custom_acs_job(job)
        return output
    output += add_job_test_matrix(job, job_type)
    output += add_job_summary_matrix(job, job_type)
    return output

def add_jobs(job_type, jobs):
    output = "<li>%s</li>" % job_type
    output += "<li><ul>"
    for job in jobs:
        output += "<li>%s</li>" % add_job(job, job_type)
    output += "</ul></li>"
    return output
        
def create_landing_page(jobs, results_folder):
    global results 
    results = results_folder
    output = "<html><body>Test reports<ul>"
    for job_type in jobs.keys():
        if len(jobs[job_type]) > 0:
            output += add_jobs(job_type, jobs[job_type])
    output += "</ul></body></html>"

    return output
