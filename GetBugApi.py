from flask import Flask, request
import boto3, json, botocore, botocore.session
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig 

app = Flask(__name__)
app.config["DEBUG"] = True

##RETRIEVE SECRETS FROM SECRET MANAGER##
client = botocore.session.get_session().create_client('secretsmanager')
cache_config = SecretCacheConfig()
cache = SecretCache( config = cache_config, client = client)

##AWS SECRETS##
AWSKeySecret = cache.get_secret_string('AWS_Keys') #Retrieve AWS secret
jsonAWS = json.loads(AWSKeySecret) #jsonify secrets

AWS_ACCESS_KEY = jsonAWS['AWS_Access_Key']
AWS_SECRET_KEY = jsonAWS['AWS_Secret_Key']

##SQS SECRETS##
SQSSecret = cache.get_secret_string('SQS_QueueURL') 
jsonSQS = json.loads(SQSSecret)

SQS_Queue = jsonSQS['SQS_Queue']

##Queue Connections##
sqs = boto3.client('sqs', region_name='us-east-1', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
queue_url = SQS_Queue


@app.route('/submitBug', methods=['POST'])
def home():
    priority=request.args.get('priority') #Get bug via postman and send through sendtoqueue method
    name=request.args.get('name')
    return sendtoqueue(name, priority)

def sendtoqueue(nameForMessage, priorityForMessage): #Sends the message as attributes to an SQS Queue

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