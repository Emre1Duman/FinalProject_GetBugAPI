from flask import Flask, request
import boto3, json


app = Flask(__name__)
app.config["DEBUG"] = True

##AWS CREDENTIALS##
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''

##RETRIEVE SECRETS FROM SECRET MANAGER##
client = boto3.client('secretsmanager', region_name = 'us-east-1', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

##SQS SECRETS##
responseSQS = client.get_secret_value( 
    SecretId = 'SQS_QueueURL'
)
jsonSQS = json.loads(responseSQS['SecretString'])
Queue_url = jsonSQS['SQS_Queue']

##Queue Connections##
sqs = boto3.client('sqs', region_name='us-east-1', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
queue_url = Queue_url


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