import bcrypt, json
from time import sleep

from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from apps.login_reg.models import User, BillItem

def demo(request):
    return render(request, 'login_reg/demo.html')

def bills(request):
    if 'user_id' in request.session:
        return render(request, 'login_reg/bills.html')
    return redirect('login_reg:index')

def save_bill(request):
    if request.method == 'POST':
        try:
            description = request.POST['html_description']
            amount = float(request.POST['html_amount'])
            bill = BillItem.objects.create(user_id=request.session['user_id'], description=description, amount=amount)
            delete_url = reverse('login_reg:delete_bill', kwargs={'bill_id': bill.id})
            update_url = reverse('login_reg:update_bill', kwargs={'bill_id': bill.id})
            return JsonResponse({
                'description': description, 
                'amount': amount, 
                'bill_id': bill.id, 
                'delete_url': delete_url, 
                'update_url': update_url
            })
        except:
            raise
            return JsonResponse({'error': 'Server error'}, status=500)

    return JsonResponse({'error': 'Method Not Allowed'}, status=405)

def get_bills(request):
    bills = []
    for bill in BillItem.objects.filter(user_id=request.session['user_id']):
        delete_url = reverse('login_reg:delete_bill', kwargs={'bill_id': bill.id})
        update_url = reverse('login_reg:update_bill', kwargs={'bill_id': bill.id})
        bill_dictionary = {
                'description': bill.description, 
                'amount': bill.amount, 
                'bill_id': bill.id, 
                'delete_url': delete_url, 
                'update_url': update_url
            }
        bills.append(bill_dictionary)
    return JsonResponse(json.dumps(bills), safe=False)

def update_bill(request, bill_id):
    bill = BillItem.objects.get(id=bill_id)
    bill.description = request.POST['description']
    bill.amount = request.POST['amount']
    bill.save()
    return JsonResponse({'OK': 'it worked!'})


def delete_bill(request, bill_id):
    try:
        BillItem.objects.get(id=bill_id).delete()
        return JsonResponse({'message': 'Bill deleted'})
    except:
        pass

    return JsonResponse({'error': 'Server error'}, status=500)

def projects(request):
    return render(request, 'login_reg/projects.html')

def index(request):
    return render(request, 'login_reg/index.html')

def logout(request):
    request.session.clear()
    return redirect('login_reg:index')

def login(request):
    return render(request, 'login_reg/login.html')

def register(request):
    return render(request, 'login_reg/register.html')

def authenticate_ajax(request, auth_for):
    if request.method == 'POST':
        success = False
        user = None

        if auth_for == 'login':
            success, user = login_user(request)
        elif auth_for == 'register':
            success, user = register_user(request)

        if success:
            start_session(request, user)
            return JsonResponse({'url': redirect('login_reg:index').url})
        
        errors = []

        for message in messages.get_messages(request):
            errors.append(str(message))

        return JsonResponse({'errors': errors})

    return redirect('login_reg:index')

def authenticate(request, auth_for):
    if request.method == 'POST':
        success = False
        user = None

        if auth_for == 'login':
            success, user = login_user(request)
        elif auth_for == 'register':
            success, user = register_user(request)

        if success:
            start_session(request, user)
            return redirect('login_reg:index')
        else:
            return redirect('login_reg:'+auth_for)

    return redirect('login_reg:index')


def login_user(request):
    email = request.POST['html_email']
    password = request.POST['html_password']
    is_valid = check_length(request, email, 'Email')
    is_valid = check_length(request, password, 'Password')

    if is_valid:
        try:
            user = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return True, user
            else:
                messages.error(request, 'Invalid email or password')
        except:
            messages.error(request, 'Email not found. Please register.')

    return False, None



def register_user(request):
    username = request.POST['html_username']
    email = request.POST['html_email']
    password = request.POST['html_password']
    confirm = request.POST['html_confirm']

    is_valid = check_length(request, username, 'Full name')
    is_valid = check_length(request, email, 'Email')
    is_valid = check_length(request, password, 'Password')
    is_valid = check_length(request, confirm, 'Confirm password')

    if password != confirm:
        messages.error(request, 'Passwords do not match')
        is_valid = False

    if is_valid:
        try:
            user = User.objects.create(username=username, email=email, password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
            return True, user
        except:
            raise
            messages.error(request, 'That email address is already in use.  Please use a different email address.')

    
    return False, None


def start_session(request, user):
    request.session['user_id'] = user.id
    request.session['username'] = user.username


def check_length(request, data, name):
    if len(data) == 0:
        messages.error(request, name + ' cannot be left blank')
        return False

    return True