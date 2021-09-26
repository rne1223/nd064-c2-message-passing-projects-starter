import time
from concurrent import futures

import grpc
import order_pb2
import order_pb2_grpc


class OrderServicer(order_pb2_grpc.OrderServiceServicer):
    def __init__(self) -> None:
        self.result = order_pb2.OrderMessageList()

        first_order = order_pb2.OrderMessage(
            id="2222",
            created_by="USER123",
            status=order_pb2.OrderMessage.Status.QUEUED,
            created_at='2020-03-12',
            equipment=[order_pb2.OrderMessage.Equipment.KEYBOARD]
        )

        second_order = order_pb2.OrderMessage(
            id="3333",
            created_by="USER123",
            status=order_pb2.OrderMessage.Status.QUEUED,
            created_at='2020-03-11',
            equipment=[order_pb2.OrderMessage.Equipment.MOUSE]
        )
        self.result.orders.extend([first_order, second_order])

    def Get(self, request, context):

        # print(result)
        return self.result

    def Create(self, request, context):
        print("Received a message!")

        request_value = {
            "id": request.id,
            "created_by": request.created_by,
            "status": request.status,
            "created_at": request.created_at,
            "equipment": request.equipment 
        }
        print(request_value)

        order = order_pb2.OrderMessage(**request_value)

        self.result.orders.extend([order])
        return order 


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
order_pb2_grpc.add_OrderServiceServicer_to_server(OrderServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
