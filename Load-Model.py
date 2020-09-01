import pickle
import pandas as pd
import requests
import emoji

with open ("cosine_similarity_model", "rb") as f:
    cosine_sim= pickle.load(f)

with open ("smd_dataset", "rb") as f:
    smd= pickle.load(f)


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


indices_id_list = indices_id.tolist()



#if model not trained on data, use Tmdb API to show results

movie_id= 374720
api_key = "0cc56911115acd5222ff0c526ef328f3"
language = "en-US"
page = 1
if movie_id  not in indices_id_list:
    print("not present, run tmdb api")
    URL = f'https://api.themoviedb.org/3/movie/{movie_id}/similar'

    PARAMS = {'api_key': api_key, 'language': language, 'page': page}

    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)

    data =r.json()
    movie_list = []
    for movie in data['results']:
        movie_list.append(int(movie['id']))

    api_rec = movie_list[:20]
    print(api_rec)

else:
    print("present, run normal api")
    model_rec= get_recommendations_with_id(movie_id).head(20)
    model_rec_list = model_rec.tolist()
    print(model_rec_list)

#print(type(get_recommendations("Good Will Hunting").head(20)))


#take input to show recommendations, makes it easier to test but serves no purpose other than that.

movie_name = None


while movie_name != 'quit':
    movie_name = input("Enter a movie name to show get similar movies: \n").title()
    try:
        recommendations = get_recommendations(movie_name).head(20)
        print(recommendations)

    except:
        print(emoji.emojize("\n:upside-down_face:"))
        print("----Oops! our model is not trained on this movie, try a different movie----")
