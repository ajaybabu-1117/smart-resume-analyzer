from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def match_skills(resume_text, required_skills):
    doc = [resume_text] + [' '.join(required_skills)]
    vec = TfidfVectorizer(stop_words='english').fit_transform(doc)
    sim = (vec[0] @ vec[1].T).toarray()[0][0]
    percent = round(float(sim) * 100, 2)
    skills_found = [skill for skill in required_skills if skill.lower() in resume_text.lower()]
    return percent, skills_found
