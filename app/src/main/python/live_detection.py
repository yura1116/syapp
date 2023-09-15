import imutils
from scipy.spatial import distance as dist
from imutils import face_utils
import time
import dlib
import cv2
import random

def eye_aspect_ratio(eye):
    # 计算两组垂直眼睛地标(x, y)坐标之间的欧式距离
    A = dist.euclidean(eye[1], eye[5])  # 计算第一个和第五个点之间的距离
    B = dist.euclidean(eye[2], eye[4])  # 计算第二个和第四个点之间的距离
    # 计算一组水平眼睛地标(x, y)坐标之间的欧式距离
    C = dist.euclidean(eye[0], eye[3])  # 计算第一个和第三个点之间的距离
    # 计算眼睛纵横比
    ear = (A + B) / (2.0 * C)  # 计算眼睛纵横比
    return ear

def mouth_aspect_ratio(mouth):
    # 计算嘴巴纵横比
    A = dist.euclidean(mouth[1], mouth[11])  # 计算第一个和第十一个点之间的距离
    B = dist.euclidean(mouth[2], mouth[10])  # 计算第二个和第九个点之间的距离
    C = dist.euclidean(mouth[3], mouth[9])   # 计算第三个和第八个点之间的距离
    D = dist.euclidean(mouth[4], mouth[8])   # 计算第四个和第七个点之间的距离
    E = dist.euclidean(mouth[5], mouth[7])   # 计算第五个和第六个点之间的距离

    F = dist.euclidean(mouth[0], mouth[6])   # 计算第一个和第六个点之间的距离

    mouth_ratio = (A + B + C + D + E) / (5.0 * F)  # 计算嘴巴纵横比
    return mouth_ratio

def left_right_face_ratio(face):
    # 计算左右脸部的宽度比例
    leftA = dist.euclidean(face[0], face[27])  # 计算左脸宽度
    leftB = dist.euclidean(face[2], face[30])  # 计算左脸宽度
    leftC = dist.euclidean(face[4], face[48])  # 计算左脸宽度
    rightA = dist.euclidean(face[16], face[27])  # 计算右脸宽度
    rightB = dist.euclidean(face[14], face[30])  # 计算右脸宽度
    rightC = dist.euclidean(face[12], face[54])  # 计算右脸宽度

    ratioA = rightA / leftA  # 计算右脸宽度与左脸宽度的比例
    ratioB = rightB / leftB  # 计算右脸宽度与左脸宽度的比例
    ratioC = rightC / leftC  # 计算右脸宽度与左脸宽度的比例
    face_ratio = (ratioA + ratioB + ratioC) / 3  # 计算左右脸部宽度比例的平均值
    return face_ratio

def live_detection(shape_predictor_path):
    # 接受 shape_predictor_68_face_landmarks.dat 文件的路径作为参数
    EYE_AR_THRESH = 0.25  # 眼睛纵横比阈值，用于检测闭眼状态
    EYE_AR_CONSEC_FRAMES = 2  # 连续帧数，用于判定闭眼状态

    COUNTER = 0  # 闭眼帧计数器
    TOTAL = 0  # 闭眼总计数器
    OPEN_MOUTH_COUNTER = 0  # 张嘴帧计数器
    MOUTH_TOTAL = 0  # 张嘴总计数器
    TRUE_LEFT_TOTAL = 0  # 左转头总计数器
    TRUE_RIGHT_TOTAL = 0  # 右转头总计数器
    TRUE_LEFT_COUNTER = 0  # 左转头帧计数器
    TRUE_RIGHT_COUNTER = 0  # 右转头帧计数器

    random_number = random.randint(1, 2)  # 随机生成一个数字，用于选择检测模式
    print("[INFO]正在加载面部特征点检测器...")
    detector = dlib.get_frontal_face_detector()  # 获取人脸检测器
    predictor = dlib.shape_predictor(shape_predictor_path)  # 获取人脸特征点检测模型

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']  # 获取左眼特征点索引范围
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']  # 获取右眼特征点索引范围
    (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS['mouth']  # 获取嘴巴特征点索引范围
    print("[INFO] 启动视频流线程...")

    fileStream = True  # 文件流标志
    video_capture = cv2.VideoCapture(0)  # 打开摄像头
    fileStream = False  # 文件流标志
    textColor = (255, 0, 0)  # 文本颜色（蓝色）
    start_time = time.time()  # 记录程序开始时间
    for i in range(5):
        ret, frame = video_capture.read()  # 读取摄像头帧
        frame = cv2.flip(frame, 1)  # 翻转图像，使显示为镜像效果
        output_path = 'app/src/main/face_images/face_{i}.jpg'  # 生成文件名
        cv2.imwrite(output_path, frame)  # 保存图像

        time.sleep(0.5)  # 等待0.5秒

    while True:
        ret, frame = video_capture.read()  # 读取摄像头帧
        frame = cv2.flip(frame, 1)  # 翻转图像，使显示为镜像效果
        frame = imutils.resize(frame)  # 调整图像大小

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 将图像转换为灰度图

        rects = detector(gray, 0)  # 通过人脸检测器检测人脸
        if len(rects) > 1:
            cv2.putText(frame, 'More Face!', (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            print("检测到多个人脸，请只保留一个人脸在镜头范围内")
            livedetection = 2  # 表示检测到多个人脸
            return livedetection
            continue
        for rect in rects:
            shape = predictor(gray, rect)  # 通过特征点检测模型获取人脸特征点
            shape = face_utils.shape_to_np(shape)  # 转换为NumPy数组

            leftEye = shape[lStart:lEnd]  # 提取左眼特征点
            rightEye = shape[rStart:rEnd]  # 提取右眼特征点
            mouth = shape[mStart:mEnd]  # 提取嘴巴特征点

            leftEAR = eye_aspect_ratio(leftEye)  # 计算左眼纵横比
            rightEAR = eye_aspect_ratio(rightEye)  # 计算右眼纵横比
            mouthRatio = mouth_aspect_ratio(mouth)  # 计算嘴巴纵横比
            leftrightRatio = left_right_face_ratio(shape)  # 计算左右脸部宽度比例

            ear = (leftEAR + rightEAR) / 2.0  # 计算平均纵横比

            # 绘制轮廓（注释掉的代码）
            # leftEyeHull = cv2.convexHull(leftEye)
            # rightEyeHull = cv2.convexHull(rightEye)
            # mouthHull = cv2.convexHull(mouth)
            # cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            # cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            # cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)

            print('leftRightRatio:', leftrightRatio)

            if mouthRatio > 0.7:
                OPEN_MOUTH_COUNTER += 1
            else:
                if OPEN_MOUTH_COUNTER >= 2:
                    MOUTH_TOTAL += 1
                OPEN_MOUTH_COUNTER = 0
            if leftrightRatio >= 2.0:
                TRUE_RIGHT_COUNTER += 1
            elif leftrightRatio <= 1.0:
                TRUE_LEFT_COUNTER += 1
            else:
                if TRUE_LEFT_COUNTER >= 2:
                    TRUE_RIGHT_TOTAL += 1
                if TRUE_RIGHT_COUNTER >= 2:
                    TRUE_LEFT_TOTAL += 1

                TRUE_LEFT_COUNTER = 0
                TRUE_RIGHT_COUNTER = 0

            if ear < EYE_AR_THRESH:
                COUNTER += 1
            else:
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1
                    if TRUE_RIGHT_TOTAL >= 1 and TRUE_LEFT_TOTAL >= 1 and MOUTH_TOTAL >= 1:
                        TRUE_LEFT_TOTAL = 0
                        TRUE_RIGHT_TOTAL = 0
                        MOUTH_TOTAL = 0
                        random_number = random.randint(1, 2)

                COUNTER = 0

            if random_number == 1:
                if TRUE_LEFT_TOTAL > 0:
                    if TRUE_RIGHT_TOTAL > 0:
                        if MOUTH_TOTAL > 0:
                            livedetection = 1  # 表示活体检测通过
                            return livedetection, output_path
                        else:
                            cv2.putText(frame, 'Open Mouth', (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, textColor, 2)
                    else:
                        cv2.putText(frame, 'Turn Right Face', (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, textColor, 2)
                        MOUTH_TOTAL = 0
                else:
                    cv2.putText(frame, 'Turn Left Face', (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, textColor, 2)
                    MOUTH_TOTAL = 0
                    TRUE_RIGHT_TOTAL = 0
            elif random_number == 2:
                if MOUTH_TOTAL > 0:
                    if TRUE_RIGHT_TOTAL > 0:
                        if TRUE_LEFT_TOTAL > 0:
                            livedetection = 1  # 表示活体检测通过
                            return livedetection, output_path
                        else:
                            cv2.putText(frame, 'Turn Left Face', (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, textColor, 2)
                    else:
                        cv2.putText(frame, 'Turn Right Face', (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, textColor, 2)
                        TRUE_LEFT_TOTAL = 0
                else:
                    cv2.putText(frame, 'Open Mouth', (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, textColor, 2)
                    TRUE_LEFT_TOTAL = 0
                    TRUE_RIGHT_TOTAL = 0

        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 60:  # 超过60秒
            print("Timeout，超时")
            livedetection = 0  # 表示活体检测超时
            return livedetection

        if len(rects) == 0:
            cv2.putText(frame, 'No Face Detected!', (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Frame", frame)  # 显示帧
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
