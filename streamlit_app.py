import requests
import streamlit as st

st.title(
    "Research Writer Agent"
)

topic = st.text_input(
    "Enter Topic"
)

if st.button(
    "Generate"
):
    try:
        response = requests.post(
            "http://localhost:8000/generate",
            params={
                "topic": topic
            }
        )

        if response.status_code == 200:
            data = response.json()
            result = data.get("result", data)  # Handle both nested and flat responses
            
            st.subheader(
                "Final Article"
            )

            st.write(
                result.get("edited", result.get("article", "No article generated"))
            )

            st.subheader(
                "Evaluation"
            )

            st.json(
                result.get("evaluation", {})
            )
            
            # Show additional info
            with st.expander("View Full Response"):
                st.json(data)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Connection error: {str(e)}\n\nMake sure the API server is running on http://localhost:8000")