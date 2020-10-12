from flask import render_template, request, redirect, flash ,jsonify
from flask import url_for
from flask import Flask

from werkzeug.utils import secure_filename
import os
from keras.models import load_model

UPLOAD_FOLDER = './Images'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except:
        return "Cannot Identify"
@app.route('/getClassification', methods=['GET', 'POST'])
def getClassification():
        try:
            print('Called API')
            print(request.method)
            print('request.files')
            print(request.files)
            response = jsonify({'label': 'label'})
            print(response)
    
            if request.method == 'POST':
                if 'inputImage' not in request.files:
                    flash('No file part')
                    return "File Not Available"
                file = request.files['inputImage']
                if file.filename == '':
                    flash('No file selected for uploading')
                    return "File Name Not Found"
                if file:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                    #getPrediction(filename)
                    #label, acc = getPrediction(filename)
                    results={
                       0:'aeroplane',
                       1:'automobile',
                       2:'bird',
                       3:'cat',
                       4:'deer',
                       5:'dog',
                       6:'frog',
                       7:'horse',
                       8:'ship',
                       9:'truck'
                    }
                    print('importing model')
                    model = load_model('./Model/model1_cifar_10epoch.h5')    
                    print('importing model done')
    
                    from PIL import Image
                    import numpy as np
                    im=Image.open('./Images/'+filename)
                    # the input image is required to be in the shape of dataset, i.e (32,32,3)
                     
                    im=im.resize((32,32))
                    im=np.expand_dims(im,axis=0)
                    im=np.array(im)
                    pred=model.predict_classes([im])[0]
                    print(pred,results[pred])
                    label, acc =  results[pred], "pred*100"
                    
                    flash(label)
                    flash(acc)
                    flash(filename)
                    print('request.files')
    
                    response = jsonify({'label': label})
                    print('request.files')
    
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    print(response)
    
                    return response
                    #return redirect('/')
                    #return label
        except:
            return "Cannot Identify"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8081, debug=True)