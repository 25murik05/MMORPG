from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Comment
# from decouple import config


@receiver(post_save, sender=Comment)
def send_mail(sender, instance, created, **kwargs):
    if created:
        user = instance.post.author

        html = render_to_string(
            'messages/new_comment.html',
            {
                'user': user,
                'comment': instance,
            },
        )

        msg = EmailMultiAlternatives(
            subject=f'New response',
            from_email='murik0525@yandex.ru',
            to=[user.email]
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()
    else:
        user = instance.author

        html = render_to_string(
            'messages/update_comment.html',
            {
                'user': user,
                'comment': instance,
            },
        )

        msg = EmailMultiAlternatives(
            subject=f'Your response received',
            from_email='murik0525@yandex.ru',
            to=[user.email]
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()
