import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Dossier de stockage principal sur Render
BASE_BACKUP_DIR = "backup_recu"

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg')
VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Aucun fichier reçu"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "Nom de fichier vide"}), 400

    # Sécurisation du nom de fichier pour le serveur
    filename = secure_filename(file.filename)
    filename_lower = filename.lower()
    
    # 1. Détermination du sous-dossier selon l'extension
    if filename_lower.endswith(VIDEO_EXTENSIONS):
        sub_folder = "Video"
    elif filename_lower.endswith(IMAGE_EXTENSIONS):
        sub_folder = "Image"
    else:
        return jsonify({"status": "ignored", "message": "Format non supporté"}), 200

    # 2. Création dynamique de l'arborescence complète si nécessaire
    target_folder = os.path.join(BASE_BACKUP_DIR, sub_folder)
    os.makedirs(target_folder, exist_ok=True)

    # 3. Enregistrement du fichier
    save_path = os.path.join(target_folder, filename)
    file.save(save_path)
    
    return jsonify({"status": "success", "message": f"Fichier stocké dans {sub_folder}"}), 200

if __name__ == '__main__':
    # Configuration requise pour l'environnement Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
