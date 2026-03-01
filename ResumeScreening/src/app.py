import os
import streamlit as st

# Create Resumes directory if it doesn't exist
RESUMES_DIR = "Resumes"
if not os.path.exists(RESUMES_DIR):
    os.makedirs(RESUMES_DIR)

# Import functions from resume_processor file
from gopi_resume_processor import load_resumes, analyze_resume, store_in_chromadb, run_self_query, extract_candidate_details

# ===============Streamlit UI Setup=================
st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")
st.title("AI Resume Screener")
st.markdown("Upload resumes and analyze it using AI. Then run smart searchings over previously analyzed resumes.")

job_description = st.text_area("Enter Job Description")
uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])



if st.button("Analyze & Store Resume") and uploaded_file and job_description:
    # Save uploaded file to Resumes directory
    file_path = os.path.join(RESUMES_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner("Aanalyzing & Storing Resume..."):
        docs = load_resumes([file_path]) # Parse resume using loader for RAG usage
        report = analyze_resume(docs, job_description) # Analyze resume
        chromadb, candidate_details = store_in_chromadb(docs) # Store in vector database
        st.success("Resume analyzed and stored successfully!")

        # Display candidate details
        st.subheader("Candidate Details")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Name", candidate_details['name'])
        with col2:
            st.metric("Email", candidate_details['email'])
        with col3:
            st.metric("Location", candidate_details['location'])

        st.subheader("Analysis Report")
        st.write(report)
        st.download_button("Download Report", report, file_name="analysis_report.txt")

st.divider()

st.subheader("Ask Questions about Resumes")
query = st.text_input("Type your smart query here (e.g., 'Python developer with AWS experience')")

if st.button("Search Resume Query") and query:
    with st.spinner("Running smart query..."):
        results = run_self_query(query)

        if results:
            for i, res in enumerate(results, 1):
                st.markdown(f"**Result {i}**")
                # Display candidate details from metadata
                metadata = res.metadata
                st.markdown(f"**Name:** {metadata.get('name', 'Unknown')}")
                st.markdown(f"**Email:** {metadata.get('email', 'Unknown')}")
                st.markdown(f"**Location:** {metadata.get('location', 'Unknown')}")
                st.markdown(f"**Chunk:** {metadata.get('chunk_index', 0) + 1}/{metadata.get('total_chunks', 1)}")
                st.markdown("---")
                st.write(res.page_content.strip())
        else:
            st.warning("No results found for your query.")


