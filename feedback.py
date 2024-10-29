import streamlit as st
import json
from datetime import datetime

FEEDBACK_FILE = "feedback_log.json"

def display_feedback_form(query, response):
    """Displays a feedback form after each bot response."""
    with st.expander("Rate this response"):
    #     rating = st.thumbs("Was this response helpful?", ["Yes", "No"])
    #     comments = st.text_area("Additional feedback (optional)")
        st.write("Was this response helpful ")

    # col1 , col2 = st.columns([1,1])

    # with col1:
    #     thumbs_up = st.button("👍" , key= "thumbs_up" , help= "Helpful response")
    # with col2:
    #     thumbs_down = st.button("👎" , key= "thumbs_down" , help= "Not helpful")

    # if thumbs_up or thumbs_down:
    #     sentiment = "Yes" if thumbs_up else "No"

        sentiment = [":material/thumb_down:" , ":material/thumb_up:" ]
        selected = st.feedback("thumbs")
        if selected is not None:
            st.markdown(f"You selected : {sentiment[selected]}")

        # Option comment box
        comments = st.text_area("Additional feedback (optional)" , key = "Comments")

        # Button for submitting feedback

        if st.button("Submit Feedback"):
            collect_feedback(query, response, sentiment, comments)
            st.success("Thank you for your feedback!")

def collect_feedback(query, response, rating, comments):
    """Saves feedback data to a JSON file."""
    feedback_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "response": response,
        "rating": rating,
        "comments": comments
    }

    # Append feedback to a JSON file
    try:
        with open(FEEDBACK_FILE, "r") as f:
            feedback_log = json.load(f)
    except FileNotFoundError:
        feedback_log = []

    feedback_log.append(feedback_entry)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback_log, f, indent=4) # indent mean save the each feedback in stack not in one line

