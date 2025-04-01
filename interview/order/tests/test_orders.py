from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from interview.order.models import Order
from interview.inventory.models import Inventory
from datetime import date

class DeactivateOrderViewTests(APITestCase):
    """
    A few basic tests using Django's built in APITestCase
    """
    def setUp(self):
        # type_id should be a reference to an InventoryType id
        # language_id should be a reference to an InventoryLanguage.id of an object
        # Tests will currently not pass, but this is an illustration.
        self.inventory = Inventory.objects.create(
            name="Test Inventory",
            metadata={},
            type_id=1,
            language_id=1,
        )

        self.active_order = Order.objects.create(
            inventory=self.inventory,
            start_date=date.today(),
            embargo_date=date.today(),
            is_active=True
        )

        self.inactive_order = Order.objects.create(
            inventory=self.inventory,
            start_date=date.today(),
            embargo_date=date.today(),
            is_active=False
        )

    def test_deactivate_already_inactive_order(self):
        url = reverse('deactivate-order', kwargs={'pk': self.inactive_order.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("already inactive", response.data["detail"].lower())

    def test_deactivate_active_order(self):
        url = reverse('deactivate-order', kwargs={'pk': self.active_order.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("deactivated", response.data["detail"].lower())

        self.active_order.refresh_from_db()
        self.assertFalse(self.active_order.is_active)

    def test_deactivate_invalid_pk_format(self):
        """
        Test a string
        """
        url = reverse('deactivate-order', kwargs={'pk': "abc"})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("invalid id format", response.data["error"].lower())

    # Two more tests would ideally be added to test all5 response cases of DeactivateOrderView.