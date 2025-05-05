import streamlit as st
import os
import tempfile
import traceback
from report_generator import generate_pdf_report, combine_pdfs, generate_pdf_report_with_audio
from utils import save_uploaded_file, extract_cv_text
from cv_processor import process_cv
from audio_processor import AudioProcessor
from utils.visualization import create_radar_chart
import ssl
import whisper

import asyncio
import sys
os.environ['STREAMLIT_SERVER_ENABLE_STATIC_FILE_WATCHER'] = 'false'

# Disable Torch class inspection
import torch
torch._C._disable_class_wrapper = True

if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Disable Streamlit's problematic file watcher
import streamlit as st
st.runtime.instances = []


@st.cache_resource
def load_processor():
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        return AudioProcessor(model_size="base")  # or "tiny" for less powerful machines
    except Exception as e:
        st.error(f"Failed to initialize audio processor: {str(e)}")
        return None

def display_results(cv_analysis, audio_analysis=None, combined_analysis=None):
    """Display analysis results in Streamlit UI"""
    if audio_analysis:
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["CV Analysis", "Audio Analysis", "Combined"])
        
        with tab1:
            display_cv_results(cv_analysis)
            
        with tab2:
            display_audio_results(audio_analysis)
            
        with tab3:
            display_combined_results(cv_analysis, audio_analysis)
    else:
        display_cv_results(cv_analysis)

def display_cv_results(analysis):
    """Display CV analysis results"""
    st.subheader("CV Analysis Report")
    st.write(f"**Candidate:** {analysis['name']}")
    
    # Education
    with st.expander("Education"):
        st.write(f"**Degree:** {analysis['education']['degree']}")
        st.write(f"**University:** {analysis['education']['university']}")
    
    # Skills Radar Chart
    st.subheader("Skills Analysis")
    fig = create_radar_chart(analysis['analysis'])
    st.plotly_chart(fig, use_container_width=True)
    
    # Interview Questions
    st.subheader("Suggested Interview Questions")
    for i, question in enumerate(analysis['interview_questions'], 1):
        st.write(f"{i}. {question}")

def display_audio_results(analysis):
    """Display audio analysis results"""
    st.subheader("Interview Audio Analysis")
    
    # Audio metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Communication Score", f"{analysis['communication_score']}/5")
        st.metric("Technical Depth", f"{analysis['technical_depth']}/5")
    
    with col2:
        st.metric("Confidence Level", f"{analysis['confidence']}/5")
        st.metric("Keyword Usage", f"{analysis['keyword_usage']}/5")
    
    # Red flags
    if analysis['red_flags']:
        st.warning("**Potential Concerns:**")
        for flag in analysis['red_flags']:
            st.write(f"- {flag}")

def display_combined_results(cv_analysis, audio_analysis):
    """Display combined analysis"""
    combined_score = (cv_analysis['analysis']['technical_experience'] * 0.6 + 
                     audio_analysis['technical_depth'] * 0.4)
    
    st.subheader("Combined Evaluation")
    st.metric("Overall Score", f"{combined_score:.1f}/5.0")
    
    # Progress bar
    st.progress(combined_score/5)
    
    # Recommendations
    if combined_score >= 4:
        st.success("**Strong Candidate** - Recommended for next round")
    elif combined_score >= 3:
        st.info("**Potential Candidate** - Worth considering")
    else:
        st.warning("**Needs Improvement** - May not be suitable")


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
        st.image(
            "assets/kermittech-logo.png",
            use_container_width=True,  # Modern parameter
            output_format="PNG"
        )
        job_category = st.selectbox("Select Job Category", ["Data Engineer", "Data Analyst", "AI Engineer", "UI/UX Developer"])
        audio_enabled = st.checkbox("Include Interview Audio Analysis")
    
    st.header("CV Analysis Platform")
    uploaded_files = st.file_uploader("Upload Candidate CVs", type=["pdf", "docx"], accept_multiple_files=True)

    if audio_enabled:
        audio_file = st.file_uploader("Upload Interview Audio", type=["wav", "mp3"])
    else:
        audio_file = None

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

                    if audio_enabled:
                        print("Audio analysis enabled")
                    else:
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


        if audio_file:
            try:
                processor = AudioProcessor("base")  # or "small", "tiny"
                
                with st.spinner("Processing audio (this may take a few minutes)..."):
                    transcript = processor.process_audio(audio_file, job_category)
                    
                    if transcript:
                        st.success("Audio transcription successful!")
                        st.text_area("Transcript", transcript, height=200)
                        pdf_path = generate_pdf_report_with_audio(result, transcript, temp_dir)
                        analysis_results.append((result, pdf_path))
                        # Continue with your analysis...
                    else:
                        st.error("Failed to transcribe audio - please check the file format")
                        
            except Exception as e:
                st.error(f"Audio processing error: {str(e)}")
                st.info("Supported formats: MP3, WAV, M4A, FLAC")
                
        #display_results(result, audio_analysis, combined_analysis)


        if analysis_results:
            success_message = """
            <div style='color:#292929; padding:1rem; border-left:4px solid #FF6B35; background-color:rgba(255,107,53,0.15)'>
                <strong>✓ CV processed successfully!</strong>
            </div>
            """
            st.markdown(success_message, unsafe_allow_html=True)
            
            # Show download button for first report
            with open(analysis_results[0][1], "rb") as f:
                st.download_button(
                    label="Download PDF Report",
                    data=f,
                    file_name=f"{analysis_results[0][0]['name']}_report.pdf",
                    mime="application/pdf"
                )
            
            # For multiple files
            if len(analysis_results) > 1:
                combined_pdf = combine_pdfs([res[1] for res in analysis_results])
                st.download_button(
                    label="Download All Reports",
                    data=combined_pdf,
                    file_name="combined_reports.pdf",
                    mime="application/pdf"
                )    

        if errors:
            st.error(f"Failed to process {len(errors)} CV(s)")
            for error in errors:
                st.write(error)

if __name__ == "__main__":
    main()