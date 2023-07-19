from bing_image_downloader.downloader import download
import glob
import pandas as pd
import os
import sys
import requests

crawled_image_path = 'crawled_image/'

download('아파트 외벽 만화벽화', limit=200,  output_dir=crawled_image_path, adult_filter_off=True, force_replace=False, timeout=60, verbose=True)