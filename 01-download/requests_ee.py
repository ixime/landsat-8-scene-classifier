"""
USGS Landsat 8 Scene Classification
01 Download
USGS/EROS API wrapper
"""
import requests
import json

class RequestsEE:
	"""USGS/EROS API wrapper"""
	def __init__(self, path, row, date, user, password):
		"""
		Args:
			path (int): The path of the scene
			row (int): The row of the scene
			date (str): The date required to look for the scene
			user (str): The user required for authentication in the USGS/EROS API
			password (str): The password required for authentication in the USGS/EROS API  
		"""
		self.urlbase = "https://earthexplorer.usgs.gov/inventory/json/v/1.4.0/"
		self.path = path
		self.row = row
		self.date = date
		self.user = user
		self.password = password

	def getSceneID(self):
		"""Get scene's IDs
		Get entity Id  and display Id required to download the scene's compressed file.

		Get IDs required to download the scene. For that, we first authenticate the user
		and get the API key, then we get the coordinates corresponding the path and row of the scene.
		The coordenates correspond to a WRS2 grid type. With them we look for the IDs corresponding 
		to the given date. Finally we logout. 
		"""
		payload = {
		"username": self.user,
		"password": self.password,
		"authType": "EROS",
		"catalogId": "EE"
		}
		resp = requests.post(url=self.urlbase+'login', data={'jsonRequest':json.dumps(payload)})
		APIkey = resp.json()['data']

		payload = {
		"gridType": "WRS2",
		"responseShape": "polygon",
		"path": self.path, #26
		"row": self.row #47
		}
		resp = requests.get(url=self.urlbase+'grid2ll', params={'jsonRequest':json.dumps(payload)})

		upperRightLat = resp.json()['data']['coordinates'][0]['latitude']
		upperRightLon = resp.json()['data']['coordinates'][0]['longitude']
		lowerLeftLat = resp.json()['data']['coordinates'][2]['latitude']
		lowerLeftLon = resp.json()['data']['coordinates'][2]['longitude']

		payload = {
		"datasetName": "LANDSAT_8_C1",
		"spatialFilter": {
			"filterType": "mbr",
			"lowerLeft": {
				"latitude": lowerLeftLat,
				"longitude": lowerLeftLon
				},
			"upperRight": {
				"latitude": upperRightLat,
				"longitude": upperRightLon 
				}
			},
		"temporalFilter": {
			"startDate": self.date, #"2018-01-10"
			"endDate": self.date #"2018-01-10"
			},
		"maxResults": 30,
		"startingNumber": 1,
		"sortOrder": "ASC",
		"apiKey": APIkey
		}
		resp = requests.get(url=self.urlbase+'search', params={'jsonRequest':json.dumps(payload)})

		results = resp.json()['data']['results']
		info = [[re['entityId'], re['displayId']] for re in results if 'Path: ' + str(self.path) + ', Row: ' + str(self.row) in re['summary'] ]
		print(info)
		self.entityId = info[0][0]
		self.displayId = info[0][1]

		payload = {
		"apiKey": APIkey
		}
		resp = requests.get(url=self.urlbase+'logout', params={'jsonRequest':json.dumps(payload)})
