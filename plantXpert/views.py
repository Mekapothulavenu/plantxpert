from django.shortcuts import render,redirect
from django.contrib import messages
import requests
from datetime import datetime, timedelta
from googleapiclient.discovery import build
import os
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
# Create your views here.
def index(request):
  return render(request,"index.html")

def about_us(request):
    return render(request ,"about_us.html")

def Termsofservices(request):
    return render(request,"Termsofservices.html")

def privacy_policy(request):
    return render(request,"privacy_policy.html")






@login_required(login_url='login')
def agrishops(request):
  return render(request,"agriagrishops.html")

@login_required(login_url='login')
def assistant(request):
  return render(request,"assistant.html")




def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for reaching out to us!😊")
            return redirect("contact")  # Redirect to the same page after submission
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def index(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for reaching out to us!😊")
            return redirect("index")  # Redirect to the same page after submission
    else:
        form = ContactForm()

    return render(request, "index.html", {"form": form})


#weather
# OpenWeather API Key
API_KEY = "8781f02e33d96e889467f683df7e89d8"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Google Search API Key & Custom Search Engine ID
GOOGLE_API_KEY = "AIzaSyCxyQJV6SERjOsODCn0p3TVCSV25Fswons"
SEARCH_ENGINE_ID = "c32c85be101c34010"

CROP_SUGGESTIONS = {
    "hot_dry": [
        "Millets", "Groundnut", "Cotton", "Sorghum", "Chickpea", 
        "Sunflower", "Pulses", "Pigeon Pea", "Sesame", "Coriander"
    ],
    "hot_humid": [
        "Rice", "Sugarcane", "Banana", "Coconut", "Turmeric", 
        "Black Pepper", "Tapioca", "Arecanut", "Ginger", "Pineapple"
    ],
    "cool_dry": [
        "Wheat", "Barley", "Mustard", "Gram", "Linseed", 
        "Lentils", "Oats", "Peas", "Flaxseed", "Safflower"
    ],
    "cool_humid": [
        "Tea", "Coffee", "Cardamom", "Apple", "Pear", 
        "Plum", "Peach", "Cherry", "Strawberry", "Raspberry"
    ]
}


GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct"

def get_coordinates(place):
    """Convert any place (village, mandal, district, city) to latitude & longitude using OpenWeather Geocoding API."""
    url = f"{GEOCODING_URL}?q={place}&limit=1&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if not data:
        return None  # If no location found, return None

    return data[0]["lat"], data[0]["lon"]  # Extract latitude & longitude

def get_weather_data(place):
    """Fetch 7-day forecast weather data for any place (village, mandal, district, city)."""
    coordinates = get_coordinates(place)
    if not coordinates:
        return None  # Invalid place
    
    lat, lon = coordinates
    url = f"{FORECAST_URL}?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data.get("cod") != "200":
        return None  # API returned error
    
    forecast_list = []
    seen_dates = set()

    for entry in data["list"]:
        date = entry["dt_txt"].split()[0]

        if date not in seen_dates:
            seen_dates.add(date)
            forecast_list.append({
                "date": date,
                "temp": entry["main"]["temp"],
                "humidity": entry["main"]["humidity"],
                "rain_chance": entry.get("pop", 0) * 100,
                "description": entry["weather"][0]["description"],
                "icon": entry["weather"][0]["icon"],
            })
        
        if len(forecast_list) == 7:
            break  
    
    return forecast_list


def suggest_crops(temp, rain_chance):
    """Suggest crops based on temperature and rainfall probability."""
    if temp > 25 and rain_chance < 50:
        return CROP_SUGGESTIONS["hot_dry"]
    elif temp > 25 and rain_chance >= 50:
        return CROP_SUGGESTIONS["hot_humid"]
    elif temp <= 25 and rain_chance < 50:
        return CROP_SUGGESTIONS["cool_dry"]
    else:
        return CROP_SUGGESTIONS["cool_humid"]

def get_google_search_results(query):
    """Fetch relevant articles including images using Google Custom Search API."""
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    result = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=5).execute()
    
    articles = []
    if "items" in result:
        for item in result["items"]:
            # Extract image from page metadata (if available)
            image_url = ""
            if "pagemap" in item:
                if "cse_thumbnail" in item["pagemap"]:  # Thumbnail image
                    image_url = item["pagemap"]["cse_thumbnail"][0]["src"]
                elif "cse_image" in item["pagemap"]:  # Regular image
                    image_url = item["pagemap"]["cse_image"][0]["src"]

            articles.append({
                "title": item["title"],
                "link": item["link"],
                "snippet": item.get("snippet", ""),
                "image": image_url,
            })
    
    return articles


@login_required(login_url='login')
def weather(request):
    place = request.GET.get("place")  # Get any location input (city, village, mandal, district)

    weather_data = get_weather_data(place)
    if not weather_data:
        return render(request, "weather.html", {"error": "Place not found! Try again."})

    avg_temp = sum(day["temp"] for day in weather_data) / len(weather_data)
    avg_rain = sum(day["rain_chance"] for day in weather_data) / len(weather_data)
    crop_suggestions = suggest_crops(avg_temp, avg_rain)

    # Google Search for farming tips & weather updates
    search_query = f"{place} farming tips and weather updates"
    articles = get_google_search_results(search_query)

    context = {
        "place": place,
        "forecast_list": weather_data,
        "crop_suggestions": crop_suggestions,
        "articles": articles,
    }
    return render(request, "weather.html", context)



#news page
@login_required(login_url='login')
def news(request):
    API_KEY = '6ec3441f170047efaf182ee4db36793c'  # Replace with your actual NewsAPI key

    user_query = request.GET.get('keyword', '').strip()  # Ensure it fetches the search input

    query = f"agriculture AND ({user_query})" if user_query else "agriculture"

    url = f'https://newsapi.org/v2/everything?q={query}&sortBy=popularity&language=en&apiKey={API_KEY}'

    response = requests.get(url)
    agriculture_news = response.json()

    if agriculture_news.get("status") != "ok":
        return render(request, 'news.html', {'error': 'Failed to fetch news. Try again later.'})

    articles = agriculture_news.get("articles", [])

    required_keywords = {'agriculture', 'farming', 'crops', 'harvest', 'soil', 'pesticides', 'irrigation', 'farmer', 'organic'}
    unwanted_keywords = {'gardening', 'landscaping', 'real estate', 'home', 'decor', 'climate', 'technology', 'fashion'}

    news_list = []
    for article in articles:
        title = (article.get('title') or '').lower()
        description = (article.get('description') or '').lower()
        image_url = article.get('urlToImage') or 'https://via.placeholder.com/150'

        if any(word in title or word in description for word in required_keywords):
            if not any(word in title or word in description for word in unwanted_keywords):
                news_list.append({
                    'title': article.get('title', 'No title available'),
                    'description': article.get('description', 'No description available'),
                    'image_url': image_url,
                    'url': article.get('url', '#'),  # Ensure valid URL
                    'published_at': article.get('publishedAt', 'Unknown date'),
                    'source': article.get('source', {}).get('name', 'Unknown Source')
                })

    news_list = news_list[:12]  # ✅ Limit the number of articles to 12

    context = {'news_list': news_list, 'search_query': user_query}
    return render(request, 'news.html', context)


@login_required(login_url='login')
def agrishops(request):
    API_KEY = 'AIzaSyD5r3UUGBMZdmbRhLA_wTYJDTT-ZzNcIc8'  # Replace with actual Google Maps API key
    user_location = request.GET.get('location', '').strip()
    shop_type = request.GET.get('shop_type', '').strip()

    if not user_location:
        return render(request, 'agrishops.html', {'error': 'Please enter a location.'})

    shop_types = {
        'fertilizers': 'fertilizer shop',
        'seeds': 'seed shop',
        'nursery': 'plant nursery',
        'tools': 'agriculture tools store',
        'equipment': 'farm equipment store',
        'organic': 'organic farming shop',
        'pesticides': 'pesticide shop'
    }

    shop_query = shop_types.get(shop_type.lower(), 'agriculture shop')
    url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={shop_query}+in+{user_location}&key={API_KEY}'

    response = requests.get(url)
    shop_data = response.json()

    if shop_data.get("status") != "OK":
        return render(request, 'agrishops.html', {'error': 'Failed to fetch shop data. Try again later.'})

    shops = []
    default_image_url = "/static/images/shops_default_img.jpg"  # Ensure this image exists in static folder

    for place in shop_data.get("results", []):
        photo_reference = place.get('photos', [{}])[0].get('photo_reference')

        if photo_reference:
            image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={API_KEY}"
        else:
            image_url = default_image_url  # Use default image if no photo is available

        shops.append({
            'name': place.get('name', 'No Name Available'),
            'description': place.get('types', ['No Description Available'])[0],
            'image_url': image_url,
            'url': f"https://www.google.com/maps/place/?q=place_id:{place.get('place_id')}" if place.get('place_id') else '#',
            'location': place.get('formatted_address', 'No Address Available'),
            'contact': place.get('formatted_phone_number', 'No Contact Info')
        })

    # Limit to 12 results
    shops = shops[:12]

    context = {'shop_list': shops, 'search_query': user_location, 'shop_type': shop_type}
    return render(request, 'agrishops.html', context)
















