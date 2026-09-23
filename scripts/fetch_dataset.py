# AI GENERATED script to fetch MIT-Adobe FiveK dataset images from Kaggle, 
# requires Kaggle API setup

import os
from kaggle.api.kaggle_api_extended import KaggleApi

# Initialize and authenticate
api = KaggleApi()
api.authenticate()

# Configuration
dataset_name = "aasifkhanm/image-exposure-dataset"
local_path = "images/test_directory/OverExposed"
image_limit = 50

os.makedirs(local_path, exist_ok=True)
print("Paginating through Kaggle server to find OverExposed images (this may take a moment)...")

image_files = []
page_token = None

# Loop through the pages until we hit the 'O' folder and grab 50 images
while len(image_files) < image_limit:
    # Pull up to 200 files per page to speed up the search
    response = api.dataset_list_files(dataset_name, page_size=200, page_token=page_token)
    
    if not hasattr(response, 'files') or not response.files:
        break

    for f in response.files:
        if "overexposed" in f.name.lower() and f.name.lower().endswith((".jpg", ".jpeg", ".png")):
            image_files.append(f)
            if len(image_files) == image_limit:
                break
    
    # Grab the token for the next page of results
    page_token = getattr(response, 'nextPageToken', getattr(response, 'next_page_token', None))
    if not page_token:
        break

print(f"\nFound {len(image_files)} matching images. Downloading...")

# Download the specified subset
for file_obj in image_files:
    api.dataset_download_file(
        dataset=dataset_name,
        file_name=file_obj.name, 
        path=local_path,
        force=True,
        quiet=True,
    )
    print(f"Downloaded: {file_obj.name.split('/')[-1]}")