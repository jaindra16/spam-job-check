import streamlit as st
from reddit_fetcher import fetch_reddit_posts
from sentiment_analysis import analyze_sentiments
from faiss_manager import retrieve_from_faiss, save_to_faiss

st.title("Company Reputation Checker")
st.sidebar.title("Options")

# Search bar for company name
company_name = st.text_input("Enter a company name to search:")

# Dropdown for state-based filtering
filter_by_state = st.sidebar.checkbox("Filter by State")
state_name = st.sidebar.text_input("Enter state name:") if filter_by_state else None

if company_name:
    st.write(f"Fetching recent reviews for '{company_name}'...")
    posts = fetch_reddit_posts(company_name)
    
    if posts:
        # Sentiment Analysis
        sentiments = analyze_sentiments([post['content'] for post in posts])
        for i, post in enumerate(posts):
            post['sentiment'] = sentiments[i]
        
        # Save results to FAISS
        save_to_faiss(posts, company_name)
        
        # Display results
        st.write(f"### Recent Reviews for '{company_name}'")
        for post in posts[:10]:
            st.write(f"**Subreddit:** {post['subreddit']} | **Sentiment:** {post['sentiment']}")
            st.write(post['content'])
            st.write("---")
        
        # Overall sentiment
        sentiment_scores = [1 if s == "Legit" else -1 if s == "Scam" else 0 for s in sentiments]
        overall_sentiment = "Positive" if sum(sentiment_scores) > 0 else "Negative"
        st.write(f"### Overall Sentiment: {overall_sentiment}")
    else:
        st.write("No results found.")

if filter_by_state and state_name:
    st.write(f"Finding top 5 scam companies in {state_name}...")
    bad_companies = retrieve_from_faiss(state_name, sentiment="Scam", top_n=5)
    st.write("### Top 5 Scam Companies")
    for company in bad_companies:
        st.write(company)
