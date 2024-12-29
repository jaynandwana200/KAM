import pytest
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, get_default_timezone, utc
from KAM.models import leads, interactionLogging
from KAM.tasks import generateInteractions

@pytest.mark.django_db
def test_time_zone_call_scheduling():
    """
    Test call scheduling with time zone differences:
    1. Store all dates and times in UTC.
    2. Validate call scheduling for a lead in a different time zone.
    """

    # Step 1: Create a lead with a UTC call time
    utc_time = make_aware(datetime(2024, 12, 30, 15, 0, 0), utc)  # 3:00 PM UTC
    lead = leads.objects.create(
        restaurantName="Test Restaurant",
        address="123 Main St",
        city="Test City",
        state="Test State",
        country="Test Country",
        contactNumber="9876543210",
        currentStatus="active",
        callFrequency=7,  # Calls every 7 days
        lastCallMade=(datetime.utcnow() - timedelta(days=7)).date(),
        time=utc_time.time(),
    )

    # Step 2: Simulate generating interactions in UTC
    generateInteractions()  # This task will generate calls if due

    # Step 3: Fetch the scheduled interaction
    interaction = interactionLogging.objects.get(leadID=lead)
    assert interaction is not None

    # Verify the interaction's scheduled date and time are in UTC
    scheduled_date = interaction.date
    scheduled_time_utc = make_aware(
        datetime.combine(scheduled_date, interaction.time), utc
    )
    assert scheduled_time_utc == utc_time + timedelta(days=lead.callFrequency)

    # Step 4: Convert UTC time to a specific time zone for display
    local_tz = get_default_timezone()  # Default time zone, e.g., Asia/Kolkata
    scheduled_time_local = scheduled_time_utc.astimezone(local_tz)

    # Example: If local time zone is Asia/Kolkata (UTC+5:30)
    expected_local_time = make_aware(
        datetime(2024, 12, 31, 20, 30, 0), local_tz
    )  # 8:30 PM local time
    assert scheduled_time_local.hour == expected_local_time.hour
    assert scheduled_time_local.minute == expected_local_time.minute