# Flaskr-API
**Name**: Jalen Jackson \
**Project 2**: Microblog-Microservices

## Description
In this project, two back-end microservices were built for a microblogging service similar to Twitter.

## Services
Your microservices should be written as two separate Flask applications connected to a single SQLite Version 3 database.

For more information on the REST API definitions for each microservice and the database.\
Go to [Rest API Definitions.pdf](https://github.com/JayDiddyThaGOAT/Flaskr-API/blob/master/REST%20API%20Definitions.pdf)

### Users Service
```python
users.py
```
![](https://thumbs.gfycat.com/MedicalQuestionableAmericanbadger-size_restricted.gif)

### Timelines Service
```python
timelines.py
```
![](https://thumbs.gfycat.com/AccurateScaredKinglet-size_restricted.gif)

### SQLite Version 3 Database
```sql
schema.sql
```

## Requirements
### Operating System
* Linux (Ubuntu 20.04 Used for Development)
### Tools
* Python 3
* SQL
* Foreman
### Libraries
* Pip
  * Flask
  * Flask API
  * Werkzeug
  * PugSQL

## Installation
1. Activate the virtual environment if requirements are installed locally on your computer
```bash
$ .venv/bin/activate
```
2. Initialize database (Adds tables then fills them with test users following each other)
```bash
$ FLASK_APP=users flask init
```
3. (Optional) Adds tweets to each default user's timeline
```bash
$ FLASK_APP=timelines flask init
```

## Running Both Services Using Foreman
```bash
$ foreman start
```
### Opening Up Microservice
Microservice | Link to Open It
------------ | ---------------
Users | http://127.0.0.1:5000/
Timelines | http://127.0.0.1:5001/

## Running Only Users Microservice
```bash
$ FLASK_APP=users flask run
```
## Running Only Timelines Microservice
```bash
$ FLASK_APP=timelines flask run
```

