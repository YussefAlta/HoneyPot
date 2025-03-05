import boto3
import requests
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import io

# AWS Resources
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

# Configurations
DYNAMODB_TABLE = "CyberAttackLogs"
S3_BUCKET_NAME = "honeypot-logs-yussefaltaher"
HEATMAP_IMAGE_NAME = "cyber_attack_heatmap.png"
IP_API_URL = "http://ip-api.com/json/"

def get_attack_logs():
    """Fetch attack logs from DynamoDB"""
    table = dynamodb.Table(DYNAMODB_TABLE)
    response = table.scan()  # Scanning entire table (optimize with filters later)
    logs = response.get("Items", [])
    return logs

def get_geolocation(ip):
    """Fetch geolocation data for an IP address"""
    try:
        response = requests.get(f"{IP_API_URL}{ip}", timeout=2)
        data = response.json()
        if data["status"] == "success":
            return data["lat"], data["lon"]
    except requests.RequestException:
        pass
    return None, None  # Default to None if lookup fails

def generate_heatmap(attack_data):
    """Generate a heatmap of attack locations"""
    plt.figure(figsize=(10, 6))
    m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=80,
                llcrnrlon=-180, urcrnrlon=180, resolution='c')

    m.drawcoastlines()
    m.drawcountries()
    
    lats, lons = [], []
    
    for entry in attack_data:
        lat, lon = get_geolocation(entry["attacker_ip"])
        if lat and lon:
            lats.append(lat)
            lons.append(lon)

    # Plot attack points
    if lats and lons:
        x, y = m(lons, lats)
        m.scatter(x, y, c="red", marker="o", alpha=0.5)

    plt.title("Cyber Attack Heatmap")
    
    # Save to in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    buf.seek(0)
    
    return buf

def upload_to_s3(image_buffer):
    """Upload heatmap image to S3"""
    try:
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=HEATMAP_IMAGE_NAME,
            Body=image_buffer,
            ContentType="image/png",
            ACL="public-read"
        )
        return f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{HEATMAP_IMAGE_NAME}"
    except Exception as e:
        print(f"❌ Failed to upload heatmap to S3: {e}")
        return None

def main():
    """Main function to generate and upload the heatmap"""
    print("📡 Fetching attack logs from DynamoDB...")
    attack_logs = get_attack_logs()

    if not attack_logs:
        print("⚠️ No attack logs found. Exiting.")
        return

    print("🗺️ Generating heatmap...")
    heatmap_buffer = generate_heatmap(attack_logs)

    print("☁️ Uploading heatmap to S3...")
    image_url = upload_to_s3(heatmap_buffer)

    if image_url:
        print(f"✅ Heatmap uploaded successfully: {image_url}")
    else:
        print("❌ Heatmap upload failed.")

if __name__ == "__main__":
    main()


