import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

from model_utils.models import TimeStampedModel

from cookie_consent.cache import delete_cache


COOKIE_NAME_RE = re.compile(r'^[-_a-zA-Z0-9]+$')
validate_cookie_name = RegexValidator(
    COOKIE_NAME_RE,
    _(u"Enter a valid 'varname' consisting of letters, numbers"
      ", underscores or hyphens."),
    'invalid')


class DeleteAndSaveMixin:
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        delete_cache()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        delete_cache()


class CookieCategory(DeleteAndSaveMixin, TimeStampedModel):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True, null=True)
    ordering = models.IntegerField(_('Ordering'), default=0)

    class Meta:
        verbose_name = _('Cookie Category')
        verbose_name_plural = _('Cookie Categories')
        ordering = ['ordering']

    def __str__(self):
        return self.name


class CookieGroup(DeleteAndSaveMixin, TimeStampedModel):
    cookiecategory = models.ForeignKey(CookieCategory, verbose_name=CookieCategory._meta.verbose_name, on_delete=models.CASCADE)
    varname = models.CharField(
        _('Variable name'),
        max_length=32,
        validators=[validate_cookie_name])
    name = models.CharField(_('Name'), max_length=100, blank=True)
    description = models.TextField(_('Description'), blank=True)
    is_required = models.BooleanField(
        _('Is required'),
        help_text=_('Are cookies in this group required.'),
        default=False)
    is_deletable = models.BooleanField(
        _('Is deletable?'),
        help_text=_('Can cookies in this group be deleted.'),
        default=True)
    ordering = models.IntegerField(_('Ordering'), default=0)

    class Meta:
        verbose_name = _('Cookie Group')
        verbose_name_plural = _('Cookie Groups')
        ordering = ['ordering']

    def __str__(self):
        return self.name

    def get_version(self):
        try:
            return str(self.cookie_set.all()[0].get_version())
        except IndexError:
            return ""


class Cookie(DeleteAndSaveMixin, TimeStampedModel):
    cookiegroup = models.ForeignKey(
        CookieGroup,
        verbose_name=CookieGroup._meta.verbose_name,
        on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=250)
    description = models.TextField(_('Description'), blank=True)
    path = models.TextField(_('Path'), blank=True, default="/")
    domain = models.CharField(_('Domain'), max_length=250, blank=True)

    class Meta:
        verbose_name = _('Cookie')
        verbose_name_plural = _('Cookies')
        ordering = ['-created']

    def __str__(self):
        return "%s %s%s" % (self.name, self.domain, self.path)

    @property
    def varname(self):
        return "%s=%s:%s" % (self.cookiegroup.varname, self.name, self.domain)

    def get_version(self):
        return self.created.isoformat()


ACTION_ACCEPTED = 1
ACTION_DECLINED = -1
ACTION_CHOICES = (
    (ACTION_DECLINED, _('Declined')),
    (ACTION_ACCEPTED, _('Accepted')),
)


class UserCookieConsent(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    action = models.IntegerField(_('Action'), choices=ACTION_CHOICES)
    cookiegroup = models.ForeignKey(
        CookieGroup,
        verbose_name=CookieGroup._meta.verbose_name,
        on_delete=models.CASCADE)
    version = models.CharField(_('Version'), max_length=32)

    def __str__(self):
        return "%s %s" % (self.cookiegroup.name, self.version)

    class Meta:
        verbose_name = _('User cookie consent')
        verbose_name_plural = _('User cookie consents')
        ordering = ['-created']
        unique_together = ['user', 'cookiegroup']
