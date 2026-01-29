#Base image
FROM busybox:latest

# Create path
RUN mkdir -p /tmp/knowledgeBase/

# Copy the model and readme
COPY currentSolution.keras /tmp/knowledgeBase/
COPY README.md /tmp/knowledgeBase/

# Keep the container shell available
CMD ["sh"]