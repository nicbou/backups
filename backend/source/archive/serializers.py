from rest_framework import serializers

from archive.models.google_takeout import GoogleTakeoutArchive


class GoogleTakeoutArchiveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoogleTakeoutArchive
        fields = ['key', 'description', 'date_processed', 'archive_file']