from flask import render_template, request, redirect, url_for, flash
from models import db, Movie

def init_routes(app):

    @app.route('/', methods=['GET'])
    def home():
        movies = Movie.query.all()
        return render_template('index.html', movies=movies)
    
    @app.route('/details', methods=['GET'])
    def details():
        id = request.args.get('id')
        movie = Movie.query.get(id)
        return render_template('details.html', movie=movie)

    @app.route('/edit', methods=['GET','POST'])
    def edit():
        if request.method == 'POST':
            try:
                # Update movie with form data
                id = request.form.get('id')
                movie = Movie.query.get(id)
                movie.title = request.form.get('title')
                movie.year = int(request.form.get('year'))
                movie.director = request.form.get('director')
                movie.image_url = request.form.get('image_url')
                movie.genre = request.form.get('genre')
                movie.rating = float(request.form.get('rating'))

                # Commit changes to database
                db.session.commit()

                # Flash success message
                flash('Movie updated successfully!', 'success')
                return redirect(url_for('details', id=id))
            except Exception as e:
                # If there's an error, rollback the session and flash error message
                db.session.rollback()
                flash(f'Error updating movie: {str(e)}', 'error')
                return redirect(url_for('edit', id=id))
        else:
            id = request.args.get('id')
            movie = Movie.query.get_or_404(id)
            return render_template('edit.html', id=id, movie=movie)

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

    @app.route('/delete', methods=['POST'])
    def delete():
        movie = Movie.query.get_or_404(id)
        try:
            db.session.delete(movie)
            db.session.commit()
            flash('Movie deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting movie: {str(e)}', 'error')
        return redirect(url_for('home'))
