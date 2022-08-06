from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# open model
def open_model(model_path):
    """
    helper function for loading model
    """
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

model_iris = open_model("pipe_iris.pkl") # numpy array
model_titanic = open_model("pipe_titanic.pkl") # pandas dataframe

# Fungsi untuk inference iris
def inference_iris(data, model):
    """
    input : list with lenght : 6 --> [1, 2, 3, 4]
    output : predicted class (idx, label)
    """
    LABEL = ["Setosa", "Versicolor", "Virginica"]
    res = model.predict([data])
    return res[0], LABEL[res[0]]

# Fungsi untuk inference iris
def inference_titanic(data, model):
    """
    input : list with lenght : 6 --> [1, male/female, 2, 3, 4, 5]
    output : predicted class (idx, label)
    """
    LABEL = ["Not Survived", "Survived"]
    columns = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare']
    data = pd.DataFrame([data], columns=columns)
    res = model.predict(data)
    return res[0], LABEL[res[0]]
    

# halaman home
@app.route("/")
def homepage():
    return "<h1> Deployment Model Backend!</h1>"


@app.route("/iris_prediction", methods=['POST'])
def iris_predict():
    """
    content = 
    {
        'sl': xx,
        'sw': yy,
        'pl': xy,
        'pw': yy,        
    }
    """
    content = request.json
    newdata = [content['sl'], content['sw'], content['pl'], content['pw']]
    res_idx, res_label = inference_iris(newdata, model_iris)
    result = {
        'label_idx' : str(res_idx),
        'label_name' : res_label
    }
    response = jsonify(success=True,result=result)
    return response, 200
    
    
@app.route("/titanic_prediction", methods=['POST'])
def titanic_predict():
    """
      content = 
    {
        'passenger_class': xx,
        'age': yy,
        'sibling_spouse': xy,
        'parent_children': yy,
        'fare': yy,
        'gender': male/female        
    }
    """
    content = request.json
    # columns = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare']
    newdata = [content['passenger_class'], 
               content['gender'],
               content['age'],
               content['sibling_spouse'],
               content['parent_children'],
               content['fare']]
    res_idx, res_label = inference_titanic(newdata, model_titanic)
    result = {
        'label_idx' : str(res_idx),
        'label_name' : res_label
    }
    response = jsonify(success=True, result=result)
    return response, 200
    
# run app di local
# Jika deploy heroku komen baris dibawah
app.run(debug=True) 