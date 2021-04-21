import json
import logging
import os
import random

import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

SNSTOPIC_ARN = os.getenv("SNSTOPIC_ARN")
WORKERQUEUE_URL = os.getenv("WORKERQUEUE_URL")
WORKERDLQ_URL = os.getenv("WORKERDLQ_URL")
SQS = boto3.client("sqs")
SNS = boto3.client("sns")


def producer(event, context):
    logger.info("SNSTOPIC_ARN-------------" + SNSTOPIC_ARN)
    logger.info("ProducerSQS_URL-------------" + WORKERQUEUE_URL)
    logger.info(f'ProducerEvent----------: {event}')
    status_code = 200
    if 'body' not in event:
        event["body"] = ''
    try:
        # Publish to topic
        ack_record = SNS.publish(
            TopicArn=SNSTOPIC_ARN,
            Message=event["body"],
            Subject="subject used in emails only",
            MessageAttributes={
                "event_type": {
                    "DataType": "String",
                    "StringValue": random.choice(
                        [
                            "ORDER_CANCELLED",
                            "SHIPMENT_CANCELLED",
                            "SHIPMENT_SHIPPED",
                            "PRODUCTION_STATUS_CHANGED",
                            "ORDER_CREATED",
                        ]
                    ),
                }
            },
        )
    except Exception as e:
        logger.exception("Sending message to SNS TOPIC failed!")
        message = str(e)
        status_code = 500

    return {"statusCode": status_code, "body": json.dumps({"Key": "Value"})}


def consumer(event, context):
    logger.info("SQS_URL-----------------------" + WORKERQUEUE_URL)
    logger.info("DLQ_URL------------------------" + WORKERDLQ_URL)
    logger.info(f"consumerEvent-------------------:{event}")
    logger.info("consumer\n\n\n\n\n\n\n\n")
    logger.info(event)

    raise Exception("Raising Exception, simply to fail&push msg/event to DLQ")


def slackit(event, context):
    import requests
    from requests.structures import CaseInsensitiveDict

    logger.info("SLACK IT------------------------------------")

    url = "https://hooks.slack.com/services/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"

    headers = CaseInsensitiveDict()
    headers["Content-type"] = "application/json"
    logger.info("slackit\n\n\n\n\n\n\n\n")
    logger.info(event)
    # data = '{"text":"Hello!"}'
    data = json.dumps({"text": event["Records"][0]["Sns"]["Message"]})

    resp = requests.post(url, headers=headers, data=data)

    print(resp.status_code)
    logger.info("ALRAM MSG SLACKED : " + str(resp.status_code))
