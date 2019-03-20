# moodlerunner

This project provides a Docker image for automated validation of student submissions in Moodle.
It relies on the [moodleteacher](https://github.com/troeger/moodleteacher) project.

## Quickstart

### Step 1: Collecting basic information

MoodleRunner needs some information for validating submissions in your Moodle course:

- RUNNER_URL: The URL of your Moodle installation, e.g. `https://moodle.example.edu`.
- RUNNER_KEY: A security token for accessing the Moodle API. Click on your picture in the right upper corner of the Moodle page, then go to *Preferences* -> *Security keys* and use the key for the *Moodle mobile web service*.
- RUNNER_COURSE_ID: The ID of the Moodle course. You can find it in the URL of your course home page in Moodle, e.g. `123`when the URL is `https://moodle.example.edu/course/view.php?id=123`
- RUNNER_FOLDER_ID: The ID of a hidden folder in the Moodle course. After creating it, click on the folder and take the ID from the URL, e.g. `432312` when the URL is `https://moodle.example.edu/mod/folder/view.php?id=432312`
- RUNNER_PREAMBLE: A text that is put as preamble in each student feedback. MoodleRunner uses that text to figure out if a submission was already validated.

### Step 2: Upload validators

MoodleRunner executes validator scripts and reports the result automatically to the student. Examples for validator scripts can be found [online](https://github.com/troeger/moodlerunner/tree/master/examples/).

All validator scripts must be stored in the hidden folder you created in Step 1. The filename must match to the title of the assignment to be validated, e.g. if the assignment is named "Hello World in C", then your validator must be named "Hello World in C.py".

### Step 3: Run docker container

MoodleRunner comes as ready-to-use Docker container. The settings from Step 1 must be provided as environment variables:

```
docker run -e RUNNER_URL -e RUNNER_KEY -e RUNNER_COURSE_ID -e RUNNER_FOLDER_ID -e RUNNER_PREAMBLE troeger/moodlerunner:0.1.3
```

## Mode of operation

You can use the environment variable RUNNER_MODE to define a mode of operation:

- 'submission': Validate one submission and then exit.
- 'assignment': Validate one assignment and then exit.
- 'cycleseconds_XXX': Validate everything that was not validated before, sleep for XXX seconds, then repeat.

The default mode is 'cycleseconds_30'.

## Log level

The log level can be changed with the environment variable RUNNER_LOG_LEVEL. Possible values are CRITICAL, ERROR, WARNING, INFO, and DEBUG. The default (for the moment) is DEBUG. 	

