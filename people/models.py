from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from sorl.thumbnail.main import DjangoThumbnail

MOBILE_DEVICE_CHOICES_OTHER = 8
MOBILE_DEVICE_CHOICES = (
    (1, 'iPhone'),
    (2, 'iPod touch'),
    (3, 'Android'),
    (4, 'Palm webOS'),
    (5, 'Windows Mobile'),
    (6, 'Blackberry'),
    (7, 'Nokia/Symbian'),
    (MOBILE_DEVICE_CHOICES_OTHER, 'Anderes'),
)

COMPUTER_OS_CHOICES = (
    (1, 'Mac OS 10.6 (Snow Leopard)'),
    (2, 'Mac OS 10.5 (Leopard)'),
    (3, 'Mac OS 10.4 (Tiger)'),
    (4, 'Windows'),
    (5, 'Linux'),
)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    # matric_no = models.CharField(verbose_name=_("matric no."), max_length=20, blank=True)
    zipcode = models.CharField(verbose_name=_("zip code"), max_length=5)
    photo = models.ImageField(verbose_name=_("photo"), upload_to="uploads/", blank=True)
    mobile_device = models.PositiveSmallIntegerField(verbose_name=_("mobile device"), choices=MOBILE_DEVICE_CHOICES, null=True)
    mobile_device_other = models.CharField(verbose_name=_("other"), max_length=100, blank=True)
    computer_os = models.PositiveSmallIntegerField(verbose_name=_("computer OS"), choices=COMPUTER_OS_CHOICES, null=True)
    
    def get_photo(self, width=64, height=64, opts=None):
        if not self.photo: return ''
        relative_source = self.photo.path.replace(settings.MEDIA_ROOT,'')[1:]
        thumb = DjangoThumbnail(relative_source=relative_source, requested_size=(width, height), opts=opts)
        return u'%s' % thumb
    
    def get_mobile_device(self):
        if self.mobile_device == MOBILE_DEVICE_CHOICES_OTHER:
            return self.mobile_device_other
        return self.get_mobile_device_display()
    
    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, **kwargs):
    profile = UserProfile.objects.get_or_create(user=kwargs['instance'])
    
post_save.connect(create_user_profile, User, True)