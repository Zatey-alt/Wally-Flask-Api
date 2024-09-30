from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config.from_object('config.Config')
db = SQLAlchemy(app)

# Wallpaper Model
class Wallpaper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)

# Favorite Model
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallpaper_id = db.Column(db.Integer, db.ForeignKey('wallpaper.id'), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)  # Unique user ID for storing favorites

# Create database tables within the application context
with app.app_context():
    db.create_all()

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def home():
    return redirect(url_for('admin_dashboard')) 



# Admin Routes

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_wallpaper = Wallpaper(filename=filename)
            db.session.add(new_wallpaper)
            db.session.commit()
            return redirect(url_for('admin_dashboard'))

    wallpapers = Wallpaper.query.all()
    return render_template('admin_dashboard.html', wallpapers=wallpapers)

@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_wallpaper(id):
    wallpaper = Wallpaper.query.get(id)
    if wallpaper:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], wallpaper.filename))
        db.session.delete(wallpaper)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

# API to get wallpapers for users
@app.route('/api/wallpapers', methods=['GET'])
def get_wallpapers():
    wallpapers = Wallpaper.query.all()
    return jsonify([{'id': wp.id, 'filename': wp.filename} for wp in wallpapers])

# API to add a wallpaper to favorites
@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    user_id = request.json.get('user_id')
    wallpaper_id = request.json.get('wallpaper_id')
    
    if not user_id or not wallpaper_id:
        return jsonify({'error': 'Missing user ID or wallpaper ID'}), 400

    favorite = Favorite(user_id=user_id, wallpaper_id=wallpaper_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Added to favorites'}), 200

# API to get favorites for a users
@app.route('/api/favorites/<user_id>', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    favorite_wallpapers = [Wallpaper.query.get(fav.wallpaper_id) for fav in favorites]
    return jsonify([{'id': wp.id, 'filename': wp.filename} for wp in favorite_wallpapers])

# Serve wallpaper images
@app.route('/uploads/<filename>')
def serve_wallpaper(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Handle wallpaper download (This saves the wallpaper to the phone when accessed via a mobile browser)
@app.route('/api/download/<filename>', methods=['GET'])
def download_wallpaper(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
