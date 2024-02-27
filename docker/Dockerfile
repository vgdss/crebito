# Build the app image
FROM python:3.12.1

# Define the home directory in an environment variable
ENV APP_HOME=/home/app/api

# Create app user with a home directory /home/app in one command
# Prepare the application directory and install dependencies in one layer
# Change ownership of the home directory to the app user in one layer
RUN groupadd app && useradd -g app app && \
    mkdir -p $APP_HOME && \
    chown -R app:app /home/app

# Set the working directory
WORKDIR $APP_HOME

# Copy the application files to the container
COPY . $APP_HOME

# Upgrade pip and install both development and app dependencies in one step
RUN pip install --upgrade pip && \
    pip install -e .

# Switch to the app user
USER app

ENTRYPOINT ["sh", "-c", "uvicorn crebito.app:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}"]