import time
from datetime import datetime
from concurrent import futures
from geoalchemy2.functions import ST_AsText, ST_Point

import grpc
from shapely import wkb
import locations_pb2
import locations_pb2_grpc

from log import log
import DB

# creation_time = datetime.strptime("2020-07-07 10:38:06.00000",'%Y-%m-%d %H:%M:%S.%f+00:00'))

class LocationServicer(locations_pb2_grpc.LocationServiceServicer):
    def __init__(self) -> None:

        self.result = locations_pb2.LocationMessageList()

        first_location = locations_pb2.LocationMessage(
            id = 1,
            person_id = 1,
            longitude = "37.553441",
            latitude = "-122.290524",
            creation_time = "2020-07-07 10:37:06.000000"
        )
        second_location = locations_pb2.LocationMessage(
            id = 2,
            person_id = 2,
            longitude = "-122.290524",
            latitude = "37.553441",
            creation_time = "2020-07-07 10:38:06.000000"
        )

        self.result.locations.extend([first_location, second_location])

    def Get(self, request, context):
        log("Getting all locations from DB")
        return self.result

    def Create(self, request, context):
        log("Received a message!")

        request_value = {
            "id" : request.id,
            "person_id" : request.person_id,
            "longitude" : request.longitude,
            "latitude" : request.latitude,
            "creation_time" : request.creation_time
        }
        log(request_value)

        # DB.save_to_db(request_value)
        location = locations_pb2.LocationMessage(**request_value)

        self.result.locations.extend([location])

        return location 

    def GetLocation(self, request, context):
        log("GETLOCATION A LOCATION FROM DB")
        data = DB.getLocById(30)
        # log(data)
        data = DB.getLocById(request.id)[0]
        log(data)
        lon, lat = wkb.loads(data[2], hex=True).coords.xy
        response = {
            "id" : data[0],
            "person_id" : data[1],
            "longitude" : lon,
            "latitude" : lat,
            "creation_time" : data[3] 
        }
        log(response)
        return self.result.locations[0] 

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
locations_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


log("GRPC Location Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
