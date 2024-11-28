from flask import Blueprint,request, jsonify, send_from_directory,current_app
from flask_login import current_user, login_required
import psutil
import shutil
import os
import logging

# Set up basic logging
# logging.basicConfig(level=logging.DEBUG)

files = Blueprint('files', __name__,
                        template_folder='../templates')



# Route to handle file uploads
@files.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save file to the uploads folder
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return jsonify({'message': 'File uploaded successfully!'})


# Route to handle disk usage stats
@files.route('/system_info', methods=['GET'])
def system_info():
    try:
        # Get disk usage stats
        disk_usage = psutil.disk_usage('/')
        total = disk_usage.total
        used = disk_usage.used
        free = disk_usage.free
        percent = disk_usage.percent

        # Get CPU usage stats (1 second interval for more accurate reading)
        cpu_usage = psutil.cpu_percent(interval=1)

        # Get memory usage stats
        memory_usage = psutil.virtual_memory().percent

        data = {
            'total': total,
            'used': used,
            'free': free,
            'percent': percent,
            'cpu_percent': cpu_usage,
            'memory_percent': memory_usage
        }
        
        return jsonify(data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to handle file download
@files.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # Safely serve files from the upload folder
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to handle file deletion
@files.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        # Construct the full file path
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Check if the file exists
        if os.path.exists(file_path):
            os.remove(file_path)  # Delete the file
            return jsonify({'message': f'File {filename} deleted successfully!'}), 200
        else:
            return jsonify({'error': 'File not found!'}), 404
    except Exception as e:
        logging.error(f"Error deleting file {filename}: {e}")
        return jsonify({'error': str(file_path)}), 500
        
# Create Folder Route
@files.route('/create_folder', methods=['POST'])
def create_folder():
    data = request.json
    folder_name = data.get('folderName')
    if not folder_name:
        return jsonify({'error': 'Folder name is required'}), 400

    folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_name)
    try:
        os.makedirs(folder_path, exist_ok=True)
        return jsonify({'message': f'Folder {folder_name} created successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rename Folder Route
@files.route('/rename_folder', methods=['POST'])
def rename_folder():
    data = request.json
    old_name = data.get('oldName')
    new_name = data.get('newName')

    if not old_name or not new_name:
        return jsonify({'error': 'Old and new folder names are required'}), 400

    old_path = os.path.join(files.config['UPLOAD_FOLDER'], old_name)
    new_path = os.path.join(files.config['UPLOAD_FOLDER'], new_name)

    try:
        os.rename(old_path, new_path)
        return jsonify({'message': f'Folder {old_name} renamed to {new_name} successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete Folder Route
@files.route('/delete_folder/<folder_name>', methods=['POST'])
@files.route('/delete_folder/<folder_name>', methods=['POST'])
def delete_folder(folder_name):
    folder_path = os.path.join('uploads', folder_name)

    try:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            return jsonify({'error': 'Folder does not exist'}), 400

        logging.debug(f"Attempting to delete folder: {folder_path}")
        
        # Check if folder is empty, if not, remove files first
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Remove individual files
                    logging.debug(f"Deleted file: {file_path}")
                else:
                    shutil.rmtree(file_path)  # If it's a subdirectory, delete it recursively
                    logging.debug(f"Deleted subfolder: {file_path}")
            except PermissionError as e:
                logging.error(f"Permission error deleting {file_path}: {str(e)}")
                return jsonify({'error': f"Permission error deleting {filename}: {str(e)}"}), 500
            except Exception as e:
                logging.error(f"Error deleting {file_path}: {str(e)}")
                return jsonify({'error': f"Error deleting {filename}: {str(e)}"}), 500
        
        # Now that the folder is empty, delete the folder
        try:
            os.rmdir(folder_path)
            logging.debug(f"Folder {folder_name} deleted successfully")
            return jsonify({'message': f'Folder {folder_name} deleted successfully'}), 200
        except PermissionError as e:
            logging.error(f"Permission error when deleting the folder itself: {str(e)}")
            return jsonify({'error': 'Permission denied when deleting folder itself'}), 500
        except Exception as e:
            logging.error(f"Unexpected error deleting the folder: {str(e)}")
            return jsonify({'error': 'Unexpected error occurred when deleting folder'}), 500

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Unexpected error occurred. Please try again.'}), 500

# Updated Files Route
@files.route('/files', methods=['GET'])  # Keep this if it is the intended route
def list_files():
    try:
        items = []
        for entry in os.listdir(current_app.config['UPLOAD_FOLDER']):
            full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], entry)
            items.append({'name': entry, 'isFolder': os.path.isdir(full_path)})
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rename or modify the conflicting route if needed
@files.route('/list_all_files', methods=['GET'])  # Example alternative route
def list_all_files():
    # Implement the logic for this alternative if necessary
    pass

    return jsonify({'error': str(e)}), 500

