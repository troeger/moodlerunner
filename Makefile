VERSION = 0.1.24

.PHONY: build check-venv

build:
	docker build -t troeger/moodlerunner:$(VERSION) .

run:
	docker run -e RUNNER_URL -e RUNNER_KEY -e RUNNER_COURSE_ID -e RUNNER_FOLDER_ID -e RUNNER_PREAMBLE troeger/moodlerunner:$(VERSION)

# Prepare VirtualEnv by installing project dependencies
venv/bin/activate: requirements.txt
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt
	touch venv/bin/activate

# Shortcut for preparation of VirtualEnv
venv: venv/bin/activate

check-venv:
ifndef VIRTUAL_ENV
	$(error Please create a VirtualEnv with 'make venv' and activate it)
endif

bumpversion:
	bumpversion --verbose patch

push: build
	docker login --username=troeger
	docker push troeger/moodlerunner:$(VERSION)
