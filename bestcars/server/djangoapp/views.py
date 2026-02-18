import json
import logging
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import CarMake, CarModel, Dealer, Review

logger = logging.getLogger(__name__)


# ─── Sentiment Analysis (simple, pas besoin d'IBM) ───────────────────────────

def analyze_sentiment(text):
    if not text:
        return "neutral"
    positive = ["great","excellent","amazing","fantastic","wonderful","good","best",
                "love","perfect","outstanding","superb","awesome","happy","satisfied",
                "recommend","helpful","friendly","clean","fast","professional","honest"]
    negative = ["bad","terrible","horrible","awful","worst","hate","poor","disappointing",
                "unhappy","rude","slow","overpriced","broken","failed","waste","problem",
                "issue","dishonest","unprofessional","scam","angry","frustrated"]
    t = text.lower()
    pos = sum(1 for w in positive if w in t)
    neg = sum(1 for w in negative if w in t)
    if pos > neg:
        return "positive"
    elif neg > pos:
        return "negative"
    return "neutral"


# ─── Init data ───────────────────────────────────────────────────────────────

def init_data():
    """Populate DB with sample data on first run."""
    if Dealer.objects.exists():
        return

    dealers = [
        {"full_name": "Sunshine Toyota", "short_name": "Sunshine", "address": "123 Main St",
         "city": "Wichita", "state": "Kansas", "st": "KS", "zip_code": "67201", "lat": 37.69, "lng": -97.34},
        {"full_name": "Prairie Ford", "short_name": "Prairie", "address": "456 Elm Ave",
         "city": "Topeka", "state": "Kansas", "st": "KS", "zip_code": "66601", "lat": 39.05, "lng": -95.68},
        {"full_name": "Bluegrass Hyundai", "short_name": "Bluegrass", "address": "147 West St",
         "city": "Overland Park", "state": "Kansas", "st": "KS", "zip_code": "66204", "lat": 38.98, "lng": -94.67},
        {"full_name": "Lakeside Honda", "short_name": "Lakeside", "address": "789 Oak Blvd",
         "city": "Austin", "state": "Texas", "st": "TX", "zip_code": "73301", "lat": 30.27, "lng": -97.74},
        {"full_name": "Metro Chevrolet", "short_name": "Metro", "address": "321 Pine Rd",
         "city": "Houston", "state": "Texas", "st": "TX", "zip_code": "77001", "lat": 29.76, "lng": -95.37},
        {"full_name": "Coastal BMW", "short_name": "Coastal", "address": "654 Sunset Blvd",
         "city": "Los Angeles", "state": "California", "st": "CA", "zip_code": "90001", "lat": 34.05, "lng": -118.24},
        {"full_name": "Empire Mercedes", "short_name": "Empire", "address": "987 Fifth Ave",
         "city": "New York", "state": "New York", "st": "NY", "zip_code": "10001", "lat": 40.71, "lng": -74.01},
        {"full_name": "Gateway VW", "short_name": "Gateway", "address": "258 Michigan Ave",
         "city": "Chicago", "state": "Illinois", "st": "IL", "zip_code": "60601", "lat": 41.88, "lng": -87.63},
        {"full_name": "Rocky Mountain Subaru", "short_name": "Rocky", "address": "50 Peak Ave",
         "city": "Denver", "state": "Colorado", "st": "CO", "zip_code": "80201", "lat": 39.74, "lng": -104.98},
        {"full_name": "Sunshine Nissan", "short_name": "Sun Nissan", "address": "900 Beach Rd",
         "city": "Miami", "state": "Florida", "st": "FL", "zip_code": "33101", "lat": 25.77, "lng": -80.19},
    ]
    dealer_objs = [Dealer.objects.create(**d) for d in dealers]

    # Reviews
    sample_reviews = [
        {"dealer": dealer_objs[0], "name": "John Smith", "review": "Fantastic services and very friendly staff! I love this place.",
         "purchase": True, "car_make": "Toyota", "car_model": "Camry", "car_year": 2023},
        {"dealer": dealer_objs[0], "name": "Jane Doe", "review": "Great experience overall. Would definitely recommend to friends!",
         "purchase": False, "car_make": "Toyota", "car_model": "RAV4", "car_year": 2022},
        {"dealer": dealer_objs[1], "name": "Bob Johnson", "review": "Excellent service and very fair pricing. Very happy with my purchase.",
         "purchase": True, "car_make": "Ford", "car_model": "F-150", "car_year": 2023},
        {"dealer": dealer_objs[2], "name": "Alice Williams", "review": "Amazing dealership! The team was very helpful and professional.",
         "purchase": True, "car_make": "Hyundai", "car_model": "Tucson", "car_year": 2022},
        {"dealer": dealer_objs[3], "name": "Charlie Brown", "review": "Terrible experience. Rude staff and overpriced vehicles. Never coming back.",
         "purchase": False, "car_make": "Honda", "car_model": "Civic", "car_year": 2021},
        {"dealer": dealer_objs[4], "name": "Emma Davis", "review": "Good selection of cars. The salesman was helpful and patient.",
         "purchase": True, "car_make": "Chevrolet", "car_model": "Equinox", "car_year": 2023},
    ]
    for r in sample_reviews:
        r["sentiment"] = analyze_sentiment(r["review"])
        Review.objects.create(**r)

    # Car makes & models
    makes_data = [
        {"name": "Toyota", "country": "Japan"},
        {"name": "Ford", "country": "USA"},
        {"name": "Honda", "country": "Japan"},
        {"name": "Chevrolet", "country": "USA"},
        {"name": "BMW", "country": "Germany"},
        {"name": "Mercedes-Benz", "country": "Germany"},
        {"name": "Hyundai", "country": "South Korea"},
        {"name": "Volkswagen", "country": "Germany"},
        {"name": "Nissan", "country": "Japan"},
        {"name": "Subaru", "country": "Japan"},
    ]
    models_data = [
        ("Toyota", "Camry", "SEDAN", 2023), ("Toyota", "RAV4", "SUV", 2022), ("Toyota", "Corolla", "SEDAN", 2021),
        ("Ford", "F-150", "TRUCK", 2023), ("Ford", "Explorer", "SUV", 2022), ("Ford", "Mustang", "COUPE", 2023),
        ("Honda", "Civic", "SEDAN", 2023), ("Honda", "CR-V", "SUV", 2022), ("Honda", "Accord", "SEDAN", 2021),
        ("Chevrolet", "Silverado", "TRUCK", 2023), ("Chevrolet", "Equinox", "SUV", 2022),
        ("BMW", "3 Series", "SEDAN", 2023), ("BMW", "X5", "SUV", 2022),
        ("Mercedes-Benz", "C-Class", "SEDAN", 2023), ("Mercedes-Benz", "GLE", "SUV", 2022),
        ("Hyundai", "Elantra", "SEDAN", 2023), ("Hyundai", "Tucson", "SUV", 2022),
        ("Volkswagen", "Jetta", "SEDAN", 2023), ("Volkswagen", "Tiguan", "SUV", 2022),
        ("Nissan", "Altima", "SEDAN", 2023), ("Nissan", "Rogue", "SUV", 2022),
        ("Subaru", "Outback", "SUV", 2023), ("Subaru", "Forester", "SUV", 2022),
    ]
    make_objs = {}
    for m in makes_data:
        obj, _ = CarMake.objects.get_or_create(name=m["name"], defaults={"country": m["country"]})
        make_objs[m["name"]] = obj
    for make_name, model_name, car_type, year in models_data:
        CarModel.objects.get_or_create(
            car_make=make_objs[make_name], name=model_name,
            defaults={"car_type": car_type, "year": year}
        )


# ─── API Views ───────────────────────────────────────────────────────────────

def get_dealerships(request, state="All"):
    init_data()
    if state == "All":
        dealers = Dealer.objects.all()
    else:
        dealers = Dealer.objects.filter(state__iexact=state)
    return JsonResponse({"status": 200, "dealers": [d.to_dict() for d in dealers]})


def get_dealer_details(request, dealer_id):
    init_data()
    try:
        dealer = Dealer.objects.get(id=dealer_id)
        return JsonResponse({"status": 200, "dealer": dealer.to_dict()})
    except Dealer.DoesNotExist:
        return JsonResponse({"status": 404, "message": "Dealer not found"})


def get_dealer_reviews(request, dealer_id):
    init_data()
    try:
        dealer = Dealer.objects.get(id=dealer_id)
        reviews = Review.objects.filter(dealer=dealer).order_by('-created_at')
        return JsonResponse({"status": 200, "reviews": [r.to_dict() for r in reviews]})
    except Dealer.DoesNotExist:
        return JsonResponse({"status": 404, "message": "Dealer not found"})


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "Method not allowed"})
    if not request.user.is_authenticated:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
    try:
        data = json.loads(request.body)
        dealer = Dealer.objects.get(id=data.get("dealership"))
        review_text = data.get("review", "")
        sentiment = analyze_sentiment(review_text)

        import datetime
        purchase_date = None
        pd_str = data.get("purchase_date", "")
        if pd_str:
            try:
                purchase_date = datetime.date.fromisoformat(pd_str)
            except:
                pass

        review = Review.objects.create(
            dealer=dealer,
            user=request.user,
            name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            review=review_text,
            purchase=data.get("purchase", False),
            purchase_date=purchase_date,
            car_make=data.get("car_make", ""),
            car_model=data.get("car_model", ""),
            car_year=data.get("car_year") or None,
            sentiment=sentiment,
        )
        return JsonResponse({"status": 200, "review": review.to_dict()})
    except Dealer.DoesNotExist:
        return JsonResponse({"status": 404, "message": "Dealer not found"})
    except Exception as e:
        logger.error(f"Error adding review: {e}")
        return JsonResponse({"status": 500, "message": str(e)})


@csrf_exempt
def login_request(request):
    if request.method != "POST":
        return JsonResponse({"status": 405})
    try:
        data = json.loads(request.body)
        username = data.get("userName", "")
        password = data.get("password", "")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({
                "userName": username,
                "status": "Authenticated",
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
            })
        return JsonResponse({"userName": username, "status": "Failed"})
    except Exception as e:
        return JsonResponse({"status": "Error", "message": str(e)})


def logout_request(request):
    username = request.user.username if request.user.is_authenticated else ""
    logout(request)
    return JsonResponse({"userName": username, "status": "Logged out"})


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"status": 405})
    try:
        data = json.loads(request.body)
        username = data.get("userName", "")
        if User.objects.filter(username=username).exists():
            return JsonResponse({"userName": username, "error": "Already Registered"})
        user = User.objects.create_user(
            username=username,
            first_name=data.get("firstName", ""),
            last_name=data.get("lastName", ""),
            email=data.get("email", ""),
            password=data.get("password", ""),
        )
        login(request, user)
        return JsonResponse({
            "userName": username,
            "status": "Authenticated",
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
        })
    except Exception as e:
        return JsonResponse({"status": "Error", "message": str(e)})


def get_cars(request):
    init_data()
    cars = CarModel.objects.select_related('car_make').all()
    return JsonResponse({"CarModels": [{
        "CarMake": c.car_make.name,
        "CarModel": c.name,
        "CarType": c.get_car_type_display(),
        "ModelYear": c.year,
    } for c in cars]})


def analyze_review_view(request):
    text = request.GET.get("text", "")
    if not text:
        return JsonResponse({"status": 400, "message": "No text provided"})
    sentiment = analyze_sentiment(text)
    return JsonResponse({"status": 200, "sentiment": sentiment, "text": text})
