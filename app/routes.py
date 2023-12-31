from datetime import datetime
from flask_login import login_user, LoginManager, login_required, current_user
from flask import render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash
from app import app, db, bcrypt, login_manager
from app.models import User, RegistrationForm, NoteForm, Note, LoginForm, Client, ClientForm


ALLOW_REGISTRATION = True


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if not ALLOW_REGISTRATION:
        print(f'Регистрация новых пользователей отключина!')
        return redirect(url_for('login'))


    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print(f'Учетная запись {new_user.username} создана')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            print(f'Не удалось выполнить вход! Проверь данные')
    return render_template('login.html', form=form)


@app.route('/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    form = ClientForm()
    if form.validate_on_submit():
        new_client = Client(name=form.name.data, phone=form.phone.data ,user_id=current_user.id)
        db.session.add(new_client)
        db.session.commit()
        print(f'Клиент {new_client.name} успешно добавлен!')
        return redirect(url_for('dashboard'))
    return render_template('add_client.html', form=form)



@app.route('/modify_balance/<int:client_id>', methods=['POST'])
@login_required
def modify_balance(client_id):
    client = Client.query.get_or_404(client_id)
    amount = float(request.form['amount'])

    if request.form['action'] == 'add':
        client.balance += amount
    elif request.form['action'] == 'subtract':
        client.balance -= amount

    db.session.commit()
    print(f'Баланс клиента {client.name} изменен! Текущий баланс: {client.balance}')
    return redirect(url_for('dashboard'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/dashboard')
@login_required
def dashboard():
    clients = Client.query.join(User).add_columns(Client.id, Client.name, Client.phone, User.username, Client.balance).all()
    return render_template('dashboard.html', clients=clients)


@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        submitted_title = form.title.data
        submitted_note = form.content.data
        new_note = Note(title=submitted_title, content=submitted_note, timestamp=datetime.utcnow())
        try:
            db.session.add(new_note)
            db.session.commit()
        except Exception as e:
            print(f'Ошибка при добалвении заметки: {e}')
            db.session.rollback()
        return redirect(url_for('add_note'))
    return render_template('add_note.html', form=form)


@app.route('/display_note')
def display_note():
    notes = Note.query.order_by(Note.timestamp.desc()).all()
    return render_template('display_note.html', notes=notes)

