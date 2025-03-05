# 🔥 AWS Honeypot Cybersecurity Project

## **🚀 Overview**
This project is a **honeypot system deployed on AWS EC2** to detect and analyze **cyberattack attempts in real time**. It utilizes **Cowrie**, a medium-interaction SSH honeypot, to log attack attempts and stores the logs in **AWS DynamoDB and S3**. 
A visualization system generates **heatmaps of attack locations**, helping to identify global threat patterns.

---

## **🎯 Key Features**
✅ **Honeypot Detection**: Captures unauthorized SSH login attempts.  
✅ **AWS Integration**: Logs data in **DynamoDB** and stores files in **S3**.  
✅ **Automated Log Processing**: A **Lambda function** processes logs, extracts data, and generates attack reports.  
✅ **Heatmap Visualization**: Attack logs are visualized as a **heatmap**, updated automatically.  
✅ **Automated Deployment**: Lambda function updates dynamically from **GitHub** (without ZIP files).  

---

## **🛠️ Tech Stack**
- **Cloud Services**: AWS EC2, S3, DynamoDB, Lambda, EventOrganizer
- **Honeypot**: Cowrie (SSH-based honeypot)
- **Programming**: Python (Boto3, Matplotlib, Pandas, Requests)
- **Data Processing**: AWS Lambda, Cron Jobs
- **Visualization**: Matplotlib (Heatmaps)
- **Automation**: AWS CLI, GitHub Actions, AWS EventOrganizer

---

## **⚙️ System Architecture**
📌 **EC2 Instance**  
→ Runs Cowrie Honeypot to log attack attempts  
📌 **S3 Bucket**  
→ Stores log files for further analysis  
📌 **DynamoDB Table**  
→ Stores structured attack data (IP, timestamp, location, attack type)  
📌 **AWS Lambda**  
→ Processes logs and updates heatmap images
📌 **AWS Event Organizer** 
→ Triggers Lambda function to run every hour to update Heatmap
📌 **Heatmap Dashboard**  
→ Visualizes attack data  

---

