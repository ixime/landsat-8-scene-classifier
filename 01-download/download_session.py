"""
USGS Landsat 8 Scene Classification
01 Download
Scene downloader
"""
import re
import requests
import os

def _get_tokens(body):
	"""Get `csrf_token` and `ncforminfo`.
	Returns:
		str: csrf token 
		str: ncform info
	"""
	csrf = re.findall(r'name="csrf_token" value="(.+?)"', body)
	ncform = re.findall(r'name="__ncforminfo" value="(.+?)"', body)
	return csrf, ncform


class DownloadSession:
	"""Scene downloader"""
	def __init__(self, reqEE):
		self.reqEE = reqEE
		self.loginUrl = 'https://ers.cr.usgs.gov/login/'
		self.downloadUrl = 'https://earthexplorer.usgs.gov/download/12864/{}/STANDARD/EE'.format(reqEE.entityId)
		self.logoutUrl = 'https://earthexplorer.usgs.gov/logout'

	def downloadScene(self):
		"""Download scene's compressed file

		Open a session in USGS, download the scene's compressed file and logout.
		"""
		with requests.Session() as session:
			rsp  = session.get(self.loginUrl)
			csrf, ncform = _get_tokens(rsp.text)
			payload = {
				'username': self.reqEE.user,
				'password': self.reqEE.password,
				'csrf_token': csrf,
				'__ncforminfo': ncform
			}
			post = session.post(self.loginUrl, data=payload, allow_redirects=False)
			with session.get(self.downloadUrl, stream=True) as result:
				if (result.status_code != 400 and result.status_code != 401 and result.status_code != 404):
					with open(self.reqEE.displayId + '.tar.gz', 'wb') as f:
						for chunk in result.iter_content(chunk_size=5 * 1024**2):
							if chunk: # filter out keep-alive new chunks
								f.write(chunk)
								f.flush()
								os.fsync(f.fileno())
			session.get(self.logoutUrl)
