from flask import Blueprint, render_template, request, redirect, url_for 
import os
from werkzeug.utils import secure_filename

varieties = Blueprint('varieties', __name__)


varieties_data = [] #prueba luego eliminar 

@varieties.route('/varieties/new', methods=['GET', 'POST'])
def create_variety():
    if request.method == 'POST':

        name = request.form['grape_name']
        origin = request.form['grape_origin']
        image_file = request.files['grape_image']

    
        filename = ''
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            path = os.path.join('static/uploads', filename)
            image_file.save(path)

     
        new_variety = {
            'grape_name': name,
            'grape_origin': origin,
            'grape_image': filename
        }

        varieties_data.append(new_variety)

        print('Variedad registrada:', new_variety)

        return redirect(url_for('varieties.list_varieties'))

    return render_template('varieties/form.html')

@varieties.route('/varieties')
def list_varieties():
    return render_template('varieties/list.html', varieties=varieties_data)


# from flask import Blueprint, render_template, request, redirect, url_for
# import os
# from werkzeug.utils import secure_filename
# from models.grape_variety import GrapeVariety
# from app import db

# varieties = Blueprint('varieties', __name__)

# @varieties.route('/varieties/new', methods=['GET', 'POST'])
# def create_variety():
#     if request.method == 'POST':
#         name = request.form['grape_name']
#         origin = request.form['grape_origin']
#         image_file = request.files['grape_image']

#         filename = ''
#         if image_file and image_file.filename != '':
#             filename = secure_filename(image_file.filename)
#             path = os.path.join('static/uploads', filename)
#             image_file.save(path)

#         new_variety = GrapeVariety(
#             grape_name=name,
#             grape_origin=origin,
#             grape_image=filename
#         )

#         db.session.add(new_variety)
#         db.session.commit()

#         return redirect(url_for('varieties.list_varieties'))

#     return render_template('varieties/form.html')

# @varieties.route('/varieties')
# def list_varieties():
#     varieties = GrapeVariety.query.all()
#     return render_template('varieties/list.html', varieties=varieties)
