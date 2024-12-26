from celery import shared_task
# from .models import interactionLogging


@shared_task(bind=True)
def testing_celery(self):
    for i in range(10):
        print(i)
    return "Done"