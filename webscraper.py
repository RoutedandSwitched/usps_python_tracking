
from bs4 import BeautifulSoup as bs
import requests
import datetime
import json


class USPSTracking:
    def __init__(self):
        self.client = requests.Session()
        self.client.headers.update(self._header())

    def _header(self):
        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Max OS X 10_9_2) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"

        }
        return header

    @property
    def base_url(self):
        return 'https://tools.usps.com/go/TrackConfirmAction.action'

    def get(self, tracking_number:str):
        full_url = f'{self.base_url}?tlabels={tracking_number}'
        response = self.client.get(
            url=full_url,
            allow_redirects=False
        )
        data = self._tracking_html_parser(response.text)
        data_json = json.dumps(data, indent=4)
        return data_json

    def _tracking_html_parser(self,data:str):
        page = bs(data, 'html.parser')
        tracking_status = page.findAll('div', {'class':'current-step'})
        for item in tracking_status:
            #Status Value
            status_container = item.findAll('p', {'class': 'tb-status'})
            status = status_container[0].text.strip()
            #Status Detail Value
            status_detail_container = item.findAll('p', {'class': 'tb-status-detail'})
            status_detail = status_detail_container[0].text.strip()
            #Location
            location_container = item.findAll('p', {'class': 'tb-location'})
            location = location_container[0].text.strip()
            #Date
            date_container = item.findAll('p', {'class': 'tb-date'})
            date_split = date_container[0].text.strip().split(',')
            date_str = date_split[0] + date_split[1] + ' ' + date_split[2].replace('\n', '').replace('\t', '')
            date_format = '%B %d %Y %H:%M %p'
            date = datetime.datetime.strptime(date_str, date_format)
            
            data_dict = {
                'status': status,
                'status_detail': status_detail,
                'location': location,
                'date': str(date)

            }
        return data_dict





