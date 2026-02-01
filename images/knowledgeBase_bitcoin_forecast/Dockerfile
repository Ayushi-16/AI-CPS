# syntax=docker/dockerfile:1
FROM busybox:latest

RUN mkdir -p /knowledgeBase/

COPY currentSolution.keras /knowledgeBase/
COPY README.md /knowledgeBase/

CMD ["sh", "-c", "rm -rf /tmp/knowledgeBase/ && mkdir -p /tmp/knowledgeBase/ && cp -r /knowledgeBase/. /tmp/knowledgeBase/"]