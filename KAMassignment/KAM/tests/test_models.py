from django.test import TestCase
from ..models import KAMmail, leads, tracking, interactionLogging
from datetime import date

class TestModels(TestCase):
    def setUp(self):
        # Create initial data for testing
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
            callFrequency=5,
            time="12:00:00",
            lastCallMade=date.today()
        )
        self.tracker = tracking.objects.create(
            name="John Doe",
            role="Manager",
            phoneNumber="9876543210",
            emailID="johndoe@example.com",
            leadID=self.lead
        )
        self.interaction = interactionLogging.objects.create(
            type="order",
            notes="New order scheduled",
            followUp="Yes",
            date=date.today(),
            time="15:00:00",
            leadID=self.lead
        )

    def test_kammail_creation(self):
        self.assertEqual(self.kam.KAMmailid, "test@example.com")
        self.assertTrue(isinstance(self.kam, KAMmail))

    def test_leads_creation(self):
        self.assertEqual(self.lead.restaurantName, "Test Restaurant")
        self.assertEqual(self.lead.KAMID, self.kam)
        self.assertTrue(isinstance(self.lead, leads))

    def test_tracking_creation(self):
        self.assertEqual(self.tracker.name, "John Doe")
        self.assertEqual(self.tracker.leadID, self.lead)
        self.assertTrue(isinstance(self.tracker, tracking))

    def test_interaction_logging_creation(self):
        self.assertEqual(self.interaction.type, "order")
        self.assertEqual(self.interaction.leadID, self.lead)
        self.assertTrue(isinstance(self.interaction, interactionLogging))

    def test_lead_foreign_key_relationship(self):
        # Check if the lead is linked to the correct KAMmail
        self.assertEqual(self.lead.KAMID.KAMmailid, "test@example.com")

    def test_tracking_foreign_key_relationship(self):
        # Check if the tracker is linked to the correct lead
        self.assertEqual(self.tracker.leadID.restaurantName, "Test Restaurant")

    def test_interaction_logging_foreign_key_relationship(self):
        # Check if the interaction is linked to the correct lead
        self.assertEqual(self.interaction.leadID.restaurantName, "Test Restaurant")
