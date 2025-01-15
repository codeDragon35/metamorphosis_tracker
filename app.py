from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, init_db
from sqlalchemy.exc import IntegrityError
from models import User, Goal, Timeline, Task



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metamorphosis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super_secret_key" #this is not a good practice but for the sake of saving time, I will leave it like this
# Initialize database
init_db(app)


@app.route('/')
def home():
    return render_template('index.html');

# User routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email= request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists!', 'error')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')

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


@app.route('/create-new-goals', methods=['GET', 'POST'])
def create_new_goals():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))

    return render_template('create-new-goals.html')

@app.route('/tasks/<int:id>', methods=['GET', 'POST'])
def tasks(id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))

    goal = Goal.query.get_or_404(id)
    if request.method == 'POST':
        description = request.form['description']
        total_timeline = request.form['timeline']
        task_name = request.form['tasks']
        tasks_list = task_name.split(',')
        for task in tasks_list:
            new_task = Task(goal_id=id, task_name=task.strip(), total_timeline=total_timeline, description=description)
            db.session.add(new_task)
        db.session.commit()
    
    flash('Tasks added successfully!', 'success')
    return redirect(url_for('dashboard'))



# Goals routes
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    user_id = session['user_id']
    user = User.query.get(user_id)
    goals = Goal.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', user=user.username, goals=goals)

@app.route('/goals/new', methods=['GET', 'POST'])
def new_goal():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        category = request.form['category']
        user_id = session['user_id']
        timeline = request.form['timeline']
        new_goal = Goal(title=title, description=description, status=status, category=category,timeline= timeline, user_id=user_id)
        db.session.add(new_goal)
        db.session.commit()

        flash('Goal added successfully!', 'success')
        return redirect(url_for('tasks', goal_name=title, id=new_goal.id, user_id=user_id, timeline=timeline))

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


@app.route('/start-journey', methods=['GET'])
def start_journey():
    category = request.args.get('category')
    return render_template('start-journey-form.html', category=category)

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