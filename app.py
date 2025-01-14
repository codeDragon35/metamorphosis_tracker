from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, init_db
from models import User, Goal, Timeline



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metamorphosis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)


@app.route('/')
def home():
    return "Welcome to the Metamorphosis Tracker!"

# User routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Username already exists!', 'error')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# Goals routes
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    user_id = session['user_id']
    user = User.query.get(user_id)
    goals = Goal.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', user=user, goals=goals)

@app.route('/goals/new', methods=['GET', 'POST'])
def new_goal():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        user_id = session['user_id']

        new_goal = Goal(title=title, description=description, user_id=user_id)
        db.session.add(new_goal)
        db.session.commit()

        flash('Goal added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('new_goal.html')

@app.route('/goals/<int:id>')
def view_goal(id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    
    goal = Goal.query.get_or_404(id)
    timeline = Timeline.query.filter_by(goal_id=goal.id).all()
    return render_template('goal_details.html', goal=goal, timeline=timeline)


@app.route('/goals/<int:goal_id>/add_stage', methods=['GET', 'POST'])
def add_stage(goal_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))

    
    if request.method == 'POST':
        stage_name = request.form['stage_name']
        description = request.form['description']
        new_stage = Timeline(goal_id=goal_id, stage_name= stage_name, description=description)
        db.session.add(new_stage)
        db.session.commit()
        
        flash('Stage added successfully!', 'success')
        return redirect(url_for('view_goal', id=goal_id))
    
    return render_template('goal_details.html', goal_id=goal_id)

# @app.route('/track', methods=['POST'])
# def track():
#     data = request.get_json()
#     # Process the data here
#     return jsonify({"status": "success", "data": data})


# @app.route('/goals', methods=['POST'])
# def create_goal():
#     data = request.get_json()
#     new_goal = Goal(name=data['name'], progress=data['progress'])
#     db.session.add(new_goal)
#     db.session.commit()
#     return jsonify({"status": "success", "data": {"id": new_goal.id, "name": new_goal.name, "progress": new_goal.progress}})

# @app.route('/goals/<int:id>', methods=['GET'])
# def read_goal(id):
#     goal = Goal.query.get_or_404(id)
#     return jsonify({"id": goal.id, "name": goal.name, "progress": goal.progress})

# @app.route('/goals/<int:id>', methods=['PUT'])
# def update_goal(id):
#     data = request.get_json()
#     goal = Goal.query.get_or_404(id)
#     goal.name = data['name']
#     goal.progress = data['progress']
#     db.session.commit()
#     return jsonify({"status": "success", "data": {"id": goal.id, "name": goal.name, "progress": goal.progress}})

# @app.route('/goals/<int:id>', methods=['DELETE'])
# def delete_goal(id):
#     goal = Goal.query.get_or_404(id)
#     db.session.delete(goal)
#     db.session.commit()
#     return jsonify({"status": "success", "message": "Goal deleted"})

if __name__ == '__main__':
    app.run(debug=True)