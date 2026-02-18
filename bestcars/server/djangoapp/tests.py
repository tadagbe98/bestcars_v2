import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Dealer, Review, CarMake, CarModel
from .views import analyze_sentiment, init_data


class SentimentTest(TestCase):
    def test_positive(self):
        self.assertEqual(analyze_sentiment("Fantastic services and great staff!"), "positive")

    def test_negative(self):
        self.assertEqual(analyze_sentiment("Terrible experience, rude and awful."), "negative")

    def test_neutral(self):
        self.assertEqual(analyze_sentiment("I visited the dealer."), "neutral")

    def test_empty(self):
        self.assertEqual(analyze_sentiment(""), "neutral")


class InitDataTest(TestCase):
    def test_init_creates_dealers(self):
        init_data()
        self.assertGreater(Dealer.objects.count(), 0)

    def test_init_creates_cars(self):
        init_data()
        self.assertGreater(CarMake.objects.count(), 0)
        self.assertGreater(CarModel.objects.count(), 0)

    def test_init_idempotent(self):
        init_data()
        count1 = Dealer.objects.count()
        init_data()
        count2 = Dealer.objects.count()
        self.assertEqual(count1, count2)


class DealerAPITest(TestCase):
    def setUp(self):
        init_data()
        self.client = Client()

    def test_get_all_dealers(self):
        res = self.client.get('/djangoapp/get_dealers')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertIn('dealers', data)
        self.assertGreater(len(data['dealers']), 0)

    def test_get_dealers_kansas(self):
        res = self.client.get('/djangoapp/get_dealers/Kansas')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        for d in data['dealers']:
            self.assertEqual(d['state'], 'Kansas')

    def test_get_dealer_by_id(self):
        dealer = Dealer.objects.first()
        res = self.client.get(f'/djangoapp/dealer/{dealer.id}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(data['dealer']['id'], dealer.id)

    def test_get_dealer_not_found(self):
        res = self.client.get('/djangoapp/dealer/99999')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(data['status'], 404)

    def test_get_reviews(self):
        dealer = Dealer.objects.first()
        res = self.client.get(f'/djangoapp/reviews/dealer/{dealer.id}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertIn('reviews', data)

    def test_get_cars(self):
        res = self.client.get('/djangoapp/get_cars')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertIn('CarModels', data)
        self.assertGreater(len(data['CarModels']), 0)

    def test_analyze_review(self):
        res = self.client.get('/djangoapp/analyze_review?text=Fantastic+services')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(data['sentiment'], 'positive')


class AuthAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123',
            first_name='Test', last_name='User', email='test@test.com'
        )

    def test_login_success(self):
        res = self.client.post('/djangoapp/login',
            data=json.dumps({'userName': 'testuser', 'password': 'testpass123'}),
            content_type='application/json')
        data = json.loads(res.content)
        self.assertEqual(data['status'], 'Authenticated')

    def test_login_fail(self):
        res = self.client.post('/djangoapp/login',
            data=json.dumps({'userName': 'testuser', 'password': 'wrong'}),
            content_type='application/json')
        data = json.loads(res.content)
        self.assertEqual(data['status'], 'Failed')

    def test_register(self):
        res = self.client.post('/djangoapp/register',
            data=json.dumps({'userName': 'newuser', 'firstName': 'New',
                             'lastName': 'User', 'email': 'new@test.com', 'password': 'newpass123'}),
            content_type='application/json')
        data = json.loads(res.content)
        self.assertEqual(data['status'], 'Authenticated')

    def test_register_duplicate(self):
        res = self.client.post('/djangoapp/register',
            data=json.dumps({'userName': 'testuser', 'password': 'anything'}),
            content_type='application/json')
        data = json.loads(res.content)
        self.assertEqual(data['error'], 'Already Registered')

    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        res = self.client.get('/djangoapp/logout')
        data = json.loads(res.content)
        self.assertIn('status', data)

    def test_add_review_unauthenticated(self):
        init_data()
        dealer = Dealer.objects.first()
        res = self.client.post('/djangoapp/add_review',
            data=json.dumps({'dealership': dealer.id, 'review': 'Great!'}),
            content_type='application/json')
        data = json.loads(res.content)
        self.assertEqual(data['status'], 403)

    def test_add_review_authenticated(self):
        init_data()
        self.client.login(username='testuser', password='testpass123')
        dealer = Dealer.objects.first()
        res = self.client.post('/djangoapp/add_review',
            data=json.dumps({'dealership': dealer.id, 'review': 'Great experience!',
                             'purchase': True, 'car_make': 'Toyota', 'car_model': 'Camry', 'car_year': 2023}),
            content_type='application/json')
        data = json.loads(res.content)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['review']['sentiment'], 'positive')
