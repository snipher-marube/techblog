from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from elasticsearch.exceptions import NotFoundError
from .models import Post
from .documents import PostDocument
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Post)
def update_document(sender, instance, **kwargs):
    """
    Signal handler to update Elasticsearch document when a Post is saved.
    """
    try:
        PostDocument().update(instance)
        logger.debug(f"Successfully updated Elasticsearch document for Post {instance.id}.")
    except Exception as e:
        logger.error(f"Failed to update Elasticsearch document for Post {instance.id}: {e}")

@receiver(post_delete, sender=Post)
def delete_document(sender, instance, **kwargs):
    """
    Signal handler to delete Elasticsearch document when a Post is deleted.
    """
    try:
        PostDocument().delete(id=instance.id)
        logger.debug(f"Successfully deleted Elasticsearch document for Post {instance.id}.")
    except NotFoundError:
        logger.warning(f"Elasticsearch document for Post {instance.id} not found. It may have already been deleted.")
    except Exception as e:
        logger.error(f"Failed to delete Elasticsearch document for Post {instance.id}: {e}")