from rest_framework import serializers
from ..models.user import User
from ..utils import Util
# --
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# --
import os
from dotenv import load_dotenv
load_dotenv()
# --


class UserRegistereSerializer(serializers.ModelSerializer):
    # this is for user registration form we dont want to show this on login
    # so we specifiacly meantion it here only
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    # //object level validation for our checking as we are using our userModel
    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if (password != password2):
            raise serializers.ValidationError(
                "password and confirm password should match")
        # other validations are done automatically (via AbstractBaseUser)
        # print("custome validation success")
        # this is uneccessary for registraion so djangos create wont accept #it so we remove it after validation
        attrs.pop("password2")
        # this data then call for further validation
        return attrs

    def create(self, validated_data):
        # print("calling create")
        # return User.objects.create(**validated_data)
        # create is wrong as it just create model object
        # but we need method of User manager which do all work
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    # email is unique so as we are using semi-customization
    # we need to create extra email here so is_validate ignore unique for this field
    email = serializers.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    # make a serialized object for profile of user
    # just to fetch not create
    class Meta:
        model = User
        fields = ["name", "email"]


class UserChangePasswordSerializer(serializers.Serializer):
    # normal serializer just for updated password
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, default="", max_length=200)
    email = serializers.CharField(required=False, default="", max_length=200)
    password = serializers.CharField(required=False, default="", max_length=50,
                                     style={"input_type": "password"}, write_only=True)

    password2 = serializers.CharField(required=False, default="", max_length=50,
                                      style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["name", 'email', "password", "password2"]

    def validate_email(self, value):
        user = self.context['user']
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."})
        return value

    def validate(self, attrs):
        password = attrs.get('password', None)
        if (password):
            password2 = attrs.get('password2')
            if password != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't match")
            attrs.pop("password2")
        return attrs

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)
        # print("----------------------------------------------------")
        # print("---------------------------------", validated_data)
        # for (key, value) in validated_data.items():
        #     print(key, value)
        #     setattr(instance, key, value)
        # print("----------------------------------------------------")
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class SendPasswordResetEmailSerializer(serializers.Serializer):
    # serializer as an form dor gettting email and seding a password rest link to that email
    email = serializers.EmailField(max_length=200)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        # the emailID should be users original registered emailID
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # if user exist then we send the reset link
            # for security we need more complex link
            # encoding is used
            # we encode id of user and create token from user itself
            # this is djangos way of resetting password
            # uid and token are connected as verification is done not decode the token so at verification toekn and user with uid are matched not retrived user from token so both needed
            uid = urlsafe_base64_encode(force_bytes(user.id))
            # print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            # print('Password Reset Token', token)
            # now we make link from the encoded data.
            link = os.getenv("CLIENT") + \
                "/todo/reset-password/" + uid+'/'+token+'/'
            print('Password Reset Link', link)
            # Send Email containg instructions and link
            body = 'Click Following Link to Reset Your Password    '+link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to': user.email,
            }
            Util.sendEmail(data)
            return attrs
        else:
            # if someone give not-registered emailId
            raise serializers.ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
    # simple serializer for acting as from for new password
    password = serializers.CharField(
        max_length=100, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=100, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            # get password from form
            password = attrs.get('password')
            password2 = attrs.get('password2')
            if password != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't match")
             # get endoded data from url/parameters
            uid = self.context.get('uid')
            token = self.context.get('token')
            # decode then
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            # if not valid then raise exception
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    'Token is not Valid or Expired')
            # valid then simply update password
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            # this is more extra fail-safe
            raise serializers.ValidationError('Token is not Valid or Expired')
