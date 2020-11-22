#Name: Jalen Jackson
#Email: jaydiddy72@csu.fullerton.edu
#Project 5: NoSQL

from flask import jsonify, request
from flask_api import FlaskAPI, status, exceptions

from users import user

from uuid import uuid1
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key, Attr

# Create the app and the Direct Messages table
app = FlaskAPI(__name__)

# Get the service resource
dynamodb = boto3.resource('dynamodb')

# Create the DyanmoDB table for Direct Messages
@app.cli.command("init")
def init_dms():

    table = dynamodb.create_table(
        TableName='Messages',
        KeySchema=[
            {
                'AttributeName': 'from',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'to',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'from',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'to',
                'AttributeType': 'S'
            }

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    table.meta.client.get_waiter('table_exists').wait(TableName='Messages')

    return table

# Sends a direct message to a user
def send_direct_message(to_username, from_username, message):
    if message is None:
        raise exceptions.NotFound()

    user(to_username)
    user(from_username)

    table = dynamodb.Table('Messages')
    table.put_item(
        Item={
            'from': from_username,
            'to': to_username,
            'timestamp': datetime.now().ctime(),
            'message': message,
            'replies': []
        }
    )

# Replies to a direct message. Reply is added to direct message's replies list
def reply_to_direct_message(to_username, from_username, reply):
    if reply is None:
        raise exceptions.NotFound()

    table = dynamodb.Table('Messages')
    table.update_item(
        Key={
            'from': from_username,
            'to': to_username
        },
        UpdateExpression="set replies = list_append(replies, :reply)",
        ExpressionAttributeValues={
            ":reply": [reply]
        },
        ReturnValues="ALL_NEW"
    )

# Lists all direct messages in the Messages table. Table updates after POST
@app.route("/", methods=['GET', 'POST'])
def show_direct_messages():
    if request.method == 'POST':
        send_direct_message(request.data['to'], request.data['from'], request.data['message'])
    
    table = dynamodb.Table('Messages')
    response = table.scan()
    return response['Items']

# Lists DM's to & from a user
@app.route("/<string:username>", methods=['GET'])
def list_direct_messages_for(username):
    table = dynamodb.Table('Messages')
    response = table.scan(
        FilterExpression=Key('from').eq(username) | Attr('to').eq(username)
    )
    return response['Items']

# Lists the replies to a DM
@app.route("/<string:from_username>/<string:to_username>", methods=['GET', 'POST'])
def list_replies(to_username, from_username):
    if request.method == 'POST':
        reply_to_direct_message(to_username, from_username, request.data['reply'])
    
    table = dynamodb.Table('Messages')
    response = table.get_item(Key={'from': from_username, 'to': to_username})
    return response['Item']['replies']
