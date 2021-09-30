import grpc
import locations_pb2
import locations_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = locations_pb2_grpc.LocationServiceStub(channel)

# response = stub.Get(locations_pb2.Empty())
location = locations_pb2.LocationMessage(
            id = 2,
            person_id = 2,
            longitude = "3",
            latitude = "4",
            creation_time = "2020-03-12",
        )

# response = stub.Create(location)
# print(response)
# response = stub.Get(locations_pb2.Empty())
# print(response)

location_id = locations_pb2.UniqueLocationMessage(id=0)
response = stub.GetLocation(location_id)
print(response)