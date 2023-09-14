from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "ZlatkoPejakovicJunior"

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(100))
    evolution = db.Column(db.String(100))

@app.route('/')
def home():
    pokemon_list = Pokemon.query.all()
    return render_template('base.html', pokemon_list = pokemon_list)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get("name")
    type = request.form.get("type")
    evolution = request.form.get("evolution")

    if not name or not type or not evolution:
        error_message = "Molimo ispunite sva obavezna polja (Ime, Tip i Evolucija)."
        flash(error_message, 'error')
        return render_template('base.html', error_message=error_message)

    new_pokemon = Pokemon(name=name, type=type, evolution=evolution)
    db.session.add(new_pokemon)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/update/<int:pokemon_id>', methods=['GET', 'POST'])
def update(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)

    if request.method == 'POST':
        new_name = request.form.get("name")
        new_type = request.form.get("type")
        new_evolution = request.form.get("evolution")

        pokemon.name = new_name
        pokemon.type = new_type
        pokemon.evolution = new_evolution
        db.session.commit()

        return redirect(url_for("home"))
    
    else:
        return render_template("update.html", pokemon=pokemon)

@app.route('/delete/<int:pokemon_id>')
def delete(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    db.session.delete(pokemon)
    db.session.commit()
    return redirect(url_for("home"))


from collections import defaultdict

def count_pokemon_types(pokemon_list):
    type_counts = defaultdict(int)

    for pokemon in pokemon_list:
        type_counts[pokemon.type] += 1

    return type_counts

@app.route('/count_types')
def count_types():
    pokemon_list = Pokemon.query.all()
    type_counts = count_pokemon_types(pokemon_list)
    return render_template('count_types.html', type_counts=type_counts)

@app.route('/search', methods=['POST'])
def search():
    search_type = request.form.get("searchType")
    if not search_type:
        flash("Molimo unesite tip pokemona za pretragu.", 'error')
        return redirect(url_for("home"))

    pokemon_list = Pokemon.query.filter_by(type=search_type).all()
    
    if not pokemon_list:
        flash(f"Nema pokemona tipa {search_type}.", 'info')
    
    return render_template('base.html', pokemon_list=pokemon_list)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.debug = True
    app.run(port=8000)
