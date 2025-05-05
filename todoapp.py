from flask import Flask, render_template, request, redirect, url_for
import re
import os
import pickle

app = Flask(__name__)

# Create a file to store the ToDo list items
# This file will be used to persist the ToDo list across server restarts
DATA_FILE = 'todo_list.pkl'

# This allows the list to persist even after the server is restarted
# If the file does not exist, we start with an empty list
# This is a simple way to persist data without using a database
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'rb') as f:
        todo_list = pickle.load(f)
else:
    todo_list = []

# Validation regex for email and priority status
VALIDATION_EMAIL = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
VALIDATION_PRIORITY_STATUS = {"Low", "Medium", "High"}

@app.route('/')
def index():
    # Landing page: display the ToDo list
    return render_template('index.html', todos=todo_list)

# First Controller: Add a Task
@app.route('/submit', methods=['POST'])
def submit():
    task = request.form.get('task', '').strip()
    email = request.form.get('email', '').strip()
    priority = request.form.get('priority', '')

    # Validation reject bad input and redirect to index
    if not task or not VALIDATION_EMAIL.match(email) or priority not in VALIDATION_PRIORITY_STATUS:
        return redirect(url_for('index'))

    todo_list.append({
        'task': task,
        'email': email,
        'priority': priority
    })
    return redirect(url_for('index'))

# Clear / empty a list of tasks
@app.route('/clear', methods=['POST'])
def clear():
    todo_list.clear()
    return redirect(url_for('index'))

# Save the current state of the ToDo list to a file
@app.route('/save', methods=['POST'])
def save():
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(todo_list, f)
    return redirect(url_for('index'))

# Delete a specific task from the ToDo list
@app.route('/delete', methods=['POST'])
def delete():
    try:
        idx = int(request.form.get('index'))
        # Find the index to target 
        todo_list.pop(idx)
    except (ValueError, IndexError):
        pass
    return redirect(url_for('index'))

if __name__ == '__main__':
    # See output here : http://localhost:5000/
    
    # Run the Flask application on the local development server
    app.run()
