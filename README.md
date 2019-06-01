[![CodeFactor](https://www.codefactor.io/repository/github/simon987/ws_bucket/badge)](https://www.codefactor.io/repository/github/simon987/ws_bucket)
![GitHub](https://img.shields.io/github/license/simon987/ws_bucket_client.svg)

# ws_bucket_client
Python client for [ws_bucket](https://github.com/simon987/ws_bucket)

## Usage (Library)

```bash
git submodule add https://github.com/simon987/ws_bucket_client
python -m pip install -r ws_bucket_client/requirements.txt
```

In your project

```python
import datetime
from ws_bucket_client.api import WsBucketApi

WSB_API = "http://exemple-api-url/"
WSB_SECRET = "exemple_secret"  # Set to None for non-administrative usage
    
ws_bucket = WsBucketApi(WSB_API, WSB_SECRET)

# Allocate bucket (Requires secret)
ws_bucket.allocate(
    token="aj8209x48m",
    file_name="tmp_file.ndjson",
    max_size=1024 * 1024,
    upload_hook="rclone copy $1 my_gdrive:/wsb_tmp && rm $1",
    to_dispose_date=int(datetime.datetime.now().timestamp()) + 4000
  )

# Get bucket data
ws_bucket.read(token="aj8209x48m")

# Upload data to bucket, will trigger upload_hook
with open("my_file.ndjson", "rb") as f:
    ws_bucket.upload(token="aj8209x48m", stream=f, max_size=100000)
```
