from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Api
from models import db, ma, Tutor, Pet
from resources import TutorResource, PetResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api = Api(app)
db.init_app(app)
ma.init_app(app)

@app.route('/tutor_lista')
def lista():
    return render_template('tutor_lista.html', Tutor=Tutor)

@app.route('/')
def index():
    tutors = Tutor.query.all()
    pets = Pet.query.all()
    return render_template('index.html', tutors=tutors, pets=pets)

@app.route('/tutor/<int:tutor_id>')
def tutor_lista(tutor_id):
    tutor = Tutor.query.get(tutor_id)
    return render_template('tutor_lista.html', tutor=tutor)

@app.route('/pet/<int:pet_id>')
def pet_lista(pet_id):
    pet = Pet.query.get(pet_id)
    return render_template('pet_lista.html', pet=pet, tutor=pet.tutor)


@app.route('/tutor', methods=['GET', 'POST'])
def create_tutor():
    if request.method == 'POST':
        name = request.form['name_tutor']
        tutor = Tutor(name_tutor=name)
        db.session.add(tutor)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('tutor.html')


@app.route('/pet', methods=['GET', 'POST'])
def create_pet():
    if request.method == 'POST':
        name = request.form['name_pet']
        tutor_id = request.form['pet_tutor']

        pet = Pet(name_pet=name, tutor_id=tutor_id)
        db.session.add(pet)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('pet.html', tutors=Tutor.query.all())

@app.route('/tutor/<int:tutor_id>/editar', methods=['GET', 'POST'])
def editar_tutor(tutor_id):
    tutor = Tutor.query.get(tutor_id)
    
    if request.method == 'POST':
        tutor.name_tutor = request.form['name_tutor']
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('editar_tutor.html', tutor=tutor)

@app.route('/tutor/<int:tutor_id>/excluir', methods=['GET', 'POST'])
def excluir_tutor(tutor_id):
    tutor = Tutor.query.get(tutor_id)
    
    if request.method == 'POST':
        db.session.delete(tutor)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('excluir_tutor.html', tutor=tutor)

@app.route('/pet/<int:pet_id>/editar', methods=['GET', 'POST'])
def editar_pet(pet_id):
    pet = Pet.query.get(pet_id)
    
    if request.method == 'POST':
        pet.name_pet = request.form['name_pet']
        pet.tutor_id = request.form['pet_tutor']
        db.session.commit()
        return redirect(url_for('index'))
    
    tutors = Tutor.query.all()
    return render_template('editar_pet.html', pet=pet, tutors=tutors)

@app.route('/pet/<int:pet_id>/excluir', methods=['GET', 'POST'])
def excluir_pet(pet_id):
    pet = Pet.query.get(pet_id)
    
    if request.method == 'POST':
        db.session.delete(pet)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('excluir_pet.html', pet=pet)


with app.app_context():
    db.create_all()

api.add_resource(TutorResource, '/tutor', '/tutor/<int:tutor_id>')
api.add_resource(PetResource, '/pet/<int:pet_id>')

if __name__ == '__main__':
    app.run(debug=True)
