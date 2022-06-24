from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .utils import normalize_phone
from .tasks import send_activation_sms
User = get_user_model()

# class RegistrationSerializer(serializers.Serializer):
#     nicnname = serializers.CharField(max_length=20)

class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('nickname', 'phone', 'password', 'password_confirm')

    def validate_nickname(self, nickname):
        if User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError('This nickname is already taken. Please choose another one')
        return nickname

    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        if len(phone) != 13:
            raise serializers.ValidationError('Invalid phone format')
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('Phone already exists')
        return phone

    def validate(self, attrs: dict):
        print(attrs)
        password1 = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if not any(i for i in password1 if i .isdigit()):
            raise serializers.ValidationError('Password must contain at least one digit')
        if password1 != password_confirm:
            raise serializers.ValidationError('Passwort do not match')
        return attrs

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_sms.delay(user.phone, user.activation_code)
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User not found!")
        return email

    def validate(self, data):
        request = self.context.get('request')
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(
                email = email,
                password = password,
                request = request
            )
            if not user:
                raise serializers.ValidationError("wrong credentials")
        else:
            raise serializers.ValidationError("Email and password are required!")
        data['user'] = user
        return data

class ChangePassword(serializers.Serializer):
    old_password = serializers.CharField(min_length=6, required=True)
    new_password = serializers.CharField(min_length=6, required=True)
    new_password_confirm = serializers.CharField(min_length=6, required=True)

    def validate_old_password(self, old_password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Enter valid password!")
        return old_password

    def validate(self, attrs):
        new_pass1 = attrs.get('new_password')
        new_pass2 = attrs.get('new_password_confirm')
        if new_pass1 != new_pass2:
            raise serializers.ValidationError("Password didn't match!")
        return attrs

    def set_new_password(self):
        new_pass = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_pass)
        user.save()
        