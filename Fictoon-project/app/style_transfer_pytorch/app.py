import json
from flask import Flask, request
from flask import render_template, make_response
import tasks
import os
from PIL import Image
from datetime import datetime
from test import test_numbering
APP = Flask(__name__)
APP.config['UPLOAD_FOLDER'] = 'static/worker-img'

@APP.route('/',methods = ['GET','POST'])
def index():
    '''
    Render Home Template and Post request to Upload the image to Celery task.
    '''
    if request.method == 'GET': # get 오면 index.html
        return render_template("index.html")
    if request.method == 'POST':# post 오면 return download.html
        img = request.files['image'] # 이미지 요청 받음
        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")

        # 가공할 이미지 저장
        img.save(os.path.join(APP.config['UPLOAD_FOLDER'],img.filename))
        # OUTPUT 사진 저장 위치
        loc = "static/worker-img/"+img.filename
        # delay = CELERY.task() 에 output 사진 과 함께
        job = tasks.image_demension.delay(loc)

        JOB = test_numbering.delay()

        return render_template("download.html",JOBID=job.id)


@APP.route('/progress')
def progress():
    '''
    Get the progress of our task and return it using a JSON object
    '''
    jobid = request.values.get('jobid')
    if jobid:
        job = tasks.get_job(jobid)
        if job.state == 'PROGRESS':
            return json.dumps(dict(
                state=job.state,
                progress=job.result['current'],
            ))
        elif job.state == 'SUCCESS':
            return json.dumps(dict(
                state=job.state,
                progress=1.0,
            ))
    return '{}'

@APP.route('/result.png')
def result():
    '''
    Pull our generated .png binary from redis and return it
    '''
    jobid = request.values.get('jobid')
    if jobid:
        job = tasks.get_job(jobid)
        png_output = job.get()
        png_output="../"+png_output
        return png_output
    else:
        return 404




if __name__ == '__main__':
    APP.run(host='0.0.0.0')
