import pytest
from KAM.tasks import generateInteractions
from KAM.models import leads, KAMmail

@pytest.mark.django_db
def test_generate_interactions_task():
    """Test the generateInteractions Celery task."""
    kam = KAMmail.objects.create(KAMmailid="test@gmail.com")
    lead = leads.objects.create(
        restaurantName="Test Restaurant",
        address="123 Main St",
        city="Kota",
        state="Rajasthan",
        country="India",
        contactNumber="1234567890",
        currentStatus="active",
        KAMID=kam,
        callFrequency=7,
        lastCallMade="2024-12-23",
    )
    generateInteractions()
    lead.refresh_from_db()
    assert lead.lastCallMade != "2024-12-23"