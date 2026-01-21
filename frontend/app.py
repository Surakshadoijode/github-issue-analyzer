import streamlit as st
import requests

st.set_page_config(page_title="GitHub Issue Analyzer", layout="centered")

st.title("GitHub Issue Analyzer")
st.write("Analyze and prioritize GitHub issues using AI")

repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/facebook/react")
issue_number = st.number_input("Issue Number", min_value=1, step=1)

if st.button("Analyze Issue"):
    if not repo_url:
        st.error("Please enter a repository URL")
    else:
        with st.spinner("Analyzing issue..."):
            res = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={"repo_url": repo_url, "issue_number": issue_number}
            )

            if res.status_code == 200:
                data = res.json()

                st.success("Analysis complete")

                st.subheader("Summary")
                st.write(data["summary"])

                st.subheader("Type")
                st.write(data["type"])

                st.subheader("Priority")
                st.write(data["priority_score"])

                st.subheader("Suggested Labels")
                st.write(", ".join(data["suggested_labels"]))

                st.subheader("Potential Impact")
                st.write(data["potential_impact"])

                st.subheader("Raw JSON")
                st.json(data)
            else:
                st.error(res.json().get("detail", "Something went wrong"))
