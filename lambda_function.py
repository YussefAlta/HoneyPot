import json
import process_logs

def lambda_handler(event, context):
    """AWS Lambda entry point to generate and upload heatmap"""
    logs = process_logs.get_attack_logs()
    if not logs:
        return {"message": "No attack logs found"}

    image_buffer = process_logs.generate_heatmap(logs)
    s3_url = process_logs.upload_to_s3(image_buffer)

    return {
        "statusCode": 200,
        "message": "Heatmap updated successfully",
        "heatmap_url": s3_url
    }
