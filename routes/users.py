from flask import Blueprint,jsonify,render_template, session
from model import User
from app import db
from flask_login import current_user, login_required

users = Blueprint('users', __name__,
                        template_folder='../templates')


@users.route('/get-users')
def get_all_users():
    if 'role' not in session or session['role'] != 'ADMIN':
        users_data = [{"error_code":"403","error_message":"Un Authorized"}]
        return jsonify(users_data)
    
    users = User.query.all()
    # Convert to a list of dictionaries for JSON response
    users_data = [{'id': user.id, 'username': user.username,'role':user.role} for user in users]

    return jsonify(users_data)

@users.route('/users')
def users_template():
    if 'role' not in session or session['role'] != 'ADMIN':
        # Redirect to another template if the role is not ADMIN
        return render_template('403.html')  # Custom template for access denied
    
    return render_template('users.html')


@users.route('/user/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"}), 200
    return jsonify({"error": "User not found!"}), 404