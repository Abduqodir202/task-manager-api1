from django.db.models.signals import post_delete
from django.dispatch import receiver

from books.models import Books

import logging


@receiver(post_delete, sender=Books)
def delete_books(sender, instance, **kwargs):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='delete_books.log', filemode='a+')
    logging.info(f'delete_books {instance.title} {instance.description}')
