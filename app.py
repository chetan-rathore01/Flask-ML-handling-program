from flask import Flask
from flask import request, jsonify
import pandas as pd
import pickle
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def get_cleaned_data(form_data):
  gestation = int(form_data['gestation'])
  parity = int(form_data['parity'])
  age = int(form_data['age'])
  height = int(form_data['height'])
  weight = int(form_data['weight'])
  smoke = int(form_data['smoke'])

  # Simple prediction formula based on typical birth weight factors
  base_weight = 2.5  # Base weight in kg
  gestation_factor = (gestation - 37) * 0.15  # Each week adds ~150g
  weight_factor = (weight - 60) * 0.01  # Mother's weight influence
  height_factor = (height - 160) * 0.005  # Mother's height influence
  smoke_penalty = -0.2 if smoke == 1 else 0  # Smoking reduces birth weight
  
  prediction = base_weight + gestation_factor + weight_factor + height_factor + smoke_penalty
  prediction = max(1.5, min(5.0, prediction))  # Keep within realistic range
  
  return round(prediction, 2)

@app.route("/home", methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def get_prediction():
    # get data from user 
    baby_data_form = request.form
    prediction = get_cleaned_data(baby_data_form)

    return render_template("index.html", prediction=prediction)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002,debug=True)

    
