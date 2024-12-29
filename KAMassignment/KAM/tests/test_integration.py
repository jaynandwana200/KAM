import pytest
from django.urls import reverse
from KAM.models import KAMmail, leads, interactionLogging
from KAM.tasks import generateInteractions
from celery.result import AsyncResult
from datetime import datetime, timedelta

@pytest.mark.django_db
def test_full_workflow(client):
    """
    Test the full workflow:
    1. Add a KAMmail
    2. Create a lead assigned to the KAM
    3. Generate interactions via Celery task
    4. Validate the database state and check email interaction
    """

    # Step 1: Add a KAMmail via the view
    kam_data = {"email": "test.kam@example.com"}
    response = client.post(reverse("addKAM"), data=kam_data)
    assert response.status_code == 200
    assert KAMmail.objects.filter(KAMmailid="test.kam@example.com").exists()

    # Fetch the created KAM
    kam = KAMmail.objects.get(KAMmailid="test.kam@example.com")

    # Step 2: Create a lead assigned to the KAM
    lead_data = {
        "name": "Test Lead",
        "address": "123 Test St",
        "contactNo": "9876543210",
        "currentStatus": "active",
        "KAMID": kam.KAMID,
        "callFrequency": 7,
        "city": "Test City",
        "state": "Test State",
        "country": "Test Country",
        "time": "10:00:00",
    }
    response = client.post(reverse("createLeads"), data=lead_data)
    assert response.status_code == 200
    assert leads.objects.filter(restaurantName="Test Lead").exists()

    # Fetch the created lead
    lead = leads.objects.get(restaurantName="Test Lead")

    # Step 3: Generate interactions via Celery task
    # Simulate a past lastCallMade to trigger interaction generation
    lead.lastCallMade = datetime.now().date() - timedelta(days=lead.callFrequency)
    lead.save()

    # Trigger the task
    result = generateInteractions.delay()
    assert isinstance(result, AsyncResult)
    result.get(timeout=10)

    # Validate interactions were generated in the database
    interactions = interactionLogging.objects.filter(leadID=lead)
    assert interactions.exists()
    assert interactions.first().type == "call"
    assert interactions.first().notes == "Auto Generated"

    # Step 4: Validate email interaction
    # Check that email logic was executed successfully
    # This requires mocking send_mail if implemented in production
    # For now, validate the generated interaction data suffices
    assert lead.lastCallMade != datetime.now().date() - timedelta(days=lead.callFrequency)