from sqlalchemy import select, desc
from flask import render_template, redirect, flash, url_for, request
from todoapp.models import User, Ticket, Comment
from todoapp import app
from todoapp import db
from todoapp.forms import  RegistrationForm, NewTicketForm, TicketForm, LoginForm, NewCommentForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime

db.create_all()


@app.route("/", methods=['GET', "POST"])
def home():
    done_tickets = []
    doing_tickets = []
    todo_tickets = []
    form = NewTicketForm()
    all_tickets = Ticket.query.all()
    for ticket in all_tickets:
        
        if ticket.deleted_at == None:
            if ticket.status == 'done':
                done_tickets.append(ticket)
            elif ticket.status == 'doing':
                doing_tickets.append(ticket) 
            else:
                todo_tickets.append(ticket)    
                
    form = NewTicketForm()
    if form.validate_on_submit():
        ticket = Ticket(name=form.name.data, status=form.status.data)
        db.session.add(ticket)
        db.session.commit()
        flash(f'Ticket {ticket.name} has been added in {ticket.status}', 'info')
        return redirect(url_for('home'))
    
    return render_template("home.html", todo_tickets=todo_tickets,  done_tickets=done_tickets, doing_tickets=doing_tickets, form=form, logged_in=current_user.is_authenticated)


@app.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    form = TicketForm()
    form_comment = NewCommentForm()
    ticket = Ticket.query.get(ticket_id)
    comments_query = select(Comment).filter(Comment.ticket_id == ticket_id).filter(Comment.deleted_at == None).order_by(Comment.created_at.desc())
    #comments_query = Comment.query.filter_by(ticket_id=ticket_id).filter_by(deleted_at=None).order_by(desc(comments.created_at))
    comments = [comment.Comment for comment in db.session.execute(comments_query)]
    form.name.default = ticket.name
    form.status.default = ticket.status
    form.label.default = ticket.label
    form.process()
    
    return render_template("options.html", form=form, form_comment=form_comment, ticket=ticket,comments=comments,logged_in=current_user.is_authenticated)


@app.route("/tickets/update/<int:ticket_id>", methods=["POST"])
def update_ticket(ticket_id):
    
    #if request.method == "PUT":
        ticket_to_update = Ticket.query.get(ticket_id)
        
        update_ticket_name = request.form.get('name')
        if update_ticket_name != '':
          ticket_to_update.name = update_ticket_name
        
        updated_label = request.form.get('label')
        ticket_to_update.label = updated_label
        
        status_to_update = request.form.get('status')
        ticket_to_update.status = status_to_update
        
        db.session.commit()
        flash('You successfully added some options! ', 'warning')
        return redirect(url_for('get_ticket', ticket_id=ticket_id ))   


@app.route("/tickets/comment/<int:ticket_id>", methods=["POST"])
def create_ticket_comment(ticket_id):
    form_comment = NewCommentForm()
    if form_comment.validate_on_submit():
        options = Comment(content=form_comment.name.data, ticket_id=ticket_id, user_id=current_user.id)
    
        db.session.add(options)
        db.session.commit()
        flash('You successfully added a comment! ', 'warning')
        return redirect(url_for('get_ticket', ticket_id=ticket_id )) 
 
    
@app.route("/tickets/delete/<int:ticket_id>",  methods=["GET"])
def delete_ticket(ticket_id):
   ticket_to_delete = Ticket.query.get(ticket_id)
   ticket_to_delete.deleted_at = datetime.utcnow()

   db.session.commit()
   flash(f'{ticket_to_delete.name} has been deleted', 'danger')
   return redirect(url_for('home'))    
    

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        user = User(username=form.username.data,
                     email=form.email.data, password=hash_and_salted_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {user.username} !', 'info')
        login_user(user)
        return redirect(url_for('home'))
    return render_template("register.html", title='Register', form=form, logged_in=current_user.is_authenticated)



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.", 'warning')
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Invalid password provided', 'warning')
            return redirect(url_for('login'))
        else:
            login_user(user)
            flash(f'Hi {current_user.username}!', 'success')
            return redirect(url_for('home'))

    return render_template("login.html", title='Login', form=form, logged_in=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out', 'info')
    return redirect(url_for('home'))
