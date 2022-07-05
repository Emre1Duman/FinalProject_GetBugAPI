from queue import PriorityQueue
from flask import Flask, request, jsonify
import boto3, json

app = Flask(__name__)
app.config["DEBUG"] = True

AWS_ACCESS_KEY=''
AWS_SECRET_KEY=''

sqs = boto3.client('sqs', region_name='us-east-1', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
queue_url = 'https://sqs.us-east-1.amazonaws.com/900076774107/PriorityBugQueue'


@app.route('/submitBug', methods=['POST'])
def home():
    priority=request.args.get('priority')
    name=request.args.get('name')
    return sendtoqueue(name, priority)

def sendtoqueue(nameForMessage, priorityForMessage):

    response = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=10,
            MessageAttributes={
                'name': {
                    'DataType': 'String',
                    'StringValue': nameForMessage
                },
                'priority': {
                    'DataType': 'String',
                    'StringValue': priorityForMessage
                }
            },
            MessageBody=(
                'New bugs found!'
            )
    )
    return("Stored in queue with message ID "+response['MessageId'])


  
if __name__ == '__main__': 
    app.run(host="0.0.0.0", port=5000, debug=True) 