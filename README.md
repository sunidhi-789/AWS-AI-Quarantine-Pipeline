#  Smart AI-Driven Media Pipeline (Serverless Quarantine)

<div align="center">
  
  ![AWS - Rekognition](https://img.shields.io/badge/AWS-Rekognition-orange?style=for-the-badge&logo=amazon-aws)
  ![AWS - Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900?style=for-the-badge&logo=amazon-lambda&logoColor=white)
  ![Python - 3.12](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
  ![Status - Production Ready](https://img.shields.io/badge/Status-Complete-green?style=for-the-badge)

</div>

---

##  Project Overview
Manual content moderation is a significant bottleneck for modern web platforms. This project implements an **Automated Cyber-Defense System** that acts as a real-time "Digital Security Guard." Using AI-driven analysis, the pipeline identifies policy-violating images (e.g., violence, weapons) and executes an instant **Incident Response** by isolating the threat.

> **Key Impact:** Reduces the "Mean Time to React" (MTTR) to harmful content from minutes to milliseconds.

---

##  System Architecture
The solution is built on a **Cloud-Native, Serverless Architecture** to ensure zero server management and infinite scalability.



---

##  Technical Implementation

<details>
<summary><b>Phase 1: Event-Driven Logic & Sanitization</b></summary>

The process begins with an **S3 Event Notification**. When a file is uploaded, a JSON event triggers the Lambda function.
* **Problem:** Filenames with spaces or special characters often cause API errors.
* **Solution:** I implemented `urllib.parse.unquote_plus` to decode and sanitize filenames before processing.
</details>

<details>
<summary><b>Phase 2: AI-Powered Policy Enforcement</b></summary>

I utilized the `detect_moderation_labels` API from **Amazon Rekognition**. 
* **Logic:** The AI scans for 10+ categories of unsafe content.
* **Thresholds:** I set a confidence threshold (e.g., 90%) to minimize false positives while ensuring maximum security.
</details>

<details>
<summary><b>Phase 3: Automated Quarantine Workflow</b></summary>

This is the core "Incident Response" phase. If a violation is flagged:
1. **Copy:** The file is moved to a private `quarantine-bucket`.
2. **Purge:** The file is immediately deleted from the public `upload-bucket`.
3. **Log:** A forensic record is created in **DynamoDB**.
</details>

---

##  Testing & Results
I conducted a **Live Policy Violation Test** to verify the automation. The system was tested with both compliant and non-compliant data to ensure accuracy and prevent false positives.

| Scenario | Input Image | AI Label Detected | Confidence | System Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **Safety Violation** | `test_violence.jpg` | Physical Conflict | 98.4% | ✅ **Quarantined** |
| **Policy Compliance** | `landscape.jpg` | None | 0% | ✅ **Approved** |

### **Proof of Concept Screenshots**
*Direct evidence of the pipeline's execution:*

1. **The Detection:** AI identifying the violation.  
   ![Detection](screenshots/detection_log.png)
2. **The Isolation:** The file being moved to the Restricted Bucket.  
   ![Isolation](screenshots/quarantine_bucket.png)
3. **The Alert:** The real-time security notification.  
   ![Alert](screenshots/sns_email.png)

---



### Security & IAM (Least Privilege)
To protect the infrastructure, I wrote a scoped **IAM Policy**. This ensures the Lambda function cannot access any data outside of these specific project buckets.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:GetObject", "s3:DeleteObject", "s3:PutObject"],
            "Resource": [
                "arn:aws:s3:::your-upload-bucket/*",
                "arn:aws:s3:::your-quarantine-bucket/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": "rekognition:DetectModerationLabels",
            "Resource": "*"
        }
    ]
}


