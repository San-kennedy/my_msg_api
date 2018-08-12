# Message API
Rest api that allows users to post/view/delete message using mongo as backend DB

## Implementation Architecture

 - The API is implemented using falconAPI framework for Python. 
 - The API is served using Gunicorn WSGI server.
 - API code and it's runtime dependencies are packaged as a docker image (refer Dockerfile for details).
 - MongoDB was choose to persist messages, as it's document oriented approach lends itself seamlessly to REST API design.
 - Docker compose allows us to orchestrate/interact with the deployment of app and DB as single entity (refer docker-compose.yml within Terraform directory for details).
 - Terraform is used to provision a VM on AWS to host the application.

## Sequence diagram

![generic get](https://user-images.githubusercontent.com/13183605/43991247-47c62636-9d86-11e8-86e8-45e4a5c7f229.png)
![post message_s](https://user-images.githubusercontent.com/13183605/43991248-480c4abc-9d86-11e8-8cee-b184793a3a84.png)
![specfic get request](https://user-images.githubusercontent.com/13183605/43991246-47951c80-9d86-11e8-8ccc-e2d895828586.png)
![specfic delete request](https://user-images.githubusercontent.com/13183605/43991245-47633dbe-9d86-11e8-88b3-d2f24c770ccc.png)

## Build, delpoy and access

#### To just run the API code using WSGI servers:
- Make sure to change /msgapi/mongo_db_conf.py to reflect existing mongo details
- For windows: pip install waitress, followed by waitress-serve --port 8000 api:MSGAPI in cloned directory
- For linux/MacOS : pip install gunicorn, followed by gunicorn -b 0.0.0.0:8000 api:MSGAPI in cloned directory

#### To build and run app alone in a container

- Use dockefile to build docker image, make sure to change /msgapi/mongo_db_conf.py to reflect existing mongo details
- docker run -d -p 8000:8000 image name
- curl localhost:8000/messages to check

#### To run using docker compose

- Just run docker-compse -f Terraform/docker-compose.yml up -d
- curl localhost:8000/messages to check
- If it returns an empty array(as no messages have been inserted), app and DB have been setup successfully

#### For full blown deployment on AWS

- Update Terraform/terraform.tfvars with your AWS specific creds (Access tokens, Keys). 
- Just run terraform apply.
- Terraform outputs the public_dns name of the host, curl the hostname:8000/messages to check
- If it resturns an empty array, deployment is successful (as no messages have been inserted)

## RestAPI documentation

#### https://app.swaggerhub.com/apis/santosh_ken/Messaging/1.0.0#/

example array of messages for POST

[{
	"msg": "Eva Can I Stab Bats In A Cave"
}, {
	"msg": "malayalam",
	"Author": "test"
}, {
	"msg": "This is testing sentence"
}, {
	"msg": "A Man, A Plan, A Canal-Panama!"
}]
