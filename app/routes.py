# app/routes.py
#
# This file defines the URL routes (pages) and error handlers of the application.
# - Stage 3: Handles PDF upload, validation, and raw text extraction.
# - Stage 4: Calls parse_resume_text() to extract structured NLP details.
# - Stage 5: Saves the parsed candidate profile to PostgreSQL via SQLAlchemy.
# - Stage 6: Dashboard route (/candidates) and Detail view route (/candidate/<id>).
# - Stage 7: Custom error handlers (404, 413, 500).
# - Feature: Delete Candidate route (/candidate/<id>/delete).

import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Candidate
from app.parser import extract_text_from_pdf, parse_resume_text

# Create a Blueprint named 'main'
bp = Blueprint('main', __name__)


def allowed_file(filename):
    """
    Check if the uploaded file has a .pdf extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'


@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Homepage route — handles displaying the upload form (GET)
    and processing the uploaded resume (POST).
    """
    if request.method == 'GET':
        return render_template('index.html')

    uploaded_file = request.files.get('resume')

    if not uploaded_file or uploaded_file.filename == '':
        flash('Please select a PDF file before clicking Upload.', 'error')
        return redirect(url_for('main.index'))

    if not allowed_file(uploaded_file.filename):
        flash('Invalid file type. Please upload a PDF file only.', 'error')
        return redirect(url_for('main.index'))

    filename = secure_filename(uploaded_file.filename)
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(save_path)

    # --- Stage 3: Extract text from PDF ---
    try:
        extracted_text = extract_text_from_pdf(save_path)
    except Exception as e:
        flash(f'Could not read the PDF file. Error: {str(e)}', 'error')
        return redirect(url_for('main.index'))

    if not extracted_text.strip():
        flash(
            'No text could be extracted from this PDF. '
            'It may be a scanned image or a protected document.',
            'error'
        )
        return redirect(url_for('main.index'))

    # --- Stage 4: NLP & Regex Parsing ---
    parsed_data = parse_resume_text(extracted_text)

    # --- Stage 5: Database Persistence (PostgreSQL) ---
    candidate_id = None
    try:
        new_candidate = Candidate(
            filename=filename,
            name=parsed_data.get('name'),
            email=parsed_data.get('email'),
            phone=parsed_data.get('phone'),
            skills=parsed_data.get('skills'),
            education=parsed_data.get('education'),
            experience=parsed_data.get('experience'),
            raw_text=extracted_text
        )
        db.session.add(new_candidate)
        db.session.commit()
        candidate_id = new_candidate.id
    except Exception:
        db.session.rollback()
        flash('Resume parsed successfully, but database save encountered an issue.', 'error')

    # Render results page with candidate ID, parsed data, and raw text
    return render_template(
        'results.html',
        filename=filename,
        parsed_data=parsed_data,
        extracted_text=extracted_text,
        candidate_id=candidate_id
    )


# --- Stage 6 Routes ---

@bp.route('/candidates', methods=['GET'])
def list_candidates():
    """
    Candidates Dashboard Route — displays all candidates stored in PostgreSQL,
    ordered by newest first.
    """
    candidates = Candidate.query.order_by(Candidate.created_at.desc()).all()
    return render_template('candidates.html', candidates=candidates)


@bp.route('/candidate/<int:candidate_id>', methods=['GET'])
def view_candidate(candidate_id):
    """
    Candidate Detail View Route — displays full profile and raw text
    for a specific candidate by database ID.
    """
    candidate = Candidate.query.get_or_404(candidate_id)
    return render_template('candidate_detail.html', candidate=candidate)


# --- Delete Candidate Route ---

@bp.route('/candidate/<int:candidate_id>/delete', methods=['POST'])
def delete_candidate(candidate_id):
    """
    Deletes a candidate record from PostgreSQL and removes the corresponding
    uploaded PDF file from the uploads/ directory.
    """
    candidate = Candidate.query.get_or_404(candidate_id)

    # 1. Attempt to remove the uploaded PDF file from disk
    if candidate.filename:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], candidate.filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  # Safely proceed with DB deletion even if file removal fails

    # 2. Delete candidate record from PostgreSQL
    try:
        db.session.delete(candidate)
        db.session.commit()
        flash('Candidate deleted successfully.', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred while deleting the candidate from the database.', 'error')

    return redirect(url_for('main.list_candidates'))


# --- Stage 7 Error Handlers ---

@bp.app_errorhandler(404)
def handle_404_error(error):
    """
    Custom 404 handler — redirects user gracefully if a page or candidate profile is not found.
    """
    flash('The requested page or candidate profile was not found.', 'error')
    return redirect(url_for('main.list_candidates'))


@bp.app_errorhandler(413)
def handle_413_error(error):
    """
    Custom 413 handler — catches files exceeding MAX_CONTENT_LENGTH (5MB limit).
    """
    flash('The uploaded file is too large. Please upload a PDF file smaller than 5 MB.', 'error')
    return redirect(url_for('main.index'))


@bp.app_errorhandler(500)
def handle_500_error(error):
    """
    Custom 500 handler — catches unhandled internal server errors safely.
    """
    db.session.rollback()
    flash('An unexpected server error occurred. Please try again.', 'error')
    return redirect(url_for('main.index'))
