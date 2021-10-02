import time
from datetime import datetime
from concurrent import futures

import grpc
import locations_pb2
import locations_pb2_grpc

from log import log
# import DB
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
        # print(result)
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
        log("GetLocation a location from DB")
        request_value = {
            "id" : request.id,
        }
        log(request_value)

        return self.result.locations[request.id] 

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
