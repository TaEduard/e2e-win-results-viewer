# directory struct for results

# results_dir -- index.html ( landing page )
#             |_ periodics -- job1 ---- summary_raw_results
#             |            \_ job2   |- test_raw_results
#             |                      |- summary_matrix
#             |                      \_ test_matrix
#             \_ presubmit -- job1 

# every path is relative to output dir

LANDING_PAGE_NAME = "index.html"
LANDING_PAGE_PATH = "." 
PERIODIC_JOB_PATH_TEMPLATE = "periodics/%(job_name)s"
# where junit files are copied over and renamed 
JOB_SUMMARY_RAW_RESULTS_PATH = PERIODIC_JOB_PATH_TEMPLATE + "/summary_raw_res"
JOB_TEST_RAW_RESULTS_PATH = PERIODIC_JOB_PATH_TEMPLATE + "/test_raw_results"
JOB_SUMMARY_MATRIX_PATH = PERIODIC_JOB_PATH_TEMPLATE + "/summary_matrix"
JOB_SUMMARY_MATRIX_NAME = "%(job_name)s-summary-matrix.html" 
JOB_TEST_MATRIX_PATH = PERIODIC_JOB_PATH_TEMPLATE + "/test_matrix"
JOB_TEST_MATRIX_NAME = "%(job_name)s-test-matrix.html"

# all are relative to job output dir defined in config
JOB_BUILD_SUMMARY_SOURCE_PATH = "%(build)s/artifacts/junit_runner.xml"
JOB_BUILD_TEST_SOURCE_DIR = "%(build)s/artifacts"
JOB_BUILD_TEST_REGEX = "junit_([0-9]+)\.xml"

JOB_TYPES = ["presubmit", "periodic", "postsubmit", "custom_acs"]