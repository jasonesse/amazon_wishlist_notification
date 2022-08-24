import jinja2
from config import TEMPLATE_FILE, MAIL_FROM, MAIL_TO
from wishlist_notification.messaging.mail import send_email
from wishlist_notification.messaging.send_gmail import send_gmail_message
from decimal import *
import os

def notify(changes, wishlist, send=False):
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
        if send:
            send_gmail_message(message=body)
            # send_email(sender=MAIL_FROM, 
            #                 to=MAIL_TO, 
            #                 subject=f'Amazon {wishlist.title} Update!',
            #                 body=body,
            #                 as_html=True)
        else:
            with open('C:/Users/jason/OneDrive/Desktop/PRICE_CHANGE.html', 'w') as f:
                f.write(body)
