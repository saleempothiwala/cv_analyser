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
Guidelines:
- Cultural Fit: Alignment with our no-micromanagement philosophy
- Innovation: Evidence of novel solutions/approaches
- Leadership: Formal roles or demonstrated initiative
- Convert all scores to numbers
- Be critical - we want top 10% candidates

Include Kermit Tech's core values explicitly:
- Emphasize experience with secure application development
- Look for evidence of self-direction
- Prioritize candidates with data literacy certifications
- Reward innovative problem-solving examples

```\n\nAnalyze this CV for a {job_category} position:"""

AUDIO_ANALYSIS_PROMPT = """Analyze interview audio transcript for a {job_category} position. Generate VALID JSON analysis using this EXACT structure:
```json
{{
  "analysis": {{
  "communication_score": 1-5,  
  "technical_depth": 1-5,      
  "confidence": 1-5,           
  "keyword_usage": 1-5
  }},
  "red_flags": ["Overuse of filler words"],
  "summary": "150-word professional summary"
}}

Guidelines:
- Cultural Fit: Alignment with our no-micromanagement philosophy
- Innovation: Evidence of novel solutions/approaches
- Leadership: Formal roles or demonstrated initiative
- Convert all scores to numbers
- Be critical - we want top 10% candidates

Include Kermit Tech's core values explicitly:
- Emphasize experience with secure application development
- Look for evidence of self-direction
- Prioritize candidates with data literacy certifications
- Reward innovative problem-solving examples
"""