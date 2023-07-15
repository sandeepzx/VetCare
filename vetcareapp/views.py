from django.utils import timezone
from django.shortcuts import render,HttpResponse,redirect
from registration.models import Consult,Doctor,Patient
from .models import UserDate,ChatForm
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import get_user_model
import json
import requests
import numpy as np
from sys import maxsize
from itertools import permutations
from django.db.models import Q



# Create your views here.
def home(req):
    
    
    return render(req,'index.html')




def contact(req):
    return render(req,'contact.html')

def doc(req,username):
    file = Doctor.objects.get(username = username)
 
    return render(req,"doc.html",{'doctor':file})

    
def doctors(req):
    doctor = Doctor.objects.all()
    return render(req,'doctors.html',{'doc_list':doctor})

def map(req):
    return render(req,'map.html')

def services(req):
    return render(req,'services.html')

def consultation(req,doctorname):
    file = Consult.objects.filter(doctor=doctorname)
    doc = Doctor.objects.get(username = doctorname)
    
    # The datas needed to request the dataas from gogle
    apikey = "shfdshfsdhu"
    url1 = "https://maps.googleapis.com/maps/api/distancematrix/json?destinations="
    url2 = "&origins="
    url3 = "&mode=car&units=imperial&key="
    origin = ""

    # Initialise the list for lattitude and longitude 
    Lat=[]
    Lng=[]

    # Append all the lattitude and longitude
    Lat.append(doc.lat)
    Lng.append(doc.lng)
    for i in file:
        Lat.append(i.lat)
        Lng.append(i.lng)
    
    lat_len = len(Lat)

    # Concatinating the lat and lng to make cordinates string
    for i in range(lat_len):
        origin += str(Lat[i])
        origin += ","
        origin += str(Lng[i])
        if i!=lat_len-1:
            origin += "|"

    # Assigning the origin value to destination
    destination = origin    

    # The joined URL to send the request to googlemap server response is saved to data
    url = url1+destination+url2+origin+url3+apikey
    # data = requests.get(url).json()

    # Demo data
    data = {
        "rows": [
            {
            "elements": [
                {
                "distance": {
                    "text": "1 m",
                    "value": 0
                },
                "duration": {
                    "text": "1 min",
                    "value": 0
                },
                "status": "OK"
                },
                {
                "distance": {
                    "text": "3.4 km",
                    "value": 3394
                },
                "duration": {
                    "text": "10 mins",
                    "value": 612
                },
                "status": "OK"
                },
                {
                "distance": {
                    "text": "2.4 km",
                    "value": 2359
                },
                "duration": {
                    "text": "6 mins",
                    "value": 349
                },
                "status": "OK"
                }
            ]
            },
            {
            "elements": [
                {
                "distance": {
                    "text": "3.6 km",
                    "value": 3570
                },
                "duration": {
                    "text": "9 mins",
                    "value": 557
                },
                "status": "OK"
                },
                {
                "distance": {
                    "text": "1 m",
                    "value": 0
                },
                "duration": {
                    "text": "1 min",
                    "value": 0
                },
                "status": "OK"
                },
                {
                "distance": {
                    "text": "2.6 km",
                    "value": 2622
                },
                "duration": {
                    "text": "6 mins",
                    "value": 354
                },
                "status": "OK"
                }
            ]
            },
            {
            "elements": [
                {
                "distance": {
                    "text": "2.4 km",
                    "value": 2351
                },
                "duration": {
                    "text": "6 mins",
                    "value": 382
                },
                "status": "OK"
                },
                {
                "distance": {
                    "text": "2.8 km",
                    "value": 2836
                },
                "duration": {
                    "text": "7 mins",
                    "value": 394
                },
                "status": "OK"
                },
                {
                "distance": {
                    "text": "1 m",
                    "value": 0
                },
                "duration": {
                    "text": "1 min",
                    "value": 0
                },
                "status": "OK"
                }
            ]
            }
        ],
        "originAddresses": [
            "SH22, Patturaikkal, Thrissur, Kerala 680020, India",
            "G5FV+RJ3, Kalyan Nagar, Ayyanthole, Thrissur, Kerala 680003, India",
            "Highdeals Door No 31/117/3A SRK Lane, near Murali Mandiram, Punkunnam, Thrissur, Kerala 680002, India"
        ],
        "destinationAddresses": [
            "SH22, Patturaikkal, Thrissur, Kerala 680020, India",
            "G5FV+RJ3, Kalyan Nagar, Ayyanthole, Thrissur, Kerala 680003, India",
            "Highdeals Door No 31/117/3A SRK Lane, near Murali Mandiram, Punkunnam, Thrissur, Kerala 680002, India"
        ]
        }
    li = []
    count = 0

    # Iterating in the data till the square of numder of points to get distance
    for obj in data:
        for d in data["rows"]:
            for e in d["elements"]:
                count +=1
                if count<= np.square(lat_len):
                    li.append(e['distance']['value'])      

    # Get the dimensions and convert the list to matrix  
    li = np.array(li)
    n = int(len(li) ** 0.5)
    graph = np.reshape(li,(n,n))
    V = lat_len

    # Demo matrix s is the starting point(node)
    graph = [[0, 20, 10], [25, 0, 10], [30, 20, 0]]
    s = 0

    # Get the cost and list of nodes by TSP function
    path,route = travellingSalesmanProblem(graph, s,V)
    route = np.unique(route)

    # Creating the list with ordering the lattitude and longitude
    latt = []
    lon = []
    latt.append(Lat[0])
    lon.append(Lng[0])
    for i in route:
        j = float(Lat[i])
        latt.append(j)
        lon.append(float(Lng[i]))

    # Creating a list including all locations 
    point = []
    for i in range(lat_len):
        point.append({'lat':latt[i],'lng':lon[i]})
    point.append({'lat':latt[0],'lng':lon[0]})

    # Give the data to html file 
    return render(req,"consultations.html",{'pets':file,'d':doc, 'distance': path,'route':route,'points':point})

def travellingSalesmanProblem(graph, s,V):
        node = []
        # store all vertex apart from source vertex
        vertex = []
              
        
        for i in range(V):
          if i != s:
            vertex.append(i)
        
        # store minimum weight Hamiltonian Cycle
        min_path = maxsize
        next_permutation=permutations(vertex)
        for i in next_permutation:
          # store current Path weight(cost)
          current_pathweight = 0

          # compute current path weight
          k = s
          for j in i:
            current_pathweight += graph[k][j]
            k = j
            
            node.append(k)

          current_pathweight += graph[k][s]
          if min_path > current_pathweight:
              san = node
          
          # update minimum
          min_path = min(min_path, current_pathweight)
          
        return min_path,san

def check_date(request):
    if request.method == 'POST':
        input_date = request.POST.get('date')
        UserDate.objects.create(date=input_date)
    
    current_date = timezone.now().date()
    user_dates = UserDate.objects.filter(date=current_date)
    
    context = {
        'user_dates': user_dates,
        'current_date': current_date
    }
    
    return render(request, 'notification.html', context)

def chat(req,username,doctorname):
    cond1= Q(sender = username)
    cond2= Q(receiver = username)
    chat_text = ChatForm.objects.filter( cond1 | cond2 )
    if req.method == 'POST':
        sender = username
        receiver = doctorname
        message = req.POST.get('message')
        task = ChatForm( sender = sender, message = message, receiver = receiver)
        task.save()
       
    return render(req,"chat.html",{'chat':chat_text})
