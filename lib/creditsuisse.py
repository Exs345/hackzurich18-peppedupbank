#!/usr/bin/env python3

import requests
import logging
import json

class credit_suisse:
	def __init__(self):

		self._session = requests.Session()
		self._session.auth = None
		self._session.headers.update({
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik9UUXlRVGRCTkRFNU1rWTNNMFZFTnpNeU9EWkJOa1pETkRCR1FrRkZOamxDTTBJeE5EazRNdyJ9.eyJpc3MiOiJodHRwczovL2dicHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWI5Y2QwZTc3MmQ0YmI0N2Y5YTdjZmZlIiwiYXVkIjpbImh0dHBzOi8vb3BlbmJhbmtpbmcuY29tL2FwaSIsImh0dHBzOi8vZ2Jwcm9qZWN0LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1MzcwMDM4OTgsImV4cCI6MTUzNzA5MDI5OCwiYXpwIjoicThJTVlzMVNLekt0WExvdjhWM0pab3oxaE43MHgzQTciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZ3R5IjoicGFzc3dvcmQifQ.Ko7O6k5zVBgE7zjh4qREM82y8v-_Crz2QzR-m_-xgUk7e0-7vKceAuBZfEuMxW2Le5wx5oP3xI6h-SIEQ7Lnfzsy1N8gZijsSymjKl_u6N-qiUu3iC0NiRmnDauQ3a8blz6aPrJtWs_j7XnLnp5KPALSzhH-zpxg8XwmJaHIF18JNp3J1w0lupTN28nue1zAfIxWFLweS_Vl894CV5K4hQU08wx2YT7_4XO7TMqAxpx4o-eTn2qBtiDGq0lx7sEwwHgqqT2z6gTBiHy9Y4Zl7prUihPyIh3GvhERg-J7_T5HeFPmAxcqH_RboxBE_34H__bLjj8rKCsMZ31-iZ8Haw",
			'cache-control': "no-cache",
			'postman-token': "8750c4af-6000-f48b-0a73-9954e95cfcb5"
			})
		self._base_url = 'https://csopenbankingzh.azurewebsites.net'

	def _url(self, url):
		return self._base_url + url

	def request(self, verb, url, headers={}, input=None):
		try:
			response = self._session.request(verb, url=self._url(url), headers=headers, data=json.dumps(input), allow_redirects = True)
		except requests.TooManyRedirects as e:
			response = e.response

		try:
			output = response.json()
		except json.JSONDecodeError:
			output = {}

		return response

	def get_user_data(self, userId):
		res = self.request('POST', url = '/customers/search/unsecured', input = {
		"filter" : [
			{
				"attribute": "kyc.job" ,
				"operator": "like" ,
				"value": "'%RETIRED%'"
			},
			{
				"attribute": "id" ,
				"operator": "like" ,
				"value": userId
			}
		],
		"sorting": " nickname asc"
		});

		return res.json()


def main():
	cs = credit_suisse()
	print(cs.get_user_data(600014))


if __name__ == "__main__":
	main()

