from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Listing, Category, ListingImage
from .forms import ListingForm

def index_view(request):
    listings = Listing.objects.filter(status='ACTIVE')
    
    search_query = request.GET.get('search', '')
    location_query = request.GET.get('location', '')
    category_id = request.GET.get('category', '')
    
    if search_query:
        listings = listings.filter(title__icontains=search_query) | listings.filter(description__icontains=search_query)
        
    if location_query:
        listings = listings.filter(city__icontains=location_query)
        
    if category_id:
        listings = listings.filter(category_id=category_id)
        
    categories = Category.objects.all()
    
    context = {
        'listings': listings.distinct(),
        'categories': categories,
        'search_query': search_query,
        'location_query': location_query,
        'selected_category': category_id,
    }
    return render(request, 'index.html', context)

def product_detail_view(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    
    listing.views_count += 1
    listing.save(update_fields=['views_count'])
    
    context = {
        'listing': listing,
    }
    return render(request, 'product_detail.html', context)

@login_required
def create_listing_view(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        files = request.FILES.getlist('image')
        
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            
            for i, f in enumerate(files):
                is_main_photo = (i == 0)
                ListingImage.objects.create(listing=listing, image=f, is_main=is_main_photo)
                
            return redirect('product_detail', pk=listing.pk)
    else:
        form = ListingForm()
        
    return render(request, 'create_listing.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')
