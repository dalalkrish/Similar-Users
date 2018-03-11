# Similar-Users

Similar-Users is an API implementation that identifies similar users based on the cosine distance between them. Cosine distance is calculated using users interests and online activity. User behavior attributes used to calculate cosine distance between them are:

  - Course tags viewed by the user
  - Course difficulty levels
  - User interest
  - User course assessment tag if the user was enrolled before
  - Average user view time of the course based on the course tags
  - Average user assessment score if the user was enrolled before

Refer `conceptualize.ipynb` for the details on implementation.

### Details on how to set up this project

  - Use `Anaconda3` for `Python` and `Python Package` management.

  - Clone this project from https://github.com/dalalkrish/Similar-Users.git using `git clone https://github.com/dalalkrish/Similar-Users.git` and then `cd Similar-Users` into it.

  - Create a virtual environment using following command. Follow the instruction on the screen for activating and deactivating the    virtual environment.

    `conda create -n <environment-name> python=3.6`

  - Install necessary packages listed in `requirements.txt` using following command:

    `pip install -r requirements.txt`

  - Run server script using `python server.py` and the API should be listening at your host='0.0.0.0' and port=5002.

To get the API response make a GET request to `http://0.0.0.0:5002/users/<user-handle>` using a browser or Postman from Google Chrome web store. To send GET request from python script use Python's `request` module and convert the response to pandas data frame. `curl` from the terminal as `curl http://0.0.0.0:5002/users/50`.

API response object will be as follows:

```{

"similar-users-for":user_handle, "result": [

{"user_handle":[list of similar user's user handle],

"course_tags":[list of course tags of the user handle],

"level": [list of course difficulty levels],

"interest_tag":[list of interest tags of the user handle],

"assessment_tag": [list of course assessment tag if known for the user or "Not Available"],

 "mean_view_time":[list of user's average course view time],

 "mean_assessment_score":[list of user's average assessment score if assessment tag know or 0],

 "similarity-distance":[list of the similarity distance between the user requested in the API call and other users]}

 ]}
