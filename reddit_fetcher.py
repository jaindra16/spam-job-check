import praw
from dotenv import load_dotenv
import os 
load_dotenv()

def fetch_reddit_posts(company_name, limit=20):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )
    job_subreddits = [
        "jobs",
        "cscareerquestions",
        "recruitinghell",
        "workreform",
        "jobsearch",
        "career_guidance",
        "askHR",
    ]
    posts = []
    for subreddit_name in job_subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        for post in subreddit.search(company_name, limit=limit):
            posts.append({
            "title": post.title,
            "content": post.selftext,
            "subreddit": post.subreddit.display_name,
            "url": post.url,
            "date": post.created_utc
        })
    return posts
