# analysis_prompts.py
ANALYSIS_PROMPT = """Generate VALID JSON analysis using this EXACT structure:
```json
{{
  "name": "Full Name",
  "education": {{
    "degree": "Highest Degree",
    "university": "University Name"
  }},
  "experience": {{
    "last_title": "Most Recent Job Title",
    "ats_score": 0-100
  }},
  "analysis": {{
    "technical_experience": 1-5,
    "project_relevance": 1-5,
    "extra_curricular": 1-5,
    "business_acumen": 1-5,
    "communication": 1-5,
    "leadership": 1-5,
    "innovative": 1-5,
    "cultural_fit": 1-5
  }},
  "summary": "50-word professional summary",
  "interview_questions": ["Question 1", "..."]
}}
```\n\nAnalyze this CV for a {job_category} position:"""