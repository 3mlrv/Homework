from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task
from .models import PostCategory, Post, Category

@shared_task
def info_after_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    title = post.title
    subscribers_emails = []
    
    for category in categories:
        subscribers_users = category.subscribers.all()
        for sub_user in subscribers_users:
            subscribers_emails.append(sub_user.email)
        
    html_content = render_to_string(
    'post_created_email.html',
    context={
        'text': f'{post.title}',
        'link': f'{settings.SITE_URL}/news/{pk}',
    }
)


    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_post():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(datetime_post__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'account/email/email_weekly_posts.html',
        {
            'Link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_weekly_mail():
    start_date = datetime.today() - timedelta(days=6)
    this_weeks_posts = Post.objects.filter(post_time__gt=start_date)
    for cat in Category.objects.all():
        post_list = this_weeks_posts.filter(category=cat)
        if post_list:
            subscribers = cat.subscribers.values('username', 'email')
            recipients = []
            for sub in subscribers:
                recipients.append(sub['email'])

            html_content = render_to_string(
                'daily_post.html', {
                    'link': settings.SITE_URL + 'news/',
                    'posts': post_list,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'Категория - {cat.name}',
                body="----------",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipients
            )
            msg.attach_alternative(html_content, 'text/html')
            print(cat.name, settings.DEFAULT_FROM_EMAIL, recipients)
            msg.send()
        print('рассылка произведена')
