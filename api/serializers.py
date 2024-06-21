from rest_framework import serializers
from .models import Document, UploadSession


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file', 'uploaded_at']

    def validate_file(self, value):
        if value.content_type not in ['application/pdf', 'text/plain']:
            raise serializers.ValidationError("Only PDF and TXT files are allowed.")
        if value.size > 1024 * 1024 * 5:  # Limit to 5MB
            raise serializers.ValidationError("File size should be less than 5MB.")
        return value


class UploadSessionSerializer(serializers.ModelSerializer):
    files = serializers.ListField(child=serializers.FileField(), allow_empty=False)

    class Meta:
        model = UploadSession
        fields = ['id', 'prompt', 'files', 'uploaded_at']

    def validate_files(self, value):
        for file in value:
            if file.content_type not in ['application/pdf', 'text/plain']:
                raise serializers.ValidationError("Only PDF and TXT files are allowed.")
            if file.size > 1024 * 1024 * 5:  # Limit to 5MB per file
                raise serializers.ValidationError(
                    "Each file size should be less than 5MB."
                )
        return value
