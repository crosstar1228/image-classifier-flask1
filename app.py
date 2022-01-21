from flask import Flask, render_template, request  #render_template은 template을 불러옴

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input  #VGG 모델에서 전처리
from keras.applications.vgg16 import decode_predictions 
from keras.applications.vgg16 import VGG16  #pretrained 모델 자체


app = Flask(__name__) #  인스턴스 생성

@app.route('/',methods = ['GET'])
def hello():
    return render_template('index.html') # Template 출력하는 기본 명령어

@app.route('/',methods = ['POST'])
def predict():
    ## 1. 이미지 파일 input으로 받아 저장
    imagefile = request.files['imagefile'] #html로부터 imagefile request 전달받음
    image_path = "./images/" + imagefile.filename # filename으로부터 path 부여하고
    imagefile.save(image_path) #파일 저장!

    ## 2. 전처리 및 모델 학습
    image = load_img(image_path, target_size=(224, 224)) #path에 있는 이미지 로딩
    image = img_to_array(image) # array로 변경
    image = image.reshape((1,image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)

    #모델 불러우기 및 예측
    model = VGG16()
    yhat = model.predict(image) # 예측 결과
    label = decode_predictions(yhat) 
    label = label[0][0]

    
    classification = '%s (%.2f%%)' %(label[1], label[2]*100)

    
    


    return render_template('index.html', prediction = classification) #결과 함께 출력



if __name__ == "__main__": #import 해서 실행하는 것이 아니라, 직접 로컬 환경에서 실행할 경우
    app.run(port= 3000, debug = True) # port 번호 3000으로 지정