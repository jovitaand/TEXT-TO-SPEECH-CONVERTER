import boto3
import json
import os
import logging
import time

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def split_text(text, max_length=3000):
    """
    Splits the input text into smaller chunks for Polly.
    """
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def lambda_handler(event, context):
    # Initialize S3 and Polly clients
    s3 = boto3.client('s3')
    polly = boto3.client('polly')

    # Get the bucket names from environment variables
    source_bucket = os.environ['SOURCE_BUCKET']
    destination_bucket = os.environ['DESTINATION_BUCKET']

    # Get the object key from the event
    text_file_key = event['Records'][0]['s3']['object']['key']
    audio_key = text_file_key.replace('.txt', '.mp3')

    try:
        # Step 1: Retrieve text from the source S3 bucket
        start_time = time.time()
        logger.info(f"Retrieving text file from bucket: {source_bucket}, key: {text_file_key}")
        text_file = s3.get_object(Bucket=source_bucket, Key=text_file_key)
        text = text_file['Body'].read().decode('utf-8')
        logger.info(f"Retrieved text file. Time taken: {time.time() - start_time:.2f} seconds")

        # Step 2: Send text to Polly in chunks if necessary
        start_time = time.time()
        logger.info(f"Splitting text into chunks for Polly synthesis if necessary")
        chunks = split_text(text)
        temp_audio_path = '/tmp/audio.mp3'
        with open(temp_audio_path, 'wb') as output_file:
            for chunk in chunks:
                logger.info(f"Sending chunk to Polly for synthesis")
                response = polly.synthesize_speech(
                    Text=chunk,
                    OutputFormat='mp3',
                    VoiceId='Joanna'  # Choose the voice you prefer
                )
                if 'AudioStream' in response:
                    output_file.write(response['AudioStream'].read())
                else:
                    logger.error("No audio stream found in Polly response.")
                    raise RuntimeError("Polly synthesis failed to return audio stream.")
        logger.info(f"Polly synthesis completed. Time taken: {time.time() - start_time:.2f} seconds")

        # Step 3: Upload the audio file to the destination S3 bucket
        start_time = time.time()
        logger.info(f"Uploading audio file to bucket: {destination_bucket}, key: {audio_key}")
        s3.upload_file(temp_audio_path, destination_bucket, audio_key)
        logger.info(f"Audio file uploaded successfully. Time taken: {time.time() - start_time:.2f} seconds")

        # Step 4: Cleanup temporary file (optional)
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            logger.info(f"Temporary file deleted: {temp_audio_path}")

        logger.info(f"Text-to-Speech conversion completed successfully for file: {text_file_key}")

        return {
            'statusCode': 200,
            'body': json.dumps('Text-to-Speech conversion completed successfully!')
        }

    except Exception as e:
        logger.error(f"Error processing file {text_file_key} from bucket {source_bucket}: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('An error occurred during the Text-to-Speech conversion.')
        }
