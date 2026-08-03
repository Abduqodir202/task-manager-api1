from celery import shared_task

@shared_task
def every_minute_task():
    print("Har 1 minutda ishladi!")
    return "OK"