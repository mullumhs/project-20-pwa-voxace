from flask import render_template, request, redirect, url_for, flash
from models import db, Movie

def init_routes(app):

    @app.route('/', methods=['GET'])
    def home():
        movies = Movie.query.all()
        return render_template('index.html', movies=movies)

    @app.route('/add', methods=['POST'])
    def add():
        try:
            # Get form data
            title = request.form.get('title')
            year = request.form.get('year')
            director = request.form.get('director')
            image_url = request.form.get('image_url')
            genre = request.form.get('genre')
            rating = request.form.get('rating')

            # Create new movie instance
            new_movie = Movie(
                title=title,
                year=int(year),
                director=director,
                image_url=image_url,
                genre=genre,
                rating=float(rating)
            )

            # Add to database
            db.session.add(new_movie)
            db.session.commit()

            # Flash success message
            flash('Movie added successfully!', 'success')
        except Exception as e:
            # If there's an error, rollback the session and flash error message
            db.session.rollback()
            flash(f'Error adding movie: {str(e)}', 'error')

        return redirect(url_for('home'))

    @app.route('/update', methods=['POST'])
    def update():
        # This route should handle updating an existing item identified by the given ID.
        return render_template('index.html', message=f'Item updated successfully')

    @app.route('/delete', methods=['POST'])
    def delete():
        # This route should handle deleting an existing item identified by the given ID.
        return render_template('index.html', message=f'Item deleted successfully')
