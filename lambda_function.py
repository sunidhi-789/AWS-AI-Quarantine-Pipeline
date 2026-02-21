import boto3
import os

sns = boto3.client('sns')
s3_client = boto3.client('s3') # NEW: Needed to move files

def lambda_handler(event, context):
    # 1. Get the file info
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # 2. Call the AI - MODERATION
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_moderation_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': key}},
        MinConfidence=60
    )

    # 3. Format the labels
    labels = [label['Name'] for label in response['ModerationLabels']]

    # If unsafe content is found, we move it to another bucket
    if labels:
        quarantine_bucket = "my-smart-media-bucket"
        s3_client.copy_object(
            Bucket=quarantine_bucket,
            Key=key,
            CopySource={'Bucket': bucket, 'Key': key}
        )
        
        # Delete original file from public bucket
        s3_client.delete_object(Bucket=bucket, Key=key)

        message = f"SECURITY ALERT: Unsafe content {key} MOVED TO QUARANTINE. Labels: {labels}"
        subject = 'ACTION REQUIRED: Content Blocked'
    else:
        message = f"Smart Media Pipeline processed {key}. Image is safe."
        subject = 'Image Processing Complete'

    # 5. Save to Database (DynamoDB)
    db = boto3.resource('dynamodb', region_name='us-east-1')
    table = db.Table('ImageMetadata')
    table.put_item(Item = {'ImageID': key, 'Tags': labels, 'Status': 'Quarantined' if labels else 'Safe'})

    # 6. THE EMAIL
    sns.publish(
        TopicArn='arn:aws:sns:us-east-1:322113025946:ImageAlerts',
        Message=message,
        Subject=subject
    )

    return {"status": "success"}
