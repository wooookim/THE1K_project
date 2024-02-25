# from google.cloud import storage
# import os
# import base64
# from google.cloud import aiplatform
# import json
# import sqlite3

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="team05-project-c7a54e239686.json"

# def analyze_single_image(image_blob_name):
#     # Google Cloud Storage 클라이언트 생성
#     storage_client = storage.Client()

#     # 버킷 객체 생성
#     BUCKET_NAME = "video_file_upload_test"
#     bucket = storage_client.bucket(BUCKET_NAME)

#     # 이미지 Blob 가져오기
#     blob = bucket.blob(image_blob_name)

#     # 이미지 다운로드
#     image_bytes = blob.download_as_bytes()

#     # 이미지 파일 인코딩
#     encoded_content = base64.b64encode(image_bytes).decode("utf-8")

#     # 예측 요청 생성
#     instance = {"content": encoded_content}
#     instances = [instance]

#     # 모델 파라미터 설정
#     parameters = {"max_predictions": 10}

#     # 클라이언트 초기화 및 예측 수행
#     client_options = {"api_endpoint": "us-central1-aiplatform.googleapis.com"}  # ENDPOINT_API 대신 api_endpoint 사용
#     client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
#     endpoint = client.endpoint_path(
#         project="team05-project", location="us-central1", endpoint= "8588041232976969728"
#     )
#     response = client.predict(
#         endpoint=endpoint, instances=instances, parameters=parameters
#     )

#     # 예측 결과 수집
#     predictions = response.predictions
#     predictions_json = [dict(prediction) for prediction in predictions]

#     return predictions_json


# # GCS에서 분석할 이미지의 Blob 이름 지정
# image_blob_name = "User.id_20240224190037_7.jpg"

# # 이미지 분석 실행
# results = analyze_single_image(image_blob_name)

# # 결과 출력
# print(results)

######################################################   이미지 하나를 분석

from google.cloud import storage
import os
import base64
from google.cloud import aiplatform
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="team05-project-c7a54e239686.json"

def analyze_images_in_folder(folder_blob_name):
    # Google Cloud Storage 클라이언트 생성
    storage_client = storage.Client()

    # 버킷 객체 생성
    BUCKET_NAME = "video_file_upload_test"
    bucket = storage_client.bucket(BUCKET_NAME)

    # 폴더 내 이미지 목록 가져오기
    blobs = bucket.list_blobs(prefix=folder_blob_name)

    result = []
    
    # 각 이미지에 대한 분석 수행
    for blob in blobs:
        if blob.name.endswith('.jpg') or blob.name.endswith('.jpeg') or blob.name.endswith('.png'):
            # 이미지 다운로드
            print("이미지 다운로드:", blob.name)
            image_bytes = blob.download_as_bytes()

            # 이미지 파일 인코딩
            print("이미지 인코딩:", blob.name)
            encoded_content = base64.b64encode(image_bytes).decode("utf-8")

            # 예측 요청 생성
            instance = {"content": encoded_content}
            instances = [instance]

            # 모델 파라미터 설정
            parameters = {"max_predictions": 10}

            # 클라이언트 초기화 및 예측 수행
            client_options = {"api_endpoint": "us-central1-aiplatform.googleapis.com"}
            client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
            endpoint = client.endpoint_path(
                project="team05-project", location="us-central1", endpoint= "8588041232976969728"
            )
            response = client.predict(
                endpoint=endpoint, instances=instances, parameters=parameters
            )

            # 예측 결과 수집
            predictions = response.predictions
            predictions_json = [dict(prediction) for prediction in predictions]
            
            result.append({blob.name: predictions_json}) #????????
    
    return result

# def count_concentration_predictions(predictions):
#     # 집중 카운트 초기화
#     concentration_count = 0
    
#     # 각 예측 결과에 대해 확인
#     for prediction in predictions:
#         # 예측 결과 가져오기
#         prediction_result = list(prediction.values())[0][0]  # 예측 결과는 리스트의 첫 번째 요소
        
#         # 예측 결과의 confidences 가져오기
#         confidences = prediction_result.get("confidences", [])
        
#         # 첫 번째 인덱스 값이 두 번째 인덱스 값보다 큰지 확인
#         if len(confidences) >= 2 and confidences[0] > confidences[1]:
#             concentration_count += 1
    
#     return concentration_count

def count_concentration_predictions(predictions_by_folder):
    # 각 하위 폴더별 집중 카운트를 저장할 딕셔너리 초기화
    concentration_counts = {}

    # 각 하위 폴더별로 예측 결과에 대해 확인
    for folder, predictions in predictions_by_folder.items():
        # 집중 카운트 초기화
        concentration_count = 0
        
        # 각 예측 결과에 대해 확인
        for prediction in predictions:
            # 예측 결과 가져오기
            prediction_result = list(prediction.values())[0][0]  # 예측 결과는 리스트의 첫 번째 요소
            
            # 예측 결과의 confidences 가져오기
            confidences = prediction_result.get("confidences", [])
            
            # 첫 번째 인덱스 값이 두 번째 인덱스 값보다 큰지 확인
            if len(confidences) >= 2 and confidences[0] > confidences[1]:
                concentration_count += 1
        
        # 하위 폴더 별 집중 카운트를 딕셔너리에 저장
        concentration_counts[folder] = concentration_count
    
    return concentration_counts

# GCS에서 분석할 이미지가 있는 폴더 지정
folder_blob_name = "한수진_2024_02_25_16_22"

# 이미지 분석 실행
result = analyze_images_in_folder(folder_blob_name)

# 결과 출력
print(result)

concentration_count = count_concentration_predictions(result)

print("집중하는 예측 횟수:", concentration_count)











#################################################

# def convert_repeated_composite_to_dict(repeated_composite):
#     """
#     RepeatedComposite 객체를 딕셔너리로 변환하는 함수
#     """
#     results = []
#     for item in repeated_composite:
#         item_dict = {}
#         for field in item.ListFields():
#             item_dict[field[0].name] = field[1]
#         results.append(item_dict)
#     return results

# def save_results_to_sqlite(results):
#     """
#     결과를 SQLite에 저장하는 함수
#     """
#     # SQLite 연결 생성
#     conn = sqlite3.connect('predictions.db')
#     cursor = conn.cursor()

#     # 테이블 생성
#     cursor.execute('''CREATE TABLE IF NOT EXISTS predictions
#                       (id INTEGER PRIMARY KEY AUTOINCREMENT, prediction_json TEXT)''')

#     # 결과를 SQLite에 저장
#     for result in results:
#         prediction_json = json.dumps(result)  # JSON 형식으로 변환
#         cursor.execute("INSERT INTO predictions (prediction_json) VALUES (?)", (prediction_json,))
    
#     # 변경사항 저장 및 연결 종료
#     conn.commit()
#     conn.close()

# # 이미지 분석 실행
# # results = analyze_single_image(image_blob_name)

# # RepeatedComposite 객체를 딕셔너리로 변환
# for result in results:
#     if 'key' in result:
#         result['key'] = convert_repeated_composite_to_dict(result['key'])


# # 결과를 SQLite에 저장
# save_results_to_sqlite(results)

# # 결과 출력 (옵션)
# print("Predictions saved to SQLite database.")


###########################################app.py 수정 전
# import os
# import pathlib

# import requests
# from flask import Flask, session, abort, redirect, request, render_template
# from google.oauth2 import id_token
# from google_auth_oauthlib.flow import Flow
# from pip._vendor import cachecontrol
# import google.auth.transport.requests

# #############
# from flask_sqlalchemy import SQLAlchemy
# from flask import after_this_request

# ##############

# from werkzeug.utils import secure_filename
# import cv2
# from google.cloud import storage
# import datetime
# from google.cloud import aiplatform
# import time

# import base64

# ##############

# app = Flask("Google Login App")
# app.secret_key = "CodeSpecialist.com"


# ##############
# # SQLAlchemy 초기화
# app.config["SQLALCHEMY_DATABASE_URI"] = (
#     "sqlite:///login_info.db"  # SQLite 데이터베이스를 사용하도록 설정
# )
# db = SQLAlchemy(app)


# # 사용자 모델 정의
# class User(db.Model):
#     id = db.Column(db.String, primary_key=True)
#     name = db.Column(db.String)
#     email = db.Column(db.String)


# # 데이터베이스 생성 및 초기화
# with app.app_context():
#     db.create_all()
# ##############


# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# # 유출 조심 / client_secret.json 유출 금지
# GOOGLE_CLIENT_ID = (
#     "200475201819-kjn35ua9q131d6f7ohru6qpus0h6cbue.apps.googleusercontent.com"
# )
# client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

# flow = Flow.from_client_secrets_file(
#     client_secrets_file=client_secrets_file,
#     scopes=[
#         "https://www.googleapis.com/auth/userinfo.profile",
#         "https://www.googleapis.com/auth/userinfo.email",
#         "openid",
#     ],
#     redirect_uri="http://127.0.0.1:5000/callback",
# )


# def login_is_required(function):
#     def wrapper(*args, **kwargs):
#         if "google_id" not in session:
#             return abort(401)  # Authorization required
#         else:
#             return function()

#     return wrapper

# ###########################################
# # sj 서비스 계정 gcs 연동
# # 유출 금지!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="team05-project-c7a54e239686.json"

# ######################################################

# @app.route("/")
# def index():
#     return render_template("home.html")


# @app.route("/googlelogin")
# def google_login():
#     authorization_url, state = flow.authorization_url()
#     session["state"] = state
#     return redirect(authorization_url)

# ############################################

# @app.route("/study")
# def study():
#     return render_template("study.html")

# # ----------------------------------------
# # bucket 정보 (현 테스트 파일 !!!!!!!!!!!!!!!)
# bucket_name = "video_file_upload_test"

# # 임시 디렉토리 생성 (GCS에 업로드 후 바로 삭제됨)
# temp_dir = "temp"
# if not os.path.exists(temp_dir):
#     os.makedirs(temp_dir)
    
# # GCS에 업로드 함수
# def upload_to_gcs(blob_name, file_content):
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(blob_name)       #blob_name 은 업로드 할때 저장 이름

#     blob.upload_from_string(file_content)
    
    
# # 파일 gcs 전송
# @app.route("/study/uploader", methods=['POST'], endpoint = "uploader")
# def uploader_file():
#     if request.method == 'POST':
#         f = request.files['file']  # study.html에 form에서 받아온 파일 
        
#         timestamp = time.strftime("%Y_%m_%d_%H_%M", time.localtime())
        
#         blob_name = secure_filename(f.filename)     # filename 저장
#         id = session['name']
        
#         # 업로드된 파일을 일시적으로 로컬 디스크에 저장
#         local_file_path = os.path.join(temp_dir, blob_name)
#         f.save(local_file_path)
        
#         # 로컬 디스크에 저장된 파일을 OpenCV로 읽어와서 처리
#         video = cv2.VideoCapture(local_file_path)
#         if not video.isOpened():
#             return "Error: Could not open video file", 400
        
#         fps = video.get(cv2.CAP_PROP_FPS)
#         count = 0
#         time_count = 0
        
#         # 1초 단위로 영상을 자르고 Google Cloud Storage로 업로드
#         while(video.isOpened()):
#             ret, image = video.read()
#             if ret == False:
#                 break
                
#             if(int(video.get(1)) % fps == 0):
#                 local_img_path = "%s_%s_%d_img_%d.jpg" %(id, timestamp, time_count, count)
#                 cv2.imwrite(local_img_path, image)
#                 print('save', str(int(video.get(1))))
                
#                 upload_img_path = "%s_%s/%d/img_%d.jpg" %(id, timestamp, time_count, count)
#                 upload_to_gcs(upload_img_path, cv2.imencode('.jpg', image)[1].tobytes())
#                 # os.remove(local_img_path)
#                 count += 1
            
#                 if count % 60 == 0:
#                     time_count += 1
                
#         os.remove(local_file_path)
                
#         video.release()
#         return render_template("report.html")
    
# ##########################################

# @app.route("/report")
# def report():
#     return render_template("report.html")


# # @app.route("/logout")
# # def logout():
# #     session.clear()
# #     return redirect("/")


# # @app.route("/studycam")
# # def study_cam():
# #     return render_template("cam_page.html")


# @app.route("/contact")
# def contact():
#     return render_template("contact.html")


# @app.route("/callback")
# def callback():
#     flow.fetch_token(authorization_response=request.url)

#     if not session["state"] == request.args["state"]:
#         abort(500)  # State does not match!

#     credentials = flow.credentials
#     request_session = requests.session()
#     cached_session = cachecontrol.CacheControl(request_session)
#     token_request = google.auth.transport.requests.Request(session=cached_session)

#     id_info = id_token.verify_oauth2_token(
#         id_token=credentials._id_token, request=token_request, audience=GOOGLE_CLIENT_ID
#     )

#     session["google_id"] = id_info.get("sub")
#     session["name"] = id_info.get("name")

#     ###
#     # 데이터베이스에 사용자 정보 저장
#     existing_user = User.query.filter_by(id=id_info.get("sub")).first()

#     if not existing_user:
#         # 사용자가 데이터베이스에 없는 경우에만 추가
#         user = User(
#             id=id_info.get("sub"), name=id_info.get("name"), email=id_info.get("email")
#         )
#         db.session.add(user)
#         db.session.commit()
#     ###

#     return redirect("/google_protected_area")


# @app.route("/google_protected_area")
# @login_is_required
# def google_protected_area():
#     user = User.query.filter_by(id=session["google_id"]).first()
#     return render_template("logined_home.html", user=user)


# ##################
# @app.after_request
# def add_no_cache_header(response):
#     response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
#     response.headers["Pragma"] = "no-cache"
#     response.headers["Expires"] = "0"
#     return response


# ##################

# if __name__ == "__main__":
#     app.run(debug=True)
