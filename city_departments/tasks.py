from celery import shared_task



@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_widgets():
    print("a")
    return 1


@shared_task
def rename_widget(widget_id, name):
    return 1