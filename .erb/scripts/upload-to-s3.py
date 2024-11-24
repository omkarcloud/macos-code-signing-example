from botasaurus import bt
from botasaurus.env import get_os
from botasaurus.task import task
import os

bucket_name = "awesome-app-distribution"

@task(output=None, raise_exception=True, close_on_crash=True, parallel=4)
def upload(data):
    upload_file_name = bt.trim_and_collapse_spaces(os.path.basename(data)).replace(' ','')
    
    uploaded_file_url = bt.upload_to_s3(
        data,
        bucket_name,
        os.environ['AWS_ACCESS_KEY_ID'],
        os.environ['AWS_SECRET_ACCESS_KEY'],
        upload_file_name,
    )
    
    print(f"Visit {uploaded_file_url} to download the uploaded file.") # URL to share with users

app_name = bt.read_json('./package.json')['build']['productName']
operating_system = get_os()

if operating_system == "mac":
    upload(f"./release/build/{app_name}.dmg")
elif operating_system == "windows":
    upload(f"./release/build/{app_name}.exe")
elif operating_system == "linux":
    upload(
        [
            f"./release/build/{app_name}-amd64.deb",
            f"./release/build/{app_name}-arm64.deb",
            f"./release/build/{app_name}-x86_64.rpm",
            f"./release/build/{app_name}-aarch64.rpm",
        ]
    )
