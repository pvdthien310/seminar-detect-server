from flask import Flask,  request
from flask_cors import CORS
from model import detect
from model import detect1

app = Flask('__name__')
CORS(app)

# Detect
@app.route('/detectData', methods = ['POST'])
def data_analysis():
    print(request)
    image = request.form['image'].replace('data:image/png;base64,','')
    return detect.Detect(image)

# Detect v2
@app.route('/detectData1', methods = ['POST'])
def data_analysis1():
    print(request)
    image = request.form['image'].replace('data:image/png;base64,','')
    return detect1.Detect(image)

    
if __name__ == '__main__':
    app.run(debug = True)
