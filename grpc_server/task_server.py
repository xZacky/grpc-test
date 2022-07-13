# other
import time

# grpc
from . import task_pb2
from . import task_pb2_grpc

# img handler
from tools.img_handler import ImgEncode
from tools.img_handler import ImgDecode

# app
from app.app_api import APIFaceRecognition


class TaskServer(task_pb2_grpc.TaskServiceServicer):
    """grpc server远程函数调用"""

    def __init__(self):
        print("class TaskServer initial...")

    def task_face_recognition(self, request, context):
        """face_recoginiton remote server

        Args:
            request: message FaceRecognitionRequest {
                        int32 sequence = 1;
                        bytes img_orig = 2;
                        string target = 3;
                    }
        Returns:
           FaceRecognitionReplay: FaceRecognitionRequest {
                                    int32 sequence = 1;
                                    bytes img_orig = 2;
                                    string target = 3;
                                }
        """
        # 记录到达时间
        arrival_time = time.time()

        # 接收并处理参数
        sequence = request.sequence
        img_orig = ImgDecode(request.img_orig)
        target = request.target

        # 进行人脸识别, 识别结果编组发送给调用方
        start_handle_time = time.time()
        success, img_out = APIFaceRecognition(img_orig, target, sequence)
        end_handle_time = time.time()
        face_recognition_replay = task_pb2.FaceRecognitionReplay(sequence=sequence,
                                                                 img_out=ImgEncode(img_out, '.jpg'),
                                                                 success=success,
                                                                 arrival_time=str(arrival_time),
                                                                 start_handle_time=str(start_handle_time),
                                                                 end_handle_time=str(end_handle_time)
                                                                 )
        return face_recognition_replay

    def server_time_delta(self, request, context):
        return task_pb2.FaceRecognitionReplay(sequence=request.sequence,
                                              img_out=request.img_orig,
                                              success=True,
                                              arrival_time=str(time.time()),
                                              start_handle_time=str(0),
                                              end_handle_time=str(0)
                                              )