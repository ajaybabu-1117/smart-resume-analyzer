from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
import os
import io
import pandas as pd
from . import db
from .models import Resume
from .utils.parser import extract_text_from_file
from .utils.matcher import match_skills
from config import Config

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('resumes')
        skills = request.form.get('skills','').split(',')
        saves = []
        for file in files:
            filename = secure_filename(file.filename)
            path = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(path)
            text = extract_text_from_file(path, filename)
            percent, skills_found = match_skills(text, skills)
            resume = Resume(filename=filename, raw_text=text, match_percent=percent, skills=','.join(skills_found))
            db.session.add(resume)
            saves.append(resume)
        db.session.commit()
        return redirect(url_for('main.results'))
    return render_template('upload.html')

@main.route('/results')
def results():
    resumes = Resume.query.order_by(Resume.match_percent.desc()).all()
    return render_template('results.html', resumes=resumes)

@main.route('/admin')
def admin():
    resumes = Resume.query.all()
    df = pd.DataFrame([{
        'Filename': r.filename,
        'Match %': r.match_percent,
        'Skills': r.skills,
        'Uploaded': r.uploaded_at
    } for r in resumes])
    stats = {
        'total': len(df),
        'avg_match': round(df['Match %'].mean(), 2) if not df.empty else 0
    }
    return render_template('admin.html', stats=stats, resumes=resumes)

@main.route('/download')
def download():
    resumes = Resume.query.order_by(Resume.match_percent.desc()).all()
    df = pd.DataFrame([{
        'Filename': r.filename,
        'MatchPercent': r.match_percent,
        'SkillsFound': r.skills,
        'UploadedAt': r.uploaded_at
    } for r in resumes])
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='resume_results.csv', mimetype='text/csv')
