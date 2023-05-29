from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from ..serializers.user_serializer import UserRegistereSerializer,\
    UserLoginSerializer, UserProfileSerializer,\
    UserChangePasswordSerializer,\
    SendPasswordResetEmailSerializer,\
    UserPasswordResetSerializer,\
    UserUpdateSerializer
from ..renderer import UserRenderer


# //----------JWT generation------------------
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# //--------------------------------------------

# //-------------------------------------------------
# user registration
# POST "/todo/register/"


class userRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        # print("--------------register view---------")
        print("request.data", request.data)
        serialized_data = UserRegistereSerializer(data=request.data)
        # print(serialized_data)
        if (serialized_data.is_valid(raise_exception=True)):
            # if valid then save user
            user = serialized_data.save()
            token = get_tokens_for_user(user)
            serialized_data = UserProfileSerializer(user)
            content = {"message": "registered Successfully",
                       "user": serialized_data.data, "token": token}
            # print("------------registered Successfully")
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            # print("------------registration Failed")
            content = {"errors": serialized_data.errors}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request, format=None):
    #     context = {"message": "registered Successfully"}
    #     return Response(context)


# //-------------------------------------------------
# user login
# POST "/todo/login/"

class userLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        # print("--------------login view---------")
        serialized_data = UserLoginSerializer(data=request.data)

        if (serialized_data.is_valid(raise_exception=True)):
            email = serialized_data.data.get("email")
            password = serialized_data.data.get("password")
            # print("----", email, "---", password)
            # the authenticate fun check login credential and give us result
            user = authenticate(email=email, password=password)
            # print("---", user)
            if user is not None:
                token = get_tokens_for_user(user)
                serialized_data = UserProfileSerializer(user)
                content = {"message": "login Successfully",
                           "user": serialized_data.data, "token": token}
                # content = {"message": "login Successfully",
                #            "user": serialized_data.data, }
                # print("------------login Successfully")
                res = Response(content, status=status.HTTP_200_OK)
                # res.set_cookie("access_token", token["access"])
                # res.set_cookie("refresh_token", token["refresh"])
                return res
            else:
                # print("------------login Failed because of wrong credentials")
                content = {"errors": {
                    "non_field_errors": "email or password is not valid"}}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("------------login Failed because of invalid data")
            content = {"errors": serialized_data.errors}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

# //-------------------------------------------------
# user profile
# GET "/todo/profile/"


class userProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    # this view just to check authentication via JWT and return user whoose token is.

    def get(self, request, format=None):
        # print("--------------profile view---------")
        serialized_data = UserProfileSerializer(request.user)
        # here we dont have to validate or authenticate anything
        # as IsAuthenticated(django auto) allow only authenticated user
        # which uses token so if valid-users-token is passes get access to this view
        # so ,request.user is always gona be valid user as we come inside views via authentication
        return Response(serialized_data.data, status=status.HTTP_202_ACCEPTED)

# user data update
# POST "/todo/user-update/"
# simply update data in user


class userUpdateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def patch(self, request, format=None):
        print("req data", request.data)
        serializer = UserUpdateSerializer(request.user,
                                          data=request.data, partial=True, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serialized_data = UserProfileSerializer(request.user)
        content = {'meesage': 'user data modified Successfully',
                   "user": serialized_data.data}
        return Response(content, status=status.HTTP_200_OK)


# //---password change and reset-------------------------------------------

# user changepassword
# POST "/todo/changepassword/"
# simply update password of loged in user
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # in serializer we can pas data as attr for additional data we can pass it as context
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)


# --------------------------------------------------
# user SendPasswordResetEmail
# POST "/todo/send-send-password-reset-emai/"
# send email where to send reset email to reset password message


class SendPasswordResetEmailView(APIView):

    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link has been successfully sent to your email address. Please check your Email'}, status=status.HTTP_200_OK)

# --------------------------------------------------
# user resetpassword
# POST "/todo/send-send-password-reset-emai/"
# ckeck paras and validate them , then ret new password that comes


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)
