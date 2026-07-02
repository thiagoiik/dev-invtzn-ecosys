from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
    terms_version = serializers.CharField(max_length=50, required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['terms_version'] = self.validated_data.get('terms_version', '')
        return data
