from django.test import TestCase, Client
from django.urls import reverse
from ..models import leads, interactionLogging, KAMmail
from datetime import date

class TestViews(TestCase):
    def setUp(self):
        # Setting up a test client and initial data
        self.client = Client()
        self.kam = KAMmail.objects.create(KAMmailid="test@example.com")
        self.lead = leads.objects.create(
            restaurantName="Test Restaurant",
            address="123 Test Street",
            city="Test City",
            state="Test State",
            country="Test Country",
            contactNumber="1234567890",
            currentStatus="Active",
            KAMID=self.kam,
            callFrequency=10,
            time="12:00:00",
            lastCallMade=date.today()
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "KAM/index.html")

    def test_showKAM_view(self):
        response = self.client.get(reverse('showKAM'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "KAM/addKAM.html")
        self.assertContains(response, "test@example.com")

    def test_performanceTracking_view(self):
        response = self.client.get(reverse('performanceTracking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "KAM/performanceTracking.html")

    def test_createLeads_view_valid_data(self):
        data = {
            "name": "New Restaurant",
            "address": "456 New Street",
            "contactNo": "0987654321",
            "currentStatus": "Active",
            "KAMID": self.kam.KAMID,
            "callFrequency": 5,
            "city": "New City",
            "state": "New State",
            "country": "New Country",
            "time": "10:00:00"
        }
        response = self.client.post(reverse('createLeads'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(leads.objects.filter(restaurantName="New Restaurant").exists())

    def test_deleteKAM_view(self):
        data = {"KAMID": self.kam.KAMID}
        response = self.client.post(reverse('deleteKAM'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(KAMmail.objects.filter(KAMID=self.kam.KAMID).exists())

    def test_addInteraction_view_valid_data(self):
        data = {
            "leadID": self.lead.leadID,
            "type": "order",
            "notes": "New order scheduled",
            "followUp": "Yes",
            "date": date.today(),
            "time": "14:00:00"
        }
        response = self.client.post(reverse('addInteraction'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(interactionLogging.objects.filter(notes="New order scheduled").exists())

    def test_updateLeads_view_valid_data(self):
        data = {
            "leadId": self.lead.leadID,
            "name": "Updated Restaurant",
            "address": "789 Updated Street",
            "city": "Updated City",
            "state": "Updated State",
            "country": "Updated Country",
            "contactNo": "1231231234",
            "currentStatus": "Active",
            "callFrequency": 8,
            "KAMID": self.kam.KAMID
        }
        response = self.client.post(reverse('updateLeads'), data)
        self.assertEqual(response.status_code, 200)
        updated_lead = leads.objects.get(leadID=self.lead.leadID)
        self.assertEqual(updated_lead.restaurantName, "Updated Restaurant")

    def test_searchResult_view(self):
        data = {"searchResult": "Test"}
        response = self.client.post(reverse('searchResult'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "KAM/searchResult.html")
        self.assertContains(response, "Test Restaurant")
