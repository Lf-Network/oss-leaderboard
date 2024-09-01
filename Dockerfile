FROM python:3.8-slim AS main

# Create a non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup -G appgroup -m appuser

# Set the working directory
WORKDIR /app

# Copy files
COPY . .

# Set ownership to the new user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Install Python requirements
# Install Python requirements
RUN pip3 install --user --upgrade pip && \
    pip3 install --user -r requirements.txt && \
    pip3 install --user -r requirements-dev.txt

# Run the main application
CMD ["python", "main.py"]
