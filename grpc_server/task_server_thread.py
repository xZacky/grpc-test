# grpc
import grpc
from . import task_pb2_grpc
from . import task_server

from concurrent import futures

# other
import time
import threading


class TaskServerThread(threading.Thread):
    def __init__(self, ip, port):
        super(TaskServerThread, self).__init__()
        self.ip = ip
        self.port = port

    def run(self) -> None:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        service = task_server.TaskServer()
        task_pb2_grpc.add_TaskServiceServicer_to_server(service, server)
        server.add_insecure_port("[::]:" + str(self.port))

        server.start()
        print("grpc服务已启动, ip: {}, port: {}".format(self.ip, self.port))
        server.wait_for_termination()
        print("grpc服务结束!")


def GetClientStub(ip, port):
    """获取grpc客户端

    Args:
        ip: grpc服务的ip地址
        port: grpc服务的端口号
    Returns:
        stub: grpc客户端
    """
    channel = grpc.insecure_channel(str(ip) + ":" + str(port))
    client_stub = task_pb2_grpc.TaskServiceStub(channel)

    return client_stub
