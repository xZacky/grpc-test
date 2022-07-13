import sys
print(sys.path)

# grpc server
from grpc_server.task_server_thread import TaskServerThread
from grpc_server import task_pb2_grpc

# constant
grpc_ip = '127.0.0.1'
grpc_port = 10000

if __name__ == '__main__':
    grpc_thread = TaskServerThread(grpc_ip, grpc_port)
    grpc_thread.start()
    while True:
        a = 1