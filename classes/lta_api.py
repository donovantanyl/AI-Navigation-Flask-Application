import json
from urllib.parse import urlparse
from datetime import datetime, timedelta
import httplib2 as http


class BusArrival:
    def __init__(self, num, est):
        self.__num = num
        self.__est = est

    def get_num(self):
        return self.__num

    def get_est(self):
        return self.__est


# Writes arriving busses for specified bus stop to bus_arr.txt file every minute
def bus_order(bus_code, api_key):
    # API Key and format
    headers = {
        'AccountKey': api_key,
        'accept': 'application/json'
    }

    uri = "http://datamall2.mytransport.sg/"
    path = "ltaodataservice/BusArrivalv2"
    query = "?BusStopCode="
    h = http.Http()
    while True:
        target = urlparse(uri + path + query + bus_code)  # Parse API URI
        method = "GET"
        body = ""
        response, content = h.request(
            target.geturl(),
            method,
            body,
            headers
        )
        json_obj = json.loads(content)
        bus_list = []
        datetime_format = "%Y-%m-%dT%H:%M:%S+08:00"
        for service in json_obj.get("Services"):
            for i in range(1, 4):
                count = ""
                if i > 1:
                    count = str(i)
                if try_parse(service.get(f"NextBus{count}").get("EstimatedArrival")):
                    bus_list.append(BusArrival(service.get("ServiceNo"),
                                               datetime.strptime(service.get(f"NextBus{count}").get("EstimatedArrival"),
                                                                 datetime_format)))
        sorted_bus_list = list(map(lambda x: x.get_num(),
                                   filter(lambda y: y.get_est() < datetime.now() + timedelta(minutes=3),
                                          sorted(bus_list, key=lambda x: x.get_est()))))


# Check if you can parse as datetime object
def try_parse(dt):
    try:
        datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S+08:00")
        return True
    except ValueError:
        return False
