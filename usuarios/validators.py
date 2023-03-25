import re
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

SALT = 'DLZjTiZxI1OE6pfFd9xVZwaaINK34JTF6BQdzb6bAPFFgUDgBneNiBwq6Oxs1upwe3MEr5R13pt3QFEbsuaPHDTroxsEGlIDyPBRhJd6jJTMg'


class NumberValidator:

    def validate(self, password, user=None):
        if not re.findall("\d", password):
            raise ValidationError(
                _("La contraseña debe tener mínimamente un número, 0-9."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe tener mínimamente un número, 0-9."
        )


class UppercaseValidator:
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una mayúscula, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe contener al menos una mayúscula, A-Z."
        )


class LowercaseValidator:
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos 1 minúscula, a-z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe contener al menos 1 minúscula, a-z."
        )


class SymbolValidator:
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("La contraseña debe contener un carácter especial: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe contener un carácter especial: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )
