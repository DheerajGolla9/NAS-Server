from flask import Blueprint,jsonify,render_template, session, request
from model import User, Role
from app import db, admin_permission
from flask_login import current_user, login_required

users = Blueprint('users', __name__,
                        template_folder='../templates')


@users.route('/get-users')
@admin_permission.require(http_exception=403)
@login_required
def get_all_users():
    users = User.query.all()
    if not users:
        return jsonify({"message": "No users found"}), 404

    users_data = [
        {
            'id': user.id,
            'username': user.username,
            'role':user.role.name
        } 
        for user in users
    ]

    return jsonify(users_data), 200

@users.route('/users')
@admin_permission.require(http_exception=403)
@login_required
def users_template():
    if 'role' not in session or session['role'] != 'ADMIN':
        # Redirect to another template if the role is not ADMIN
        return render_template('403.html')  # Custom template for access denied
    
    return render_template('users.html')

@users.route('/user/update/<int:user_id>', methods=['PUT'])
@admin_permission.require(http_exception=403)
@login_required
def update_user(user_id):
    # Check if the current user has permission to update roles
    if not current_user.has_role('ADMIN'):
        return jsonify({"error": "Unauthorized. Only admins can update roles."}), 403

    # Get the new role from the request JSON
    data = request.get_json()
    new_role_name = data.get('role')

    if not new_role_name:
        return jsonify({"error": "Role name is required."}), 400

    # Fetch the user by ID
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    # Fetch the role by name
    new_role = Role.query.filter_by(name=new_role_name).first()
    if not new_role:
        return jsonify({"error": f"Role '{new_role_name}' does not exist."}), 404

    # Update the user's role
    user.role = new_role
    db.session.commit()
    session['role']=new_role_name
    return jsonify({
        "message": f"Role of user '{user.username}' updated to '{new_role.name}'."
    }), 200



@users.route('/user/delete/<int:user_id>', methods=['DELETE'])
@admin_permission.require(http_exception=403)
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"}), 200
    return jsonify({"error": "User not found!"}), 404


@users.errorhandler(403)
def forbidden_error(e):
    return jsonify({"error": "You do not have permission to access this resource."}), 403
