from django.conf import settings
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from picker.models import PickedNumber, PickerSettings
from picker.views import clear_results, initialize_numbers


class PickerBehaviorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def attach_messages(self, request):
        SessionMiddleware(lambda req: None).process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)

    def test_initialize_numbers_creates_ten_slots(self):
        initialize_numbers()

        self.assertEqual(PickedNumber.objects.count(), 10)
        self.assertEqual(list(PickedNumber.objects.order_by('number').values_list('number', flat=True)), list(range(1, 11)))

    def test_clear_results_only_clears_matching_user(self):
        PickedNumber.objects.create(number=1, user='Alice', is_picked=True)
        PickedNumber.objects.create(number=2, user='Bob', is_picked=True)
        PickedNumber.objects.create(number=3, user='Alice', is_picked=True)

        request = self.factory.post('/clear/', {'user': 'Alice'})
        self.attach_messages(request)
        response = clear_results(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(PickedNumber.objects.filter(user='Alice').count(), 0)
        self.assertEqual(PickedNumber.objects.filter(user='Bob').count(), 1)
        self.assertTrue(PickedNumber.objects.filter(number=2, user='Bob').first().is_picked)

    def test_initialize_numbers_uses_admin_slot_count(self):
        PickerSettings.objects.create(slot_count=7)

        initialize_numbers()

        self.assertEqual(PickedNumber.objects.count(), 7)
        self.assertEqual(list(PickedNumber.objects.order_by('number').values_list('number', flat=True)), list(range(1, 8)))

    def test_static_root_is_configured_for_collectstatic(self):
        self.assertTrue(settings.STATIC_ROOT)
        self.assertIn('staticfiles', str(settings.STATIC_ROOT))
