# EventDrivenConsumer

A serverless event consumer that logs out events payload.

# Technical requirements

*	Should follow pattern of (see above diagram): Message Bus (SNS) -> Service Queue(SQS) -> Lambda *
*	Should filter for events from siteId: 1 and the following event types: ORDER_CREATED, PROOF_STATUS_CHANGED, PRODUCTION_STATUS_CHANGED *
*	Should implement DLQ *
*	Should set a Cloudwatch Alarm on DLQ with a threshold *
*	Should use Sentry to capture errors If DLQ Alarm is tripped then it should slack #serverles-npe (non-production-environment)*


# Get started with Serverless Framework 

Install the serverless CLI :
:: 
    $npm install -g serverless
Update with :
::
    $npm update -g serverless


# Configure serverless credentials

Need details of Provider, accesskey and secretkey
::
    $serverless config credentials --provider aws --key xxxxxxxxxxx --secret xxxxxxxxxxxxxxx --overwrite



#Create and deploy a serverless Service

Now that you’ve completed your setup, let’s create and deploy a serverless Service.

#Create a new Service from a Template

Use the Serverless Framework open-source CLI to create a new Service.

# Create a new Serverless service/project
::
    $ serverless

# Change into the newly created directory
::
    $ cd TestEDC

Define your design in your serverless.yml that will trigger aws cloudformation stack.

#Deploy the Service

Use this command to deploy your service for the first time and after you make changes to your Functions, Events or Resources in serverless.yml and want to deploy all changes within your Service at the same time.
::
    $ serverless deploy -v

#Test your Service

Replace the URL in the following curl command with your returned endpoint URL, which you can find in the sls deploy output, to hit your URL endpoint.
::
    $ curl -X POST https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/hello

#Invoke your Service's function

Invokes a Function and returns logs.
::
    $serverless invoke -f hello -l

#Fetch the Function Logs

Open up a separate tab in your console and stream all logs for a specific Function using this command.
::
    $serverless logs -f hello -t

#Monitor your Service

Use either of the two commands below to generate mock errors that you will then be able to visualize in the Serverless Framework Dashboard. If you use the curl command remember to replace the URL in the command with your returned endpoint URL, which you can find in your sls deploy output.

::
    $serverless invoke -f hello -d '{"body": "not a json string"}' # causes a JSON parsing error so error Insights will populate
    $ curl https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/hello --data-binary 'not a json string' # causes a JSON parsing error so error Insights will populate

#Cleanup

#Remove your Service

If at any point you no longer need your Service, you can run the following command to remove the Functions, Events and Resources that were created. This will delete the AWS resources you created and ensure that you don't incur any unexpected charges. It will also remove the Service from your Serverless Framework Dashboard.
::
    $serverless remove
