# Daily Check-In App (Serverless)

A fully serverless daily check-in system built on AWS that sends scheduled emails, collects user input via a web form, and stores responses for tracking and analysis.

This project demonstrates end-to-end cloud architecture using Infrastructure as Code, event-driven workflows, and frontend/backend integration.

---

## Overview

The Daily Check-In App is designed to:

- Send a daily reminder email with a personalized form link
- Allow users to submit a structured check-in
- Store submissions in a database
- Prevent duplicate submissions
- Provide a clean, user-friendly experience

The system is fully serverless and runs at minimal cost.

---

## Architecture

This application is built using:

- **AWS Lambda** – backend logic and frontend hosting  
- **Lambda Function URLs** – API endpoints  
- **DynamoDB** – persistent storage  
- **EventBridge** – scheduled email triggers  
- **SES (Simple Email Service)** – email delivery  
- **Route 53** – DNS and domain management  
- **Terraform** – Infrastructure as Code  

---

## Features

- Daily scheduled email reminders  
- Serverless web form hosted via Lambda  
- Form submission API  
- DynamoDB data storage  
- Token-based submission validation  
- Duplicate submission prevention  
- Additional tracked fields:
  - Sleep hours  
  - Money spent  
- Improved UI/UX:
  - Emoji-based scoring
  - Sectioned layout
  - Guided prompts
  - Validation and confirmation feedback  

---

## Example Flow

1. EventBridge triggers a Lambda daily  
2. Lambda sends an email via SES  
3. Email contains a unique form link  
4. User fills out check-in form  
5. Submission is sent to Lambda API  
6. Data is validated and stored in DynamoDB  
7. Duplicate submissions are blocked  

---

## Cost

The application is extremely cost-efficient:

| Service | Monthly Cost |
|--------|------|
| Lambda | $0 (free tier) |
| DynamoDB | ~$0 |
| SES | $0 |
| EventBridge | $0 |
| Route 53 Hosted Zone | $0.50 |
| Domain | ~$1 |

**Total: ~ $1–2/month**

---

## Development Challenges & Lessons Learned

This project involved several real-world debugging and integration challenges.

### Terraform Issues
- Undeclared variables and unsupported arguments
- Mismatched module interfaces
- Missing required inputs

**Lesson:** Treat Terraform modules like APIs — explicitly define inputs/outputs.

---

### Lambda Configuration Issues
- Missing environment variables (`FORM_URL`, `SUBMIT_URL`, `TABLE_NAME`)
- Reserved variables like `AWS_REGION`
- Handler and packaging mismatches

**Lesson:** Always validate environment variables and ensure handler alignment.

---

### API & Function URL Issues
- Attempted to use Lambda ARN instead of Function URL
- Function URL not appearing due to misconfiguration

**Lesson:** ARN is not an endpoint — always use Function URLs for HTTP access.

---

### CORS Debugging
- Browser “failed to fetch” errors
- OPTIONS preflight behavior
- Duplicate CORS headers

**Root Cause:**
CORS headers were set in both:
- Lambda Function URL config
- Lambda response code

**Fix:**
Removed headers from code and let AWS manage CORS.

**Lesson:** Only one layer should control CORS.

---

### Frontend Issues
- JSON parsing errors (`Unexpected token 'I'`)
- Incorrect API endpoint usage
- Lack of validation and feedback

**Fixes:**
- Standardized JSON responses
- Added validation and confirmation UX
- Improved form usability

---

### DynamoDB Integration
- Incorrect resource references
- Missing table name in environment variables
- Uncertainty around data persistence

**Fixes:**
- Used module outputs (`module.dynamodb.table_name`)
- Verified data using AWS CLI

---

### Duplicate Submission Handling
Users could submit multiple entries per day.

**Fix:**
```python
ConditionExpression="attribute_not_exists(person_id) AND attribute_not_exists(submission_date)"
```
- Also added proper error handling to return a 409 Conflict.
- Lesson: Enforce data integrity at the database level.

## Key Takeaways

- Most issues were integration-related, not logic-related  
- Debugging required isolating frontend, backend, and infrastructure  
- Direct testing tools (`curl`, AWS CLI) were critical  
- Terraform requires strict consistency between modules  
- CORS is one of the most common pitfalls in serverless applications  
- DynamoDB is flexible but still requires proper key design for data integrity  
- Serverless architectures reduce cost but increase integration complexity  

---

## Future Improvements

- Token signing for security  
- User personalization (e.g., displaying user name in UI)  
- Analytics dashboard for tracking trends over time  
- Streak tracking to improve user engagement  
- Allow editing submissions instead of blocking duplicates  

---

## Final Thoughts

This project demonstrates a complete serverless application lifecycle, including:

- Infrastructure provisioning with Terraform  
- Backend API development using AWS Lambda  
- Frontend delivery through Lambda Function URLs  
- Event-driven scheduling with EventBridge  
- Data persistence using DynamoDB  
- Email delivery with SES  
- DNS management via Route 53  

In addition to building the system, significant effort was spent debugging real-world issues such as CORS conflicts, environment variable misconfigurations, module wiring errors, and frontend/backend integration challenges.

The project reflects practical cloud engineering experience and highlights the importance of structured debugging, proper infrastructure design, and user-focused improvements.

Overall, this application represents a production-style system built with minimal cost, strong scalability, and a focus on reliability and usability.