# moodlerunner

This project provides a Docker image for automated validation of student submissions in Moodle.
It relies on the [moodleteacher](https://github.com/troeger/moodleteacher) project.

## Quickstart

### Step 1: Prepare Moodle resources

- Create a Moodle course.
- Create a folder hidden from students inside that course to store validator scripts.
- Create an assignment to be validated. Got to the setting *Feedback Types* and activate *Feedback comments* for the assignment.

### Step 2: Collect basic information

MoodleRunner needs some information for validating submissions in your Moodle course:

- RUNNER_URL: The URL of your Moodle installation, e.g. `https://moodle.example.edu`.
- RUNNER_KEY: A security token for accessing the Moodle API. Click on your picture in the right upper corner of the Moodle page, then go to *Preferences* -> *Security keys* and use the key for the *Moodle mobile web service*.
- RUNNER_COURSE_ID: The ID of the Moodle course you created in Step 1. You can find it in the URL of your course home page in Moodle, e.g. `123` when the URL is `https://moodle.example.edu/course/view.php?id=123`
- RUNNER_FOLDER_ID: The ID of the hidden folder you created in Step 1. In the browser, click on the folder and take the ID from the URL, e.g. `432312` when the URL is `https://moodle.example.edu/mod/folder/view.php?id=432312`

### Step 3: Upload validators

MoodleRunner executes validator scripts and reports the result automatically to the student. Examples for validator scripts can be found [online](https://github.com/troeger/moodlerunner/tree/master/examples/).

All validator scripts must be stored in the hidden folder you created in Step 1. The filename must match to the title of the assignment to be validated, e.g. if the assignment is named "Hello World in C", then your validator must be named "Hello World in C.py".

### Step 3: Run docker container

MoodleRunner comes as ready-to-use Docker container. The settings from Step 2 must be provided as environment variables:

```
docker run -e RUNNER_URL -e RUNNER_KEY -e RUNNER_COURSE_ID -e RUNNER_FOLDER_ID troeger/moodlerunner:0.1.11
```

## Mode of operation

You can use the environment variable RUNNER_MODE to define a mode of operation:

- 'submission': Validate one submission and then exit.
- 'assignment': Validate one assignment and then exit.
- 'cycleseconds_XXX': Validate everything that was not validated before, sleep for XXX seconds, then repeat.

The default mode is 'cycleseconds_30'.

## Local testing

You can run the image locally and without any Moodle interaction, which is useful during the development of validators.

Lets assume that the validator script to be tested lives in *./helloworld_java/validator.py*, while the example solution lives in *./helloworld_java/working/HelloWorld.java*: 

```
docker run --mount type=bind,src=$(PWD),dst=/hostdir troeger/moodlerunner:0.1.11 test helloworld_java/validator.py helloworld_java/working/HelloWorld.java
```

## Log level

The log level can be changed with the environment variable RUNNER_LOG_LEVEL. Possible values are CRITICAL, ERROR, WARNING, INFO, and DEBUG. The default (for the moment) is DEBUG. 	

