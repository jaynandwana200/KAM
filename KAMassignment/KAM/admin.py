from django.contrib import admin

# Register your models here.
from .models import leads
from .models import tracking
from .models import interactionLogging

admin.site.register(leads)
admin.site.register(tracking)
admin.site.register(interactionLogging)
