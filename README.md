# Flaskr-API
**Name**: Jalen Jackson \
**Project 6**: Caching

## Description
This project expands on Project 2, adding HTTP and object caching to reduce the load on the database caused by retrieving timelines. \
To show the caching, running the timelines microservices is mandatory. Other microservices, like users, are optional.

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

### Direct Messages Service
```python
dm.py
```
![](https://thumbs.gfycat.com/BelatedWelltodoAustralianfurseal-size_restricted.gif)

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
* DynamoDB
* Amazon Web Services
### Libraries
* Pip
  * Flask
  * Flask API
  * Werkzeug
  * PugSQL
  * Boto3

## Installation
1. Initialize database (Adds tables then fills them with test users following each other)
```bash
$ FLASK_APP=users flask init
```

2. Initialize messages NOSQL table (If Messages table has been deleted)
```bash
$ FLASK_APP=dm flask init
```

3. (Optional) Adds tweets to each default user's timeline
```bash
$ FLASK_APP=timelines flask init
```

## Running All Services Using Foreman
```bash
$ foreman start
```
### Opening Up Microservice
Microservice | Link to Open It
------------ | ---------------
Users | http://127.0.0.1:5000/
Timelines | http://127.0.0.1:5001/
DMs | http://127.0.0.1:8000/

## Running Only Users Microservice
```bash
$ FLASK_APP=users flask run
```
## Running Only Timelines Microservice
```bash
$ FLASK_APP=timelines flask run
```
## Running Only Direct Messages Microservice
```bash
$ FLASK_APP=dm flask run --port 8000
```
