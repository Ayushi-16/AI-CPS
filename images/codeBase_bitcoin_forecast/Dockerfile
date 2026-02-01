FROM busybox:latest

RUN mkdir -p /codeBaseSource/ /activationBaseSource/

COPY activation_data.csv /activationBaseSource/
COPY train_ann.py train_ols.py LinearRegDiagnostic.py README.md /codeBaseSource/

CMD ["sh", "-c", "rm -rf /tmp/activationBase/ /tmp/codeBase/ && \
    mkdir -p /tmp/activationBase/ /tmp/codeBase/ && \
    cp -r /activationBaseSource/. /tmp/activationBase/ && \
    cp -r /codeBaseSource/. /tmp/codeBase/"]