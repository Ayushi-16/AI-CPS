FROM busybox:latest

# Create necessary directory
RUN mkdir -p /tmp/activationBase

# Copy activation data
COPY images/activationBase_bitcoin_forecast/tmp/activationBase/activation_data.csv /tmp/activationBase/

# Copy README 
COPY images/activationBase_bitcoin_forecast/tmp/activationBase/README.md /tmp/activationBase/