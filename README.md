# AWS_S3_Enumerations

## About
A Python Web based tool to enumerate AWS S3 buckets using different permutations

## Installation
After cloning the repository and navigating to the created folder, simply run:
```bash
pip install -r requirements.txt
```

## Usage
```bash

python lazys3.py --help

usage: lazys3.py [-h] [-p PREFIXES] [-l LIMIT] [-u USER_AGENT] target

Bruteforce AWS s3 buckets using different permutations

positional arguments:
  target                which target to scan

optional arguments:
  -h, --help            show this help message and exit
  -p PREFIXES, --prefixes PREFIXES
                        prefixes file to use (default:
                        lists/common_bucket_prefixes.txt)
  -l LIMIT, --limit LIMIT
                        rate limit the http requests (default: 100)
  -u USER_AGENT, --user-agent USER_AGENT
                        which user agent to use when sending requests
                        (default: aiohttp client 0.17)
```




