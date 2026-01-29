#Base image
FROM busybox:latest

# Create path 
RUN mkdir -p /tmp/activationBase/

# Copy the activation data and readme
COPY activation_data.csv /tmp/activationBase/
COPY README.md /tmp/activationBase/

# Keep the container shell available
CMD ["sh"]