from django.contrib import messages, auth
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from registration.models import Patient, Doctor,Consult


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username taken")
                return render(request, "pet_reg.html")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email taken")
                return render(request, "pet_reg.html")
            else:
                Patient.objects.create(username=username, email=email, phonenumber=phonenumber, address=address)
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save();

        else:
            messages.info(request, "password not matching")
            return render(request, "pet_reg.html")
        return redirect('/')
    return render(request, 'pet_reg.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
    
        if user is not None:
            auth.login(request, user)
            patient = Patient.objects.filter(username=username).exists()
            print("patient login using ",username)
            return render(request,"index.html", {'yes': patient} )
        else:
            messages.info(request, "invalid credentials")
            return redirect(login)
        
    return render(request, "login.html")

def doctor(request):
    if request.method == 'POST':
        username = request.POST['username']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        email = request.POST['email']
        lat = request.POST.get('lattitude')
        lng = request.POST.get('longitude')
        time1 = request.POST['time1']
        time2 = request.POST['time2']
        days = request.POST['days']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username taken")
                return render(request, 'doc_reg.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email taken")
                return render(request, 'doc_reg.html')
            else:
                Doctor.objects.create(username=username, email=email, phonenumber=phonenumber, address=address,lat = lat, lng = lng, time1=time1, time2=time2, days=days)
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save();

        else:
            messages.info(request, "password not matching")
            return render(request, 'doc_reg.html')
        return redirect('/')
    return render(request, 'doc_reg.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            doctor = Doctor.objects.filter(username=username).exists()
            patient = Patient.objects.filter(username=username).exists()
            if doctor:
                print("doctor logined using ",username)
                return render(request,"index.html", {'no': doctor} )
            elif patient:
                print("pet logined using ",username)
                return render(request,"index.html", {'yes': patient} )
            else:
                print("another")
            
        else:
            messages.info(request, "invalid credentials")
            print("else in doctors login")
            return render(request,"login.html")
        
    return render(request, "login.html")

def logout(req):
    auth.logout(req)
    print("logout")
    return redirect('/')

# doctor booking  
def pet(req,username,User_id):
    if req.method == 'POST':
        doc = Doctor.objects.get(username=username)
        user = Patient.objects.get(username=User_id)
        doctorname = doc.username
        ownername = user.username
        phone = req.POST.get('phone')
        lat = req.POST.get('lattitude')
        lng = req.POST.get('longitude')
        name = req.POST.get('petname')
        age = req.POST.get('petage')
        pet_type = req.POST.get('patientdetails')
        problem = req.POST.get('pmessage')
        book = Consult.objects.create(ownername = ownername,phone = phone, lat = lat, lng = lng, pet_name = name, pet_age = age, pet_type = pet_type,symptoms = problem, doctor = doctorname)
        book.save()
        print("doctor booked by ", name)
        return redirect('/')
    return render(req,'booking.html')