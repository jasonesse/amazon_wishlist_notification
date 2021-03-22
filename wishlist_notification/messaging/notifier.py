import jinja2
from config import TEMPLATE_FILE, MAIL_FROM, MAIL_TO
from wishlist_notification.messaging.mail import send_email
from decimal import *
import os

def notify(changes, wishlist):
    templateLoader = jinja2.FileSystemLoader(searchpath=f"{os.path.dirname(os.path.dirname(os.path.dirname(__file__)))}/wishlist_notification/messaging/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(TEMPLATE_FILE)

    results = []
    for change in changes:
        if len(change.products) > 0:
            change.products =  (dict(sorted(change.products.items(), key=lambda item: Decimal(item[1]['price']))))
            results.append(change)

    if results:
        body = template.render(results=results, wishlist=wishlist)

        #print(body)
        send_email(sender=MAIL_FROM, 
                        to=MAIL_TO, 
                        subject=f'Amazon {wishlist.title} Update!',
                        body=body,
                        as_html=True)