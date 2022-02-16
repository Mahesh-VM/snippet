from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
from django.contrib.auth.hashers import make_password, check_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'confirm_password', 'roles', 'username')
        extra_kwargs = {
            'password': {'write_only': True, },
        }

    def validate(self, attrs):
        user_mail_id = attrs.get('email', None)
        print(attrs.get('password'), attrs.get('confirm_password'))
        if check_password(attrs.get('password'), attrs.get('confirm_password')):
            raise ValidationError({"password": "Password fields didn't match."})
        if user_mail_id:
            user_mail_exist = User.objects.filter(email=user_mail_id).exists()
            if user_mail_exist:
                raise ValidationError({"email": 'Email already in use.'})
        return attrs

    def validate_password(self, value):
        return make_password(value)
