import streamlit as st
import os
import tempfile
import traceback
from report_generator import generate_pdf_report, combine_pdfs
from utils import save_uploaded_file, extract_cv_text
from cv_processor import process_cv

# Add debug mode
DEBUG = st.secrets.get("DEBUG", False)

def local_css(file_name):
    """Load local CSS file"""
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}")

def main():
    st.set_page_config(page_title="KermitTech CV Analyzer", layout="wide")
    local_css(os.path.join("assets", "styles.css"))
    
    with st.sidebar:
        st.markdown('<img src="assets/kermittech-logo.png" class="logo">', unsafe_allow_html=True)
        job_category = st.selectbox("Select Job Category", ["Data Engineer", "Data Analyst", "AI Engineer", "UI/UX Developer"])
    
    st.header("CV Analysis Platform")
    uploaded_files = st.file_uploader("Upload Candidate CVs", type=["pdf", "docx"], accept_multiple_files=True)

    if uploaded_files:
        temp_dir = tempfile.mkdtemp()
        analysis_results = []
        errors = []

        for idx, file in enumerate(uploaded_files):
            try:
                with st.expander(f"Processing {file.name}", expanded=DEBUG):
                    # Save file
                    file_path = save_uploaded_file(file, temp_dir)
                    if DEBUG: st.write(f"Saved to: {file_path}")
                    print(file_path)
                    # Extract text

                    # Process CV
                    result = process_cv(file_path, job_category)
                    print("result", result)
                    if DEBUG: st.json(result)

                    # Generate report
                    pdf_path = generate_pdf_report(result, temp_dir)
                    analysis_results.append((result, pdf_path))
                    
            except Exception as e:
                base_name = os.path.basename(file_path) if file_path else file.name
                error_msg = f"{base_name[:30]}: {str(e)}"
                errors.append(error_msg)
                if DEBUG:
                    st.error(f"Processing Error: {error_msg}")
                    st.code(f"Error details: {traceback.format_exc()[-500:]}")
        if analysis_results:
            st.success(f"Processed {len(analysis_results)} CV(s) successfully!")
            # Display first result
            with st.container():
                st.subheader("Analysis Results")
                st.json(analysis_results[0][0])
                
        if errors:
            st.error(f"Failed to process {len(errors)} CV(s)")
            for error in errors:
                st.write(error)

if __name__ == "__main__":
    main()