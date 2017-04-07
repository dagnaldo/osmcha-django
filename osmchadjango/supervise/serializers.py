from django.core.urlresolvers import reverse

from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.fields import SerializerMethodField, HiddenField, CurrentUserDefault
from rest_framework.validators import ValidationError, UniqueTogetherValidator

from .models import AreaOfInterest


class AreaOfInterestSerializer(GeoFeatureModelSerializer):
    changesets_url = SerializerMethodField()
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = AreaOfInterest
        geo_field = 'geometry'
        exclude = ('user',)
        validators = [
            UniqueTogetherValidator(
                queryset=AreaOfInterest.objects.all(),
                fields=('name', 'user')
                )
            ]

    def get_changesets_url(self, obj):
        return reverse('supervise:aoi-list-changesets', args=[obj.id])

    def validate(self, data):
        if data.get('filters') is None and data.get('geometry') is None:
            raise ValidationError(
                'Set a value to the filters field or to the geometry to be able to save the AoI'
                )
        return data
