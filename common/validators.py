import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ComplexPasswordValidator:
    """
    Validate whether the password contains minimum one uppercase,
    one digit and one symbol.
    """

    def validate(self, password, user=None):
        if (
            re.search("[A-Z]", password) is None
            or re.search("[0-9]", password) is None
            or re.search("[a-z]", password) is None
            or re.search("[^A-Za-z0-9]", password) is None
        ):
            raise ValidationError(
                _("This password is not strong."),
                code="password_is_weak",
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 number, 1 uppercase "
            + "1 lowercase, 1 special character and mimimum 8 character."
        )
