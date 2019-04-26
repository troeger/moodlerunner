#!/usr/bin/env python3

from moodleteacher.connection import MoodleConnection
from moodleteacher.courses import MoodleCourse
from moodleteacher.validation import Job
from moodleteacher.files import MoodleFile
from moodleteacher.submissions import MoodleSubmission
from moodleteacher.assignments import MoodleAssignment

import logging
import os
import time
import sys

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# Enable library debug logging on screen
logging.getLogger('moodleteacher').addHandler(handler)
logger = logging.getLogger('moodlerunner')
logger.addHandler(handler)


def check_env_var(name, mandatory, default=None):
    if name not in os.environ:
        if mandatory:
            logger.error("Missing environment variable {0}.".format(name))
            exit(-1)
        else:
            return default
    else:
        return os.environ[name]


def test_mode(validator_fname, submission_fname):
    if "RUNNER_PDB" in os.environ:
        import pdb
        pdb.set_trace()
    conn = MoodleConnection(is_fake=True)
    course = MoodleCourse(conn=conn, course_id=1)
    assignment = MoodleAssignment(
        course=course, assignment_id=1, allows_feedback_comment=True)
    submission = MoodleSubmission.from_local_file(
        assignment=assignment, fpath=submission_fname)
    validator = MoodleFile.from_local_file(validator_fname)
    job = Job(submission, validator, preamble="Local test result: ")
    job.start(log_level=logging.DEBUG)


if __name__ == '__main__':
    # Check for local testing mode, needs no configuration
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        logger.info("Running in local test mode ...")
        if len(sys.argv) != 4:
            print("Usage: docker run --mount type=bind,src=$(PWD),dst=/hostdir troeger/moodlerunner:0.1.19 test <validator file> <submission file>")
            exit(-1)
        test_mode('/hostdir/' + sys.argv[2], '/hostdir/' + sys.argv[3])
        exit(0)

    url = check_env_var('RUNNER_URL', mandatory=True)
    key = check_env_var('RUNNER_KEY', mandatory=True)
    course_id = check_env_var('RUNNER_COURSE_ID', mandatory=True)
    course_id = int(course_id)
    folder_id = check_env_var('RUNNER_FOLDER_ID', mandatory=True)
    folder_id = int(folder_id)
    preamble = check_env_var('RUNNER_PREAMBLE', mandatory=False, default="")
    log_level = check_env_var('RUNNER_LOG_LEVEL', mandatory=False)
    if log_level:
        log_level = logging.getLevelName(log_level)
    else:
        log_level = logging.DEBUG
    logger.setLevel(log_level)

    # choices: ['submission', 'assignment', 'cycleseconds_XXX']
    mode = check_env_var('RUNNER_MODE', mandatory=False,
                         default='cycleseconds_30')

    logger.info("Connecting to Moodle at {0} ...".format(url))
    conn = MoodleConnection(moodle_host=url,
                            token=key, interactive=False)

    while(True):
        # Get assignments for this course from Moodle server
        course = MoodleCourse.from_course_id(conn, course_id)
        assignments = course.assignments()
        logger.info("Course {0} with {1} assignments".format(
            course, len(assignments)))

        # Get folder with validation scripts from Moodle server
        for folder in course.get_folders():
            if folder.id_ == folder_id:
                validators_folder = folder
                logger.info("Folder with validators: {0}".format(
                    validators_folder))

        # Scan validator files in folder, determine according assignment and check if it has submissions
        for validator in validators_folder.files:
            validator_assignment_name = os.path.splitext(validator.name)[0]
            logger.debug("Searching for assignment with name '{0}'".format(
                validator_assignment_name))
            for assignment in assignments:
                if assignment.name.strip().lower() == validator_assignment_name.strip().lower():
                    submissions = assignment.submissions()
                    logger.info("Assignment {0} with {1} submissions has validators.".format(
                        assignment, len(submissions)))
                    for submission in submissions:
                        tech_header = "<hr/><small>Validation {0}: ".format(validator.time_modified)
                        for f in submission.files:
                            tech_header += "{0} ({1}) ".format(f.name, f.time_modified)
                        tech_header += "</small><hr/>"
                        # Check if submission was already validated, based on tech header
                        current_feedback = submission.load_feedback()
                        if current_feedback and tech_header in current_feedback:
                            logger.info("Submission {0} was already validated. Skipping it.".format(
                                submission.id_))
                        else:
                            logger.info(
                                "Submission to be validated: {0}".format(submission))
                            try:
                                job = Job(submission, validator, preamble=tech_header + preamble)
                                # Note: Log level for moodleteacher library is set to the same value as here
                                job.start(log_level=log_level)
                            except Exception as e:
                                logger.error("Validation crashed:")
                                logger.exception(e)
                            if mode == 'submission':
                                exit(0)
                else:
                    logger.debug("Ignoring assignment '{0}', does not match validator name.".format(
                        assignment.name))
                if mode == 'assignment':
                    exit(0)
        if mode.startswith('cycleseconds_'):
            timeout = int(mode.split('_')[1])
            logger.debug("Sleeping for {0} seconds ...".format(timeout))
            time.sleep(timeout)
        else:
            exit(0)
