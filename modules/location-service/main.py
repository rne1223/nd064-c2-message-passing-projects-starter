import time
from concurrent import futures

import grpc
import locations_pb2
import locations_pb2_grpc


class LocationServicer(locations_pb2_grpc.LocationServiceServicer):
    def __init__(self) -> None:

        self.result = locations_pb2.LocationMessageList()

        first_location = locations_pb2.LocationMessage(
            id = 1,
            person_id = 1,
            longitude = "test",
            latitude = "test",
            creation_time = "2020-03-12",
        )
        second_location = locations_pb2.LocationMessage(
            id = 2,
            person_id = 2,
            longitude = "3",
            latitude = "4",
            creation_time = "2020-03-12",
        )

        self.result.orders.extend([first_location, second_location])

    def Get(self, request, context):

        # print(result)
        return self.result

    def Create(self, request, context):
        print("Received a message!")

        request_value = {
            "id" : request.id,
            "person_id" : request.person_id,
            "longitude" : request.longitude,
            "latitude" : request.latitude,
            "creation_time" : request.creation_time
        }
        print(request_value)

        order = locations_pb2.LocationMessage(**request_value)

        self.result.locations.extend([order])
        return order 

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
locations_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
