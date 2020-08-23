from django.shortcuts import render, redirect
from django.contrib import messages
from fav_books_app.models import Book, User
import bcrypt

# Create your views here.
def login_reg(request):
  return render(request, "login_reg.html")

def process_reg(request):
  errors = User.objects.register_validator(request.POST)
  if len(errors) > 0:
    for key, error_msg in errors.items():
      messages.error(request, error_msg)
    return redirect('/')

  first_name = request.POST['first_name']
  last_name = request.POST['last_name']
  email = request.POST['email']
  password = request.POST['password']
  pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
  print(f"pw hash: {pw_hash}")

  new_user = User.objects.create(first_name=first_name, last_name=last_name,email=email, password=pw_hash)
  request.session['user_id'] = new_user.id
  messages.success(request, "Successfully registered!")
  return redirect("/")

def process_login(request):
  errors = User.objects.login_validator(request.POST)
  if len(errors) > 0:
    for key, error_msg in errors.items():
      messages.error(request, error_msg)
    return redirect('/')
  login_user_list = User.objects.filter(email=request.POST['email'])
  if login_user_list:
    this_user = login_user_list[0]
    if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
      request.session['user_id'] = this_user.id
      messages.success(request, "successfully logged in!")
      return redirect('/books')
  else:
    messages.error(request, "Password did not match")
  return redirect('/')

def log_out(request):
  request.session.flush()
  return redirect('/')

def index(request):
  if 'user_id' not in request.session:
    return redirect('/')
  user_id = request.session['user_id']
  user = User.objects.get(id = user_id)
  all_books = Book.objects.all()
  all_users = User.objects.all()
  context = {
    "all_books" : all_books,
    "all_users" : all_users,
    "user" : user
  }
  return render(request, "index.html", context)

def add(request, user_id):
  if 'user_id' not in request.session:
    return redirect('/')
  errors = Book.objects.book_validator(request.POST)
  if len(errors) > 0:
      for key, value in errors.items():
          messages.error(request, value)
      return redirect("/books")
  this_user = User.objects.get(id=user_id)
  book_title = request.POST['title']
  book_desc = request.POST['desc']
  new_book = Book.objects.create(title=book_title, desc=book_desc, uploaded_by = this_user)
  new_book.users_who_like.add(this_user)
  new_book.save()
  return redirect(f'/books/{new_book.id}')

def details(request, book_id):
  if 'user_id' not in request.session:
    return redirect('/')
  this_book = Book.objects.get(id = book_id)
  this_user = User.objects.get(id = request.session['user_id'])
  context = {
    "this_book" : this_book,
    "this_user" : this_user
  }
  print('logged in user is:', this_user)
  if this_user.id == this_book.uploaded_by.id:
    return render(request, "edit.html", context)
  else:
    return render(request, "details.html", context)

def edit(request, book_id):
  if 'user_id' not in request.session:
    return redirect('/')
  errors = Book.objects.book_validator(request.POST)
  if len(errors) > 0:
      for key, value in errors.items():
          messages.error(request, value)
  else:
    edit_this_book = Book.objects.get(id=book_id)
    edit_this_book.title = request.POST['title']
    edit_this_book.desc = request.POST['desc']
    edit_this_book.save()
    messages.success(request, "Book successfully updated")
  return redirect('/books')

def add_to_favs (request, book_id):
  this_book = Book.objects.get(id=book_id)
  this_user = User.objects.get(id=request.session['user_id'])
  this_book.users_who_like.add(this_user)
  this_book.save()
  return redirect(f'/books/{this_book.id}')

def un_favs(request, book_id):
  this_book = Book.objects.get(id=book_id)
  this_user = User.objects.get(id=request.session['user_id'])
  this_book.users_who_like.remove(this_user)
  this_book.save()
  return redirect(f'/books/{this_book.id}')

def delete(request, book_id):
  delete_this_book = Book.objects.get(id=book_id)
  delete_this_book.delete()
  messages.success(request,'Book successfully deleted')
  return redirect('/books')

def fav_list(request):
  user_id = request.session['user_id']
  this_user = User.objects.get(id=user_id)
  all_books = Book.objects.all()
  context = {
    "this_user" : this_user,
    "all_books" : all_books
  }
  return render(request, 'fav_list.html', context)
