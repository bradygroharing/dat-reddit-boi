from pprint import pprint
import numpy
import praw as praw
from praw.models import MoreComments
import requests
import json
import os
import sys
import sched, time

#gets shit from other classes when Test.py exists outside of src
sys.path.append(os.path.join(sys.path[0], 'src'))

# This is equal to 15 minutes
SCHEDULE_TIME = 60.0 * 15.0
SELECTED_SUBREDDITS = ['funny', 'pics', 'gaming', 'aww', 'mildlyinteresting']
SINGLE_SUBREDDIT = ['pubattlegrounds']
NUM_OF_POSTS_TO_GRAB = 2
#example of importing a method from database
# from src import database
from src import Comment

reddit = praw.Reddit(client_id='El479iqdfj-v0g',
                     client_secret='_2lWTM5i_USFV4Aynn_k_p-ySOo',
                     password='TeamHandsome',
                     user_agent='testscript by /u/EverestAtlas',
                     username='EverestAtlas')

# print(reddit.user.me())

submissionsCount = 0
topCommentCount = 0
secondCommentCount = 0
thirdCommentCount = 0

starttime = time.time()
def grabInformation(incomingSubreddit):
    # file = open(str(round(time.time())) + ".txt", "w")

    subredditSubmissions = []
    # This section grabs info from the subreddit /r/funny and displays info about it
    print("{")
    print('"Reddit_Object":[')
    print("{")
    print('"subreddit": {')
    print('"name": "/r/' + incomingSubreddit +'",')
    print('"all_posts": {')
    selectedReddit = reddit.subreddit(incomingSubreddit)
    for submission in selectedReddit.hot(limit=NUM_OF_POSTS_TO_GRAB):

        print('"post": {')
        print('"title":"' + str(submission.title) + '",')
        print('"author":"' + str(submission.author) + '",')
        print('"score":"' + str(submission.score) + '",')
        print('"id":"' + str(submission.id) + '",')
        print('"url":"' + str(submission.url) + '",')
        # subredditSubmissions.append(submission)
        submission.comments.replace_more(limit=0)
        print('"comments": {')
        for top_level_comment in submission.comments:
            newComment = Comment.TopLevelComment(top_level_comment)
            # print("{")
            print('"author":"' + str(top_level_comment.author) +'",')
            for second_level_comment in top_level_comment.replies:
                if (second_level_comment.score > 0):
                    newComment.commentChildren.append(second_level_comment)
                    #     for third_level_comment in second_level_comment.replies:
                    #         print("THIRD: " + third_level_comment.body)
        print("}}")
    print("}}}]}")



while True:
    for sub in SINGLE_SUBREDDIT:
        grabInformation(sub)
    time.sleep(SCHEDULE_TIME -((time.time() - starttime) % SCHEDULE_TIME))
