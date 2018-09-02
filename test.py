import os
from shutil import copy
import errno
from subprocess import call

periodic_jobs = []
results_dir = []

path = "./35.231.16.99/win-e2e-test/pr-logs"
dest = "./test-output"

SUMMARY_TEMPLATE = "%(job)s/%(build)s/artifacts/junit_runner.xml"
ARTIFACTS_DIR_TEMPLATE = "%(job)s/%(build)s/artifacts"

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def get_build_results(job, build):
    artifacts_path = ARTIFACTS_DIR_TEMPLATE % {"job": job , "build": build}
    results = []
    for result in os.listdir(os.path.join(path, artifacts_path)):
        if result.startswith("junit") and not result.endswith("runner.xml"):
            results.append(result)


for job in os.listdir(path):
    builds = []

    for build in os.listdir(os.path.join(path, job)):
        if not os.path.isdir(os.path.join(path, job, build)):
            continue
        build_summary = SUMMARY_TEMPLATE % {"job": job , "build": build}
        results = []
        try:
            results = get_build_results(job, build)
        except:
            pass
        builds.append(dict(
            summary=build_summary,
            results=results,
            name = build
        ))
    periodic_jobs.append(dict(
        job=job, builds=builds
    ))

def copy_periodic_job_summaries(job):
    dest_dir = os.path.join(dest, "%(job)s/summary" % {"job": job['job']})
    mkdir_p(dest_dir)
    for build in job['builds']:
        if build["summary"]:
            dest_path = os.path.join(dest_dir, "%s.xml" % build['name'])
            summary_path = (os.path.join(path, build['summary']))
            if os.path.exists(summary_path):
                copy(summary_path, dest_path)

# for job in jobs
copy_periodic_job_summaries(periodic_jobs[0])

COPIED_SUMARIES_PATH_TEMPLATE = os.path.join(dest, "%(job)s/summary")

paths = []
for file_name in os.listdir(os.path.join(dest, "pull-kubernetes-e2e-win-1-11-fast/summary/")):
    paths.append(os.path.join(dest, "pull-kubernetes-e2e-win-1-11-fast/summary",file_name))


call(["junit2html", "--report-matrix=./test-output/test-matrix.html"] + paths)