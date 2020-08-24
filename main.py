
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
import numpy as np
import json
import pickle
import pandas as pd


#loading stuff here



app = Flask(__name__)

with open ("cosine_similarity_model", "rb") as f:
    cosine_sim= pickle.load(f)

with open ("smd_dataset", "rb") as f:
    smd= pickle.load(f)

@app.route('/test-api', methods=['GET'])
def home():
    return "<h1>Content Filtering API working</h1><p>this is content filtering API for our application</p>"




@app.route('/content-prediction', methods=['POST'])
def index():
        def get_recommendations(title):
            idx = indices[title]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:31]
            movie_indices = [i[0] for i in sim_scores]
            return titles.iloc[movie_indices]

        def get_recommendations_with_id(id):
            idx = indices_id[id]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:31]
            movie_indices = [i[0] for i in sim_scores]
            return ids.iloc[movie_indices]

        titles = smd['title']
        indices = pd.Series(smd.index, index=smd['title'])

        ids = smd['id']
        indices_id = pd.Series(smd.index, index=smd['id'])

        #getting the userId from front-end
        message = request.get_json(force=True)
        py_testuser = json.loads(message['user']) #makes a python variable of type string
        int_testuser = int(py_testuser) #converts string into int

        #making predictions

        movie_list = get_recommendations_with_id(int_testuser).head(20) #this is pandas 1d array

        json_movie_list =movie_list.tolist() #this is python list
        total = len(json_movie_list)

        response = {
            'total' : total,
            'movieId' : json_movie_list
        }
        return jsonify(response)


if __name__ == '__main__':
    app.run(debug = True )
