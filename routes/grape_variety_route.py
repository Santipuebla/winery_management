import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from models.db import db
from models.grape_variety import GrapeVariety

grape_variety = Blueprint('grape_variety', __name__, url_prefix='/grape_varieties')

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@grape_variety.route('/')
def get_varieties():
        varieties_list = GrapeVariety.query.all()
        return render_template ('grape_variety/grape_variety.html', GrapeVariety=varieties_list)

@grape_variety.route('create/new_variety', methods = ['POST'])


def add_variety():
        grape_name = request.form['grape_name'] 
        grape_origin = request.form['grape_origin']
        grape_image = request.files.get('image')
        filename = None
        status = bool(request.form.get('status',True))

        if grape_image and grape_name.filename != '':
            if allowed_file(grape_name.filename):
                filename = secure_filename(grape_image.filename)
                imagen_path = os.path.join(UPLOAD_FOLDER,filename)
                grape_image.save(imagen_path)
            else:
                flash('Formato de imagen invalido. Solo formato png,jpg,jpeg o gif.','danger')
                return redirect(request.referrer)
        
        new_variety = GrapeVariety(
            grape_name= grape_name,
            grape_origin= grape_origin,
            grape_image= filename,
            status = status 
        )

        db.session.add(new_variety)
        db.session.commit

        flash('Variedad cargada con exito','sucess')
        return redirect(url_for('grape_variety.get_varieties'))

@grape_variety('/edit_variety/<string:id>', methods = ['GET','POST'])

def edit_variety(id):
        variety = GrapeVariety.query.get_or_404(id)

        if request.method == 'POST':
            variety.grape_name = request.form['grape_name'] 
            variety.grape_origin = request.form['grape_origin']
            variety.grape_image = request.files.get('image')
            variety.status = bool(request.form.get('status',True)) == '1'

            #COMO SE MANEJA LA IMAGEN 
            grape_image = request.files.get('image')
            if grape_image and grape_image.filename != '':
                if allowed_file(grape_image.filename)
                #Procedemos a borrar la imagen anterior para luego cargar la nueva
                    if variety.image:
                        old_image_path = os.path.join(UPLOAD_FOLDER,variety.image)
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                    filename = secure_filename(grape_image.filename)
                    image_path = os.path.join(UPLOAD_FOLDER,filename)
                    grape_image.save(image_path)
                    grape_image.image = filename
                else:
                    flash('Formato de imagen invalido. Solo formato png,jpg,jpeg o gif.','danger')
                return redirect(request.referrer)
            
            db.session.commit
            flash('Producto actualizado con exito','sucess')
            return redirect(url_for('grape_variety.get_varieties'))
        return render_template ('variety'/'edit_variety.html', varieties_list=variety)