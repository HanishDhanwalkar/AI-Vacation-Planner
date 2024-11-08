# frontend/app.py
import streamlit as st
import requests

st.title("One-Day Tour Planner")

city = st.text_input("Enter the city you want to visit:")
start_time = st.text_input("Enter your start time:")
end_time = st.text_input("Enter your end time:")
budget = st.number_input("Enter your budget:", min_value=0)
interests = st.multiselect("Select your interests:", ["Culture", "Adventure", "Food", "Shopping"])

if st.button("Generate Itinerary"):
    # Collect user preferences
    response = requests.post("http://localhost:8000/collect_preferences/", json={
        "city": city,
        "start_time": start_time,
        "end_time": end_time,
        "budget": budget,
        "interests": interests
    })
    if response.status_code == 200:
        st.success("Preferences saved successfully!")

    # Generate initial itinerary
    itinerary_response = requests.post("http://localhost:8000/generate_itinerary/")
    itinerary = itinerary_response.json().get("itinerary", [])
    st.write("Generated Itinerary:")
    for item in itinerary:
        st.write(f"{item['time']}: {item['name']}")
