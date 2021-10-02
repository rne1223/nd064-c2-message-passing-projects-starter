import grpc
import locations_pb2
import locations_pb2_grpc
from app.misc import log

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

channel = grpc.insecure_channel("udaconnect-location-service:5002")
stub = locations_pb2_grpc.LocationServiceStub(channel)


def _getAllLocations():
    response = stub.Get(locations_pb2.Empty())
    return response

def getLocation(lid=None):
    response = [{}] 

    if(lid is None):
        response = _getAllLocations() 
    else:
        # log("Getting Unique Location from DB")
        location_id = locations_pb2.UniqueLocationMessage(lid)
        response = stub.GetLocation(location_id)

    return response

def createLocation(location_data=None):
    location = locations_pb2.LocationMessage(
                id = 2,
                person_id = 2,
                longitude = "3",
                latitude = "4",
                creation_time = "2020-03-12",
            )
    response = stub.Create(location)
    return response
