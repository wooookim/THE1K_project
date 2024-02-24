import os
import pathlib

import requests
from flask import Flask, session, abort, redirect, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

#############
from flask_sqlalchemy import SQLAlchemy
from flask import after_this_request

##############

from werkzeug.utils import secure_filename
import cv2
from google.cloud import storage
import datetime

##############

app = Flask("Google Login App")
app.secret_key = "CodeSpecialist.com"


##############
# SQLAlchemy 초기화
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///login_info.db"  # SQLite 데이터베이스를 사용하도록 설정
)
db = SQLAlchemy(app)


# 사용자 모델 정의
class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)


# 데이터베이스 생성 및 초기화
with app.app_context():
    db.create_all()
##############


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# 유출 조심 / client_secret.json 유출 금지
GOOGLE_CLIENT_ID = (
    "200475201819-kjn35ua9q131d6f7ohru6qpus0h6cbue.apps.googleusercontent.com"
)
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_uri="http://127.0.0.1:5000/callback",
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


###########################################
# sj 서비스 계정 gcs 연동
# 유출 금지!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "team05-project-3ee2c0d1741b.json"

######################################################


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/googlelogin")
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


############################################


@app.route("/study")
def study():
    return render_template("study.html")


# ----------------------------------------
# bucket 정보 (현 테스트 파일 !!!!!!!!!!!!!!!)
bucket_name = "video_file_upload_test"

# 임시 디렉토리 생성 (GCS에 업로드 후 바로 삭제됨)
temp_dir = "temp"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)


# GCS에 업로드 함수
def upload_to_gcs(blob_name, file_content):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)  # blob_name 은 업로드 할때 저장 이름

    blob.upload_from_string(file_content)


# 파일 gcs 전송
@app.route("/study/uploader", methods=["POST"], endpoint="uploader")
def uploader_file():
    if request.method == "POST":
        f = request.files["file"]  # study.html에 form에서 받아온 파일
        current_date = datetime.datetime.now().strftime("%Y%m%d")

        blob_name = secure_filename(f.filename)  # filename 저장
        id = User.id
        # blob_directory = f"{id}/{current_date}/"
        id = session["name"]

        # 업로드된 파일을 일시적으로 로컬 디스크에 저장
        local_file_path = os.path.join(temp_dir, blob_name)
        f.save(local_file_path)

        # 로컬 디스크에 저장된 파일을 OpenCV로 읽어와서 처리
        video = cv2.VideoCapture(local_file_path)
        if not video.isOpened():
            return "Error: Could not open video file", 400

        fps = video.get(cv2.CAP_PROP_FPS)
        count = 0

        # 1초 단위로 영상을 자르고 Google Cloud Storage로 업로드
        while video.isOpened():
            ret, image = video.read()
            if ret == False:
                break
            if int(video.get(1)) % fps == 0:
                local_img_path = "%s_%s_%d.jpg" % (id, current_date, count)
                cv2.imwrite(local_img_path, image)
                print("save", str(int(video.get(1))))
                upload_to_gcs(local_img_path, cv2.imencode(".jpg", image)[1].tobytes())
                os.remove(local_img_path)
                count += 1

        os.remove(local_file_path)

        video.release()
        return "Upload successful", 200


##########################################


@app.route("/report")
def report():
    return render_template("report.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token, request=token_request, audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")

    ###
    # 데이터베이스에 사용자 정보 저장
    existing_user = User.query.filter_by(id=id_info.get("sub")).first()

    if not existing_user:
        # 사용자가 데이터베이스에 없는 경우에만 추가
        user = User(
            id=id_info.get("sub"), name=id_info.get("name"), email=id_info.get("email")
        )
        db.session.add(user)
        db.session.commit()
    ###

    return redirect("/google_protected_area")


@app.route("/google_protected_area")
@login_is_required
def google_protected_area():
    user = User.query.filter_by(id=session["google_id"]).first()
    return render_template("logined_home.html", user=user)


##################
@app.after_request
def add_no_cache_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


##################

if __name__ == "__main__":
    app.run(debug=True)
