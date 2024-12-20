from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from . import db
from typing import List, Tuple, Any, Dict
from .models import Photo
from.schemas import PhotoCreateSchema

photo_bp = Blueprint('photo_bp', __name__)

@photo_bp.route('/')
def index() -> str:
    photos: List[Tuple[Any]] = Photo.query.all()

    return render_template('index.html', photos=photos)


@photo_bp.route('/SubirFoto', methods=['GET'])
def new_photo_form() -> str:
   return render_template('photo_form.html')


@photo_bp.route('/foto', methods=['POST'])
def create_photo() -> str:
    data: Tuple[Any] = request.form
    
    try:
        PhotoCreateSchema(title=data['title'],
                            description=data['description'],
                            image=str(data['image']))
        
    except ValueError as e:
        return jsonify({'error': e}), 400
    
    new_photo: Photo=Photo(title=data['title'],
                            description=data['description'],
                            image=str(data['image']))
    
    db.session.add(new_photo)
    db.session.commit()

    return redirect(url_for('photo_bp.index'))

@photo_bp.route('/foto/<int:photo_id>/edit')
def edit_photo_form(photo_id:int) -> str:
    photo: Photo = Photo.query.get_or_404(photo_id)
    return render_template('photo_form.html', photo=photo)

@photo_bp.route('/foto/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id:int) -> str:
    photo: Photo = Photo.query.get_or_404(photo_id)

    db.session.delete(photo)
    db.session.commit()

    return redirect(url_for('photo_bp.index'))

@photo_bp.route('/foto/<int:photo_id>', methods=['GET', 'POST'])
def update_photo(photo_id: int) -> str:
    photo: Photo = Photo.query.get_or_404(photo_id)

    if request.method == 'POST':
        data: Dict[str, str] = request.form

        try:
            photo_data: PhotoCreateSchema = PhotoCreateSchema(title=data['title'],
                                                                description=data['description'],
                                                                image=str(data['image']))
        
        except ValueError as e:
            return jsonify({'error': e}), 400
        
        photo.title = photo_data.title
        photo.description = photo_data.description
        photo.image = photo_data.image

        db.session.commit()
        return redirect(url_for('photo_bp.index'))
    
    return render_template('photo_form.html', photo=photo)