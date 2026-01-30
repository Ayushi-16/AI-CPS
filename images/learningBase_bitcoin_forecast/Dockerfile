FROM busybox:latest

# Create necessary directories inside the container
RUN mkdir -p /tmp/learningBase/train
RUN mkdir -p /tmp/learningBase/validation

# Copy training and validation data
COPY images/learningBase_bitcoin_forecast/train/training_data.csv /tmp/learningBase/train/
COPY images/learningBase_bitcoin_forecast/validation/test_data.csv /tmp/learningBase/validation/

# Copy README
COPY README.md /tmp/learningBase/

# Keep the container shell available
CMD ["sh"]