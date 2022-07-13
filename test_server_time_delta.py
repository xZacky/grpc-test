# grpc server
from grpc_server.task_server_thread import GetClientStub
from grpc_server import task_pb2
from tools.img_handler import ImgEncode

# data processing
import time
import numpy as np
import pandas as pd
import cv2

# constant
time_delta_test_rounds = 100
test_rounds = 100
server1 = 'win'
server2 = 'win'
writer_path = server1 + '_to_' + server2 + '_net_delay.xlsx'
grpc_ip = '127.0.0.1'
grpc_port = 10000
img_path = './test_grpc.jpg'

if __name__ == "__main__":
    img = cv2.imread(img_path)
    img_orig = ImgEncode(img, ".jpg")

    # get grpc client
    client_stub = GetClientStub(grpc_ip, grpc_port)
    delta_time = []

    for test_round in range(1, time_delta_test_rounds + 1):
        if test_round % 1000 == 0:
            print(str(test_round / 1000) + ": " + str(time.time()))
        start_request_time = time.time()
        arrival_time = float(client_stub.server_time_delta(
            task_pb2.FaceRecognitionRequest(sequence=0, img_orig=img_orig, target="wgk")).arrival_time)
        end_request_time = time.time()
        delta_time.append((end_request_time + start_request_time) / 2 - arrival_time)

    average_time_delta = np.mean(np.array(delta_time))
    print(server1 + ' and ' + server2 + ' time_delta: {}'.format(average_time_delta))

    time_data = {}
    for test_round in range(1, test_rounds + 1):
        if test_round % 1000 == 0:
            print('网络延迟测试：' + str(test_round / 1000) + ": " + str(time.time()))
        start_request_time = time.time()
        arrival_time = float(client_stub.server_time_delta(
            task_pb2.FaceRecognitionRequest(sequence=0, img_orig=img_orig, target="wgk")).arrival_time)
        end_request_time = time.time()
        time_data[test_round] = {}
        time_data[test_round]['test_round'] = test_round
        time_data[test_round]['start_request_time'] = start_request_time
        time_data[test_round]['arrival_time'] = arrival_time
        time_data[test_round]['end_request_time'] = end_request_time

    df = pd.DataFrame(data=time_data).T
    df['relative_net_delay'] = df['arrival_time'] + average_time_delta - df['start_request_time']
    df['absolute_net_delay'] = (df['end_request_time'] - df['start_request_time']) / 2
    writer = pd.ExcelWriter(writer_path)
    df.to_excel(writer, index=False)
    writer.save()
    writer.close()