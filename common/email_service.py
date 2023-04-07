from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException, NotFound

from common.constants import NO_TEMPLATE_FOUND
from common.logging import logger


def send_email(template_path, data_dict, user, email_subject):
    try:
        try:
            template = get_template(template_path)
        except Exception:
            raise NotFound(_(NO_TEMPLATE_FOUND))

        if not user.email:
            raise APIException("No email address is found for the receiver user.")

        data_dict["username"] = (
            f"{user.first_name} {user.last_name}" if user.first_name else "There"
        )
        content = template.render(data_dict)

        msg = EmailMessage(
            email_subject,
            content,
            settings.EMAIL_HOST_USER,
            to=[
                user.email,
            ],
        )
        msg.content_subtype = "html"
        msg.send()

    except Exception as e:
        logger.error("Error in sending an email: ", str(e))
