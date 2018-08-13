"""
USGS Landsat 8 Scene Classification
01 Download
Downloads one Landsat 8 OLI/TIRS C1 Level-1 Scene in a compressed file tar.gz
through the USGS/EROS API
"""
import os
from dotenv import load_dotenv, find_dotenv
import argparse
from requests_ee import RequestsEE
from download_session import DownloadSession

# Load credentials from .env
load_dotenv(find_dotenv())
USER = os.environ.get('USUARIO')
PASSWORD = os.environ.get('PASSWORD')

parser = argparse.ArgumentParser()
parser.add_argument("--row", help="row of scene", required=True, type=int)
parser.add_argument("--path", help="path of scene", required=True, type=int)
parser.add_argument("--date", help="date of scene", required=True, type=str)
args = parser.parse_args()

# Get scene's IDs through USGS/EROS API wrapper
reqEE = RequestsEE(args.path, args.row, args.date, USER, PASSWORD)
reqEE.getSceneID()

# Download scene's compressed file
dwnlSess = DownloadSession(reqEE)
dwnlSess.downloadScene()

print('Downloaded successfully')



