#
# WTForms-Honeypot
#
# Copyright (C) 2019 Boris Raicheff
# All rights reserved
#


from markupsafe import Markup
from wtforms.compat import string_types, text_type
from wtforms.fields import StringField
from wtforms.widgets import TextInput


class HoneypotInput(TextInput):
    """"""

    def __call__(self, field, **kwargs):
        kwargs['autocomplete'] = 'off'
        return super().__call__(field, **kwargs)


class HoneypotField(StringField):
    """"""

    widget = HoneypotInput()


class HoneypotMixin(object):
    """"""

    # https://github.com/curtis/honeypot-captcha
    # https://github.com/mixkorshun/django-antispam
    # https://github.com/mmilkin/flask_wtf_honeypot
    # https://stackoverflow.com/questions/26452716/how-to-create-a-nuclear-honeypot-to-catch-form-spammers
    # https://stackoverflow.com/questions/36227376/better-honeypot-implementation-form-anti-spam

    @property
    def is_dipped(self) -> bool:
        return any(f.data for f in self._honeypot_fields(self))

    def honeypot_tag(self, *fields, **kwargs):
        """
        Render the form's honeypot fields in one call.

        A field is considered a honeypot if it uses the
        :class:`~HoneypotInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.
        """

        return Markup('\n'.join(text_type(f(**kwargs)) for f in self._honeypot_fields(fields or self)))

    def _honeypot_fields(self, fields):
        for f in fields:
            if isinstance(f, string_types):
                f = getattr(self, f, None)
            if f is None or not isinstance(f.widget, HoneypotInput):
                continue
            yield f


# EOF
