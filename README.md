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

#### GET to '/groups'  
The GET method to /groups will return all the current groups in the database in the above formating

---
The second way to interact with the server is through websocket events.

#### Join Group
The join group event handles opening a websocket from client to server as well as giving the client access to a specific group.  The event should emit a json payload with the following key values:

  * access_code - This is the access code for the group.  This is used almost as a password into the group.
  * name - The name the user has input.
  
When a user joins a group they wait in a lobby for another client to connect to the same group.  When there is another connection (or more then 2) the users are randomly assigned into chat rooms.  This is done through the server emitting a 'join_room' event.

<img width="830" alt="Screen Shot 2020-06-04 at 2 28 03 PM" src="https://user-images.githubusercontent.com/56602822/83801999-a6e7a100-a66f-11ea-926e-c9feb8e65cc7.png">


---
## Project Collaborators  
