#!/usr/bin/env python3

from moodleteacher.connection import MoodleConnection
from moodleteacher.courses import MoodleCourse
from moodleteacher.validation import Job
import logging
import os
import time
import sys

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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


if __name__ == '__main__':
    url = check_env_var('RUNNER_URL', mandatory=True)
    key = check_env_var('RUNNER_KEY', mandatory=True)
    course_id = check_env_var('RUNNER_COURSE_ID', mandatory=True)
    course_id = int(course_id)
    folder_id = check_env_var('RUNNER_FOLDER_ID', mandatory=True)
    folder_id = int(folder_id)
    preamble = check_env_var('RUNNER_PREAMBLE', mandatory=True)
    log_level = check_env_var('RUNNER_LOG_LEVEL', mandatory=False)
    if log_level:
        log_level = logging.getLevelName(log_level)
    else:
        log_level = logging.DEBUG
    logger.setLevel(log_level)

    # choices: ['submission', 'assignment', 'cycleseconds_XXX']
    mode = check_env_var('RUNNER_MODE', mandatory=False, default='cycleseconds_30')

    logger.info("Connecting to Moodle at {0} ...".format(url))
    conn = MoodleConnection(moodle_host=url,
                            token=key, interactive=False)

    while(True):
        # Get assignments for this course from Moodle server
        course = MoodleCourse.from_course_id(conn, course_id)
        assignments = course.assignments()
        logger.info("Course {0} with {1} assignments".format(course, len(assignments)))

        # Get folder with validation scripts from Moodle server
        for folder in course.get_folders():
            if folder.id_ == folder_id:
                validators_folder = folder
                logger.info("Folder with validators: {0}".format(validators_folder))

        # Scan validator files in folder, determine according assignment and check if it has submissions
        for validator in validators_folder.files:
            validator_assignment_name = validator.name.split('.')[0]
            for assignment in assignments:
                if assignment.name.strip().lower() == validator_assignment_name.strip().lower():
                    submissions = assignment.submissions()
                    logger.info("Assignment {0} with {1} submissions has validators.".format(assignment, len(submissions)))
                    for submission in submissions:
                        # Check if submission was already validated, based on preamble
                        current_feedback = submission.load_feedback()
                        if current_feedback.startswith(preamble):
                            logger.info("Submission {0} was already validated, found preamble. Skipping it.".format(submission.id_))
                        else:
                            logger.info("Submission to be validated: {0}".format(submission))
                            job = Job(submission, validator, preamble=preamble)
                            # Note: Log level for moodleteacher library is set to the same value as here
                            job.start(log_level=log_level)
                            if mode == 'submission':
                                exit(0)
                if mode == 'assignment':
                    exit(0)
        if mode.startswith('cycleseconds_'):
            timeout = int(mode.split('_')[1])
            logger.debug("Sleeping for {0} seconds ...".format(timeout))
            time.sleep(timeout)
        else:
            exit(0)
