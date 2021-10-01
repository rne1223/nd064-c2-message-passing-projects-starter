import grpc
import locations_pb2
import locations_pb2_grpc
from app.misc import log


class GRPC_Server:
    def __init__(self, service=None, port=None):
        log("connecting to GRCP server")
        self.channel = grpc.insecure_channel("udaconnect-location-service:5005")
        log("connected to GRCP server")
        self.stub = locations_pb2_grpc.LocationServiceStub(self.channel)

    # Returns all the locations
    def Get(self):

        log("Getting All Locations from DB")
        response = self.stub.Get(locations_pb2.Empty())
        return response

    def GetLocation(self, id=None):

        response = [{}] 

        if(id is None):
            response = self.Get()
            log(response)
        else:
            log("Getting Unique Location from DB")
            location_id = locations_pb2.UniqueLocationMessage(id=0)
            response = self.stub.GetLocation(location_id)
            log(response)
        
        return response

    def CreateLocation(self,location_data=None):
        pass


# response = stub.Get(locations_pb2.Empty())
# location = locations_pb2.LocationMessage(
#             id = 2,
#             person_id = 2,
#             longitude = "3",
#             latitude = "4",
#             creation_time = "2020-03-12",
#         )

# response = stub.Create(location)
# print(response)



# location_id = locations_pb2.UniqueLocationMessage(id=0)
# response = stub.GetLocation(location_id)
print(response)