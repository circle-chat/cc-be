[![CircleCI](https://circleci.com/gh/circle-chat/cc-be/tree/master.svg?style=svg)](https://circleci.com/gh/circle-chat/cc-be/tree/master)

# The Circle BE  
---
## Description  
The Circle is a lightweight online chat website that randomly matches two people from a closed group together to have a one-on-one chat.  These groups can exist for an organization, a collective shared interest, or just about anything else. Our vision is to strengthen communities by fostering relationships between members of a circle who wouldn't normally take the time to chat and connect with each other.

The Circle is committed to privacy.  Groups auto expire after a certain time frame and no private user information is ever stored.

##### The live version of the full project is available at: https://circle-fe-jcg5wby7mq-uc.a.run.app/


## Back-end Tech Stack

### Python / Flask
The decision to use the Flask framework for Python came from the challenge of learning new language in a set amount of time.  Flask and its many libraries are very well documented which allowed for rapid development on the backend.  Flask and Pytest also work seamlessly together which enable near 100% test coverage.

### Circle CI
Circle CI is a very user friendly Continuous Intergration platform that uses a simple config file and is able to connect with github to make sure each Pull Request is tested prior to merging with the Production Branch

### Docker
Docker made managing the different contributors local setups with the many versions of Python and its libraries painless.  It also enabled very quick intergrated of new features and bug fixes to the deployed production server.

### Google Cloud Platform / CloudRun
Google

<img width="668" alt="Screen Shot 2020-06-04 at 2 22 41 PM" src="https://user-images.githubusercontent.com/10391857/83806630-0d1ff400-a66f-11ea-82a7-9b012f421631.png">

---
## Local Setup 
- Clone this repo to your local machine with: `git@github.com:circle-chat/cc-be.git`
- CD into the directory
- Install Poetry (instructions available at https://python-poetry.org/docs/)
  - Alternatively use your favorite python package manager like pip (a requirements.txt file is included)
- Start a Python Virtual Environment with `poetry shell`
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
  
When a user joins a group they wait in a lobby for another client to connect to the same group.  This information is briefly stored in the database for use in matchmaking.  When there is another connection (or more then 2) the users are randomly assigned into chat rooms.  This is done through the server emitting a 'join_room' event.

<img width="830" alt="Screen Shot 2020-06-04 at 2 28 03 PM" src="https://user-images.githubusercontent.com/56602822/83801999-a6e7a100-a66f-11ea-926e-c9feb8e65cc7.png">

Users are randomly paired with others in the same group.  The last socket client a user matched with is stored so that they are matched with the same person twice in a row.

The emitted 'join_room' event has this following data:

  * room - This is the room they are connecting too.  (Stored in the client)
  * user - Their username
  * match - This data has two pieces.  The first is the second user's name and the second piece is that users socket id.
  

#### Message
The message event handles the sending of messages to the server and back out to the connected sockets in that room.  The payload that comes through only has one requirement but more key values can be send as needed by the client.

  * room - This is the room that the message is to be emitted to. (Recieved from above)
  
Any additional key value pairs are pass back to the two clients connected to that room.

#### Leave Room
When this event is triggered the connection is severed and the connection is removed from the database.

---
## Database Schema
The Database used for this application is MongoDB due its ease in fast and agile development when working with none relational data.

There are two collections in the Database: Groups and Connections

### Groups
![Screen Shot 2020-06-04 at 2 43 19 PM](https://user-images.githubusercontent.com/56602822/83803297-efa05980-a671-11ea-8ba8-5e273d677fa0.png)

Groups are set to expire automatically after three days.

### Connections
![Screen Shot 2020-06-04 at 2 43 35 PM](https://user-images.githubusercontent.com/56602822/83803363-06df4700-a672-11ea-95c5-c163fd47be7b.png)

Connections are deleted automatically when a client disconnections but a fail safe is also in place that they delete after a set period of time as well.

---
## Project Collaborators  
* David Atkins - https://github.com/d-atkins
* Jordan Williams - https://github.com/iEv0lv3
* Ryan Allen - https://github.com/rcallen89
* Kyle Barnett - https://github.com/KmBarnett
* Ezekiel Clark - https://github.com/Yetidancer
