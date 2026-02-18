# Smart AI-Media Pipeline 
### *Automated Serverless Image Processing with Amazon Rekognition*

<p align="center">
  <img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Serverless-FF9900?style=for-the-badge&logo=serverless&logoColor=white" />
  <img src="https://img.shields.io/badge/DynamoDB-4053D6?style=for-the-badge&logo=amazondynamodb&logoColor=white" />
</p>

---

##  Navigation
[ Overview](#overview) | [Architecture](#architecture) | [ Tech Stack](#tech-stack) | [ Implementation](#implementation) | [Results](#results) | [Security](#security)

---

<a name="overview"></a>
##  Project Overview
This 3rd-year vocational project demonstrates a **Cloud-Native Event-Driven Architecture**. By leveraging AWS Lambda and Rekognition, I've built a system that eliminates manual image tagging, reducing processing time to **<400ms** per file.
<a name="architecture"></a>
##  System Architecture
The pipeline is fully serverless, ensuring **High Availability** and **Auto-Scaling**.

<details>
<summary><b>View Architecture Flow Details (Click to Expand)</b></summary>

1. **Trigger:** `S3:PutObject` event notification.
2. **Compute:** `AWS Lambda` environment initialized.
3. **AI Layer:** `Amazon Rekognition` performs deep-learning feature extraction.
4. **Storage:** NoSQL metadata storage in `Amazon DynamoDB`.
5. **Messaging:** Asynchronous notification via `Amazon SNS`.

</details>
<a name="implementation"></a>
##  Implementation Highlights

###  The Brain (AWS Lambda)
The Python function is optimized for **Performance** and **Cold Starts**.

| Feature | Implementation | Benefit |
| :--- | :--- | :--- |
| **Parsing** | `urllib.parse.unquote_plus` | Handles spaces and special characters in filenames. |
| **AI Filter** | `MinConfidence: 80` | Filters out "noise" and low-accuracy AI guesses. |
| **Concurrency** | Serverless | Handles 1000+ uploads simultaneously. |
<a name="results"></a>
##  Testing Results
The pipeline was validated using a variety of test cases.

| Input Media | AI Analysis (Metadata) | Status |
| :--- | :---: | :---: |
| `street_view.jpg` | `["Car", "City", "Traffic"]` | ✅ Pass |
| `forest.png` | `["Trees", "Nature", "Green"]` | ✅ Pass |

> **Log Trace:** `[INFO] Image processed in 369.41 ms. Billed: 370 ms.`


