from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Package, Booking
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import TravelSystem
from django.db.models import Q
from .models import Travel
def search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = Travel.objects.filter(
            Q(name__icontains=query) |
            Q(mode__icontains=query) |  # e.g., flight, bus, train, cab
            Q(source__icontains=query) |
            Q(destination__icontains=query)
        )
    return render(request, 'booking/search_results.html', {
        'query': query,
        'results': results
    })
# --------- AUTH ----------
def register_view(request):
    if request.method == "POST":
        username = request.POST['username'].strip()
        password = request.POST['password']
        email = request.POST['email'].strip()

        # --- VALIDATION ---
        errors = []
        if not username or not email or not password:
            errors.append("All fields are required.")

        if User.objects.filter(username=username).exists():
            errors.append("Username already exists.")

        if User.objects.filter(email=email).exists():
            errors.append("Email already registered.")

        if len(password) < 6:
            errors.append("Password must be at least 6 characters long.")

        if not any(ch.isdigit() for ch in password):
            errors.append("Password must contain at least one number.")

        if not any(ch.isupper() for ch in password):
            errors.append("Password must contain at least one uppercase letter.")

        if errors:
            return render(request, 'booking/register.html', {'errors': errors})

        # --- CREATE USER ---
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect('home')

    return render(request, 'booking/register.html')





def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # basic empty-field check
        if not username or not password:
            error = "Please enter both username and password."
        else:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                # custom message you asked for:
                error = "Wrong — pls enter correct username/password or if new user, register."

    return render(request, 'booking/login.html', {'error': error})



def logout_view(request):
    logout(request)
    return redirect('home')


# --------- HOME ----------
def home(request):
    packages = Package.objects.all()
    travels = TravelSystem.objects.all()
    return render(request, 'booking/home.html', {
        'packages': packages,
        'travels': travels
    })
# --------- PACKAGE CRUD ----------
@login_required
def package_list(request):
    packages = Package.objects.all()
    return render(request, 'booking/package_list.html', {'packages': packages})


@login_required
def add_package(request):
    if request.method == "POST":
        Package.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            price=request.POST['price'],
            duration=request.POST['duration'],
            destination=request.POST['destination'],
            available_seats=request.POST['available_seats']
        )
        return redirect('package_list')
    return render(request, 'booking/add_package.html')


@login_required
def update_package(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == "POST":
        for field in ['title', 'description', 'price', 'duration', 'destination', 'available_seats']:
            setattr(package, field, request.POST[field])
        package.save()
        return redirect('package_list')
    return render(request, 'booking/add_package.html', {'package': package})


@login_required
def delete_package(request, pk):
    get_object_or_404(Package, pk=pk).delete()
    return redirect('package_list')


# --------- BOOKINGS ----------
@login_required
def book_package(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == "POST":
        travel_date = request.POST['travel_date']
        Booking.objects.create(user=request.user, package=package, travel_date=travel_date)
        return redirect('my_bookings')
    return render(request, 'booking/book_package.html', {'package': package})


@login_required
def my_bookings(request):
    if request.user.is_staff:
        bookings = Booking.objects.all()  # Admin sees all
    else:
        bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


# --------- BACKUP ----------
@login_required
def backup(request):
    return render(request, 'booking/backup.html')
# --------- TRAVEL SYSTEM CRUD ----------
@login_required
def travel_list(request):
    query = request.GET.get('q', '').strip()
    if query:
        travels = TravelSystem.objects.filter(
            Q(mode__icontains=query) |
            Q(source__icontains=query) |
            Q(destination__icontains=query)
        )
    else:
        travels = TravelSystem.objects.all()

    return render(request, 'booking/travel_list.html', {
        'travels': travels,
        'query': query
    })



@login_required
def add_travel(request):
    if request.method == 'POST':
        mode = request.POST['mode']
        source = request.POST['source']
        destination = request.POST['destination']
        price = request.POST['price']
        available_seats = request.POST['available_seats']

        image = request.FILES.get('image')
        travel = TravelSystem(
            mode=mode,
            source=source,
            destination=destination,
            price=price,
            available_seats=available_seats,
            image=image
        )
        travel.save()
        return redirect('travel_list')

    return render(request, 'booking/add_travel.html')


@login_required
def update_travel(request, pk):
    travel = get_object_or_404(TravelSystem, pk=pk)
    if request.method == 'POST':
        travel.mode = request.POST['mode']
        travel.source = request.POST['source']
        travel.destination = request.POST['destination']
        travel.price = request.POST['price']
        travel.available_seats = request.POST['available_seats']
        if request.FILES.get('image'):
            travel.image = request.FILES['image']
        travel.save()
        return redirect('travel_list')

    return render(request, 'booking/add_travel.html', {'travel': travel})


@login_required
def delete_travel(request, pk):
    travel = get_object_or_404(TravelSystem, pk=pk)
    travel.delete()
    return redirect('travel_list')