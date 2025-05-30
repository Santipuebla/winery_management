import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from models.db import db
from models.grape_variety import GrapeVariety 

grape_varieties = Blueprint('grape_varieties', __name__, url_prefix='/grape_varieties') #

UPLOAD_FOLDER = 'static/images' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@grape_varieties.route('/get_grape_varieties')
def get_grape_varieties():
    # Solo obtenemos las variedades con status = True (activas)
    grape_varieties_list = GrapeVariety.query.all()
    context = { "grape_varieties": grape_varieties_list  }
    return render_template('grape_varieties/grape_varieties.html', **context)

@grape_varieties.route('/add_grape_variety', methods=['POST'])
def add_grape_variety(): 
    # Obtenemos los datos de un formulario HTML
    grape_name = request.form['grape_name']
    grape_origin = request.form['grape_origin']
    status = bool(request.form.get('status', True)) 
    image_file = request.files.get('image') # Se espera un campo 'image'
    filename = None

    if image_file and image_file.filename != '':
        if allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(image_path)
        else:
            flash('Formato de imagen no permitido. Solo png, jpg, jpeg, gif.', 'danger')
            return redirect(request.referrer)

    new_variety = GrapeVariety(
        grape_name=grape_name,
        grape_origin=grape_origin,
        grape_image=filename, # Se guarda el nombre del archivo
        status=status # Se guarda el estado
    )

    db.session.add(new_variety)
    db.session.commit()

    flash('Variedad agregada exitosamente!', 'success')
    return redirect(url_for('grape_varieties.get_grape_varieties')) 

@grape_varieties.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_grape_variety(id): # Renombrada
    grape_variety = GrapeVariety.query.get_or_404(id)

    if request.method == 'POST':
        grape_variety.grape_name = request.form['grape_name']
        grape_variety.grape_origin = request.form['grape_origin']
        grape_variety.status = request.form.get('status') == '1' # Manejo de status (asumiendo que '1' significa True, '0' o no presente False)

        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            if allowed_file(image_file.filename):
                # Borrar imagen vieja
                if grape_variety.grape_image:
                    old_image_path = os.path.join(UPLOAD_FOLDER, grape_variety.grape_image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                # Guardar nueva imagen
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image_file.save(image_path)
                grape_variety.grape_image = filename
            else:
                flash('Formato de imagen no permitido. Solo png, jpg, jpeg, gif.', 'danger')
                return redirect(request.referrer)
            
        db.session.commit()
        flash('Variedad actualizada exitosamente!', 'success')
        return redirect(url_for('grape_varieties.get_grape_varieties'))

    # Si es GET, se renderiza un formulario de edición HTML
    return render_template('grape_varieties/edit_grape_varieties.html', grape_varieties=grape_variety)

@grape_varieties.route('/delete/<string:id>', methods=['POST'])
def delete_grape_variety(id):
    grape_variety = GrapeVariety.query.get_or_404(id)

    # NO borramos la imagen al hacer eliminación lógica. Si la variedad se reactiva, la imagen debe seguir asociada.

    grape_variety.status = False  
    db.session.commit()
    flash('Variedad eliminada exitosamente!', 'success') # Pasa a ser inactivo. 
    return redirect(url_for('grape_varieties.get_grape_varieties'))

@grape_varieties.route('/add_grape_variety', methods=['GET'])
def show_add_grape_variety_form():
    return render_template('grape_varieties/add_grape.html')

@grape_varieties.route('/new', methods=['GET'])
def get_add_grape_variety():
    return render_template('grape_varieties/add_grape.html')