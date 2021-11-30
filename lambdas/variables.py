import logging
import base64
import json
import boto3
import os
import time
import requests
import math
import dateutil.parser
import datetime
import requests


ES_URL = "https://search-photos-tyy2xhbikqwrquuxoaok26pyym.us-east-1.es.amazonaws.com/photo-album/_doc"
ES_USER = 'prateek'
ES_PASS = 'Prateek@1709'