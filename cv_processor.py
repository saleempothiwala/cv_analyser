# cv_processor.py
import json
import logging
import requests
from typing import Dict, Any
from utils.file_handlers import extract_cv_text
from analysis_prompt import ANALYSIS_PROMPT
from json import JSONDecodeError

logger = logging.getLogger(__name__)

def analyze_with_granite(cv_text: str, prompt_template: str, job_category: str) -> Dict[str, Any]:
    """Handle Ollama's nested JSON response format"""
    print("Analyzing CV with Granite model...")
    print("cv_text_analyze_with_granite", cv_text[:100])
    print("job_category_analyze_with_granite", job_category)
    print("prompt_template_analyze_with_granite", prompt_template[:100])
    # Ensure the prompt template is formatted correctly
    try:
        full_prompt = ANALYSIS_PROMPT.format(job_category=job_category)
        full_prompt += f"\n\nCV Text:\n{cv_text[:3000]}"
        print("full_prompt_analyze_with_granite", full_prompt[:100])
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "granite3.3",  # Match exact model name
                "prompt": full_prompt,
                "format": "json",
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        print("Raw API Response:", response.text)
        
        # Extract and clean JSON string
        raw_data = response.json()
        json_str = raw_data.get("response", "{}")
        
        # Fix common formatting issues
        json_str = json_str.strip()
        json_str = json_str.replace("\\n", "").replace("\\t", "")
        
        # Handle nested JSON encoding
        try:
            result = json.loads(json_str)
        except JSONDecodeError:
            # Remove extra backslashes
            json_str = json_str.encode().decode('unicode_escape')
            result = json.loads(json_str)
        
        print("Parsed Result:", result)
        return result
        
    except JSONDecodeError as e:
        logger.error(f"JSON Decode Failed. Cleaned String: {json_str}")
        raise ValueError("Invalid JSON format from model") from e


def validate_analysis_format(result: Dict) -> bool:
    """Validate the structure of analysis results"""
    required_keys = {
        'name', 'education', 'experience', 'analysis',
        'summary', 'interview_questions'
    }
    analysis_subkeys = {
        'technical_experience', 'project_relevance',
        'extra_curricular', 'business_acumen',
        'communication', 'leadership',
        'innovative', 'cultural_fit'
    }
    
    return all(
        key in result for key in required_keys
    ) and all(
        key in result['analysis'] for key in analysis_subkeys
    )

def process_cv(file_path: str, job_category: str) -> Dict[str, Any]:
    """Main CV processing pipeline"""
    print("Processing CV:")
    try:
        # 1. Extract text
        cv_text = extract_cv_text(file_path)
        print("cv_text_process_cv", cv_text[:100])
        # 2. Analyze with AI model
        analysis = analyze_with_granite(cv_text, ANALYSIS_PROMPT, job_category)
        print("analysis done")
        # 3. Calculate average score
        scores = [v for v in analysis['analysis'].values() if isinstance(v, (int, float))]
        analysis['average_score'] = round(sum(scores)/len(scores), 2)
        
        # 4. Add raw text reference
        analysis['cv_text'] = cv_text[:100] + "..."  # Store excerpt
        
        return analysis
        
    except Exception as e:
        logger.error(f"CV processing failed: {str(e)}")
        raise

def mock_process_cv(file_path: str, job_category: str) -> Dict[str, Any]:
    """Mock processor for debugging"""
    return {
        "name": "John Doe",
        "education": {
            "degree": "MS Computer Science",
            "university": "Oslo University"
        },
        "experience": {
            "last_title": "Senior Data Engineer",
            "ats_score": 85
        },
        "analysis": {
            "technical_experience": 4.5,
            "project_relevance": 4.2,
            "extra_curricular": 3.8,
            "business_acumen": 4.0,
            "communication": 4.1,
            "leadership": 3.9,
            "innovative": 4.3,
            "cultural_fit": 4.4
        },
        "average_score": 4.15,
        "summary": "Experienced data professional with 5+ years in cloud-based ETL pipelines...",
        "interview_questions": [
            "Describe a time you improved data pipeline efficiency?",
            "How would you handle conflicting requirements from stakeholders?"
        ],

    }