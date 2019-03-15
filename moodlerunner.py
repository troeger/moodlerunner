#!/usr/bin/env python3

from moodleteacher import MoodleConnection, MoodleAssignments, MoodleSubmissionFile
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def check_env_var(name, mandatory, default=None):
    if name not in os.environ:
        if mandatory:
            logger.error("Missing environment variable {0}.".format(name))
            exit(-1)
        else:
            return default
    else:
        return os.environ[name]


def handle_submission(sub):
    files = MoodleSubmissionFile.from_urls(conn, sub.files)
    logger.debug("Submission {0} has {1} files.".format(sub.id, len(files)))
    # TODO: Unpack submission in temp directory

    # TODO: Call validator function, provide MoodleSubmission object

    if finish == 'submission':
        exit(0)


if __name__ == '__main__':
    url = check_env_var('RUNNER_URL', mandatory=True)
    key = check_env_var('RUNNER_KEY', mandatory=True)
    # choices: ['submission', 'assignment', 'never']
    finish = check_env_var('RUNNER_FINISH', mandatory=False, default='never')

    logger.debug("Connecting to Moodle at {0} ...".format(url))
    conn = MoodleConnection(moodle_host=url,
                            token=key, interactive=False)

    assignments = MoodleAssignments(conn)

    for assignment in assignments:
        logger.debug("Checking assignment '{0}' ...".format(assignment.name))

        if not assignment.course.can_grade:
            logger.error("Assignment is not gradable.")
        else:
            logger.debug("Fetching validation script ...")
            # TODO: Use API to fetch validator file

            submissions = assignment.submissions()
            for sub in submissions:
                handle_submission(sub)

        if finish == 'assignment':
            exit(0)
