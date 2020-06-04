[![CircleCI](https://circleci.com/gh/circle-chat/cc-be/tree/master.svg?style=svg)](https://circleci.com/gh/circle-chat/cc-be/tree/master)

# The Circle BE  
---
## Description  

##### The live version of the full project is available at: https://circle-fe-jcg5wby7mq-uc.a.run.app/


## Back-end Code


---
## Local Setup 
- Clone this repo to your local machine with: ``
- cd into the directory
- Install Poetry (instructions available at https://python-poetry.org/docs/)
  - Alternatively use your favorite python package manager like pip (a requirements.txt file is included)
- Start a Python Virtual Environment with `poety shell`
- RUN `poetry install`
- Install MongoDB - Community 4.2 Edition (instructions available at https://docs.mongodb.com/manual/installation/)
- Make sure the Mongo service is running `brew services start mongodb-community@4.2`
- To start the server in development use `flask run`

---
## Interacting with the Server

The back-end server has two ways to interact with it.  First, through common API endpoints.

### Creating a Group

#### POST to '/groups'
The POST method to /groups should contain json information for the following:

 * Name - Title for the group. (*)
 * Description - A short discription for the group. (*)
 * Rules - A single string of rules for the group.
 
This is return the following JSON object if done correctly

![Screen Shot 2020-06-01 at 12 34 23 PM-1](https://user-images.githubusercontent.com/56602822/83800119-89650800-a66c-11ea-84f1-bbd539cf4fb7.png)


---
## Project Collaborators  
