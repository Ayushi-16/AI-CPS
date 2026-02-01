FROM busybox:latest

RUN mkdir -p /learningBaseSource/train /learningBaseSource/validation

COPY train/training_data.csv /learningBaseSource/train/
COPY validation/test_data.csv /learningBaseSource/validation/
COPY README.md /learningBaseSource/

CMD ["sh", "-c", "rm -rf /tmp/learningBase/ && mkdir -p /tmp/learningBase/train /tmp/learningBase/validation && cp -r /learningBaseSource/. /tmp/learningBase/ && echo 'LearningBase files injected into volume'"]