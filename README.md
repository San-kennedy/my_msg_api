# Message API
Rest api that allows users to post/view/delete message using mongo as backend DB

## Implementation Architecture

 - The API is implemented using falconAPI framework for Python. 
 - The API is served using Gunicorn WSGI server.
 - API code and it's runtime dependencies are packaged as a docker image (refer Dockerfile for details).
 - MongoDB was choose to persist messages posted to the app.
 - Docker compose allows us to orchestrate/interact with the deployment of app and DB as single entity (refer docker-compose.yml within Terraform directory for details).
 - Terraform is used to provision a VM on AWS to host the application.
