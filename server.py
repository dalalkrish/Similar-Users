from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from database_connector import *
from json import dumps
from sklearn.preprocessing import scale, MinMaxScaler
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
api = Api(app)

def similarity_matrix(df, user):
    """
    This function calculates similarity matrix by calculating cosine distance between users.
    :Params:
        - df: Data Frame with vector.
        - user: User Handle. The key value that identifies each user.
    """
    df_transformed = pd.get_dummies(df, columns=["course_tags","level","interest_tag","assessment_tag"]).groupby(['user_handle','mean_view_time','mean_assessment_score'], as_index=False).sum()
    scaler = MinMaxScaler()
    for i in df_transformed.columns.values.tolist()[1:]:
        df_transformed[i] = scaler.fit_transform(df_transformed[i])
    x = df_transformed.iloc[:,1:].values
    idx2user = dict(zip(df_transformed.index, df_transformed["user_handle"]))
    user2idx = {v:k for k,v in idx2user.items()}
    similarities = cosine_similarity(x)
    similar_users_dist = similarities[user2idx.get(user)]
    similar_users_idx = np.where(similar_users_dist > 0.5)[0].tolist()
    similar_users = [idx2user.get(i) for i in similar_users_idx]
    dist = similar_users_dist[similar_users_idx]
    return similar_users, dist


class Users(Resource):
    def get(self, user_id):
        try:
            print("Request receieved for user handle %s" %(user_id))
            ax = DatabaseWorker('users.db')
            data = ax.query_table('user_activity')
            similar_users, distance = similarity_matrix(data, int(user_id))
            print("Matrix calculation completed")
            data = data[data["user_handle"].isin(similar_users)]
            m = dict(zip(similar_users, distance))
            data["similarity_distance"] = data["user_handle"].map(lambda x: m.get(x, "Not Available"))
            response = {"similar-users-for":user_id, "result": [data.to_dict('list')]}
            print("Done!")
            return jsonify(response)
        except Exception as e:
            return jsonify({'error-msg':'Please try another user handle'})

api.add_resource(Users, '/users/<user_id>')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
