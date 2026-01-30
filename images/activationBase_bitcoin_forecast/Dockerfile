FROM busybox:latest

# Create necessary directory
RUN mkdir -p /tmp/activationBase

# Copy activation data
COPY images/activationBase_bitcoin_forecast/activation_data.csv /tmp/activationBase/

# Copy README 
COPY images/activationBase_bitcoin_forecast/README.md /tmp/activationBase/

# Keep the container shell available
CMD ["sh"]