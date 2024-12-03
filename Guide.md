# Step-by-Step Guide to Building Blog/Book Audio Converter using AWS Polly

## Project Description:
The **Blog/Book Narrator** project leverages AWS services to convert text files (such as blog posts, articles, newsletters, or book excerpts) into speech. This is particularly useful for creating audio versions of written content, making it accessible to a wider audience, including those who prefer listening over reading.

### Use Cases:
1. **Content Accessibility**: Provides audio versions of written content for visually impaired users.
2. **Learning**: Enables users to listen to educational materials, enhancing learning experiences.
3. **Content Distribution**: Offers an additional medium for content consumption, increasing engagement.
4. **Convenience**: Allows users to listen to articles or books while multitasking, such as during commutes or workouts.

---

## Project Architecture:
![Image](![image](https://github.com/user-attachments/assets/8cb445cc-6be0-4ce0-9784-b7eed060d836)


---

## Steps to Build the Project:

### **Step 1: Set Up an AWS Account**
- Sign in or create a new AWS account to get started.

---

### **Step 2: Create Two S3 Buckets**
- **Source S3 Bucket Name**: `amc-polly-source-bucket`
- **Destination S3 Bucket Name**: `amc-polly-destination-bucket`

---

### **Step 3: Create an IAM Policy**
- **IAM Policy Name**: `amc-polly-lambda-policy`
- **Policy Definition**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
      {
          "Effect": "Allow",
          "Action": [
              "s3:GetObject",
              "s3:PutObject"
          ],
          "Resource": [
              "arn:aws:s3:::amc-polly-source-bucket/*",
              "arn:aws:s3:::amc-polly-destination-bucket/*"
          ]
      },
      {
          "Effect": "Allow",
          "Action": [
              "polly:SynthesizeSpeech"
          ],
          "Resource": "*"
      }
  ]
}
```
### Step 4: Create an IAM Role
- **IAM Role Name**: `amc-polly-lambda-role`
- **Attach the following policies**:
  - `amc-polly-lambda-policy` (created in Step 3)
  - `AWSLambdaBasicExecutionRole` (built-in policy for Lambda)

---

### Step 5: Create and Configure the Lambda Function
- **Lambda Function Name**: `TextToSpeechFunction`
- **Configuration**:
  1. Set the runtime to **Python 3.8**.
  2. Assign the execution role created in Step 4.
  3. Add the following **Environment Variables**:
     - `SOURCE_BUCKET`: Name of your source S3 bucket.
     - `DESTINATION_BUCKET`: Name of your destination S3 bucket.

---

### Step 6: Configure S3 Event Notification
1. Set up an event notification in the source S3 bucket:
   - Trigger the Lambda function on new object creation events.
   - Filter events for files with the `.txt` suffix.

---

### Step 7: Write Lambda Function Code
Implement the Lambda function to:
1. Retrieve text files from the source S3 bucket.
2. Use AWS Polly to convert the text to speech.
3. Save the audio file to the destination S3 bucket.

---

### Step 8: Test the System
1. Upload a `.txt` file to the source S3 bucket.
2. Verify that the Lambda function is triggered.
3. Check the destination S3 bucket for the generated audio file.
