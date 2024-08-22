from django.test import TestCase
# this is a comment for Django CI Workflow testing purposes
import responses
import googlemaps

# Create your tests here.

# from https://github.com/googlemaps/google-maps-services-python/blob/master/tests/test_addressvalidation.py
class WildlifeValidationTest(TestCase):
    def setUp(self):
        self.key = "AIzaSyCgKpUnUDFKDoDKiJwbWriZ7Ca4ndoOBlo" # replaced with our key
        self.client = googlemaps.Client(self.key) #changed from googlemaps to django_google_maps

    @responses.activate
    def test_simple_addressvalidation(self):
        responses.add(
            responses.POST,
            "https://addressvalidation.googleapis.com/v1:validateAddress",
            body='{"address": {"regionCode": "US","locality": "Mountain View","addressLines": "1600 Amphitheatre Pkwy"},"enableUspsCass":true}',
            status=200,
            content_type="application/json",
        )

        results = self.client.addressvalidation('1600 Amphitheatre Pk', regionCode='US', locality='Mountain View', enableUspsCass=True)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "https://addressvalidation.googleapis.com/v1:validateAddress?" "key=%s" % self.key,
            responses.calls[0].request.url,
        )

# from https://github.com/googlemaps/google-maps-services-python/blob/master/tests/test_geolocation.py
class GeolocationTest(TestCase):
    def setUp(self):
        self.key = "AIzaSyCgKpUnUDFKDoDKiJwbWriZ7Ca4ndoOBlo" # replaced with our key
        self.client = googlemaps.Client(self.key) #changed from googlemaps to django_google_maps

    @responses.activate
    def test_simple_geolocate(self):
        responses.add(
            responses.POST,
            "https://www.googleapis.com/geolocation/v1/geolocate",
            body='{"location": {"lat": 51.0,"lng": -0.1},"accuracy": 1200.4}',
            status=200,
            content_type="application/json",
        )

        results = self.client.geolocate()

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "https://www.googleapis.com/geolocation/v1/geolocate?" "key=%s" % self.key,
            responses.calls[0].request.url,
        )