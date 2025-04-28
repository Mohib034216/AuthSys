from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, OTPVerificationSerializer, CustomLoginSerializer
from .models import CustomUser, OTP
from .utils import send_simple_email

# Create your views here.


class LoginView(APIView):
    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        print(f"serilaizer check{serializer}") 
        print(f"validation serilaizer check{serializer.is_valid()}") 
        if not serializer.is_valid():
            return Response(serializer.errors)
        # serializer.is_valid(raise_exception=True)
        
        user =  serializer.validated_data['user']

        # # JWT Token for user 
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        # # JSON data Response
        return Response({
            "refresh":str(refresh_token),
            "access":access_token,
            "user_id":user.id,
            "user_email":user.email
        })



class RegisterationView(APIView):
    def post(self,request):
        data = request.data
        try:
            user = CustomUser.objects.get(email=data['email'])
            print(user)
            if user:
                return Response({"message":"Email already Registered!"})
        except CustomUser.DoesNotExist:
            
            serializer = RegisterSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()
                
                # Sending OTP via Email
                user = CustomUser.objects.get(email=data['email'])
                user_otp = OTP.objects.get(user=user)
                subject = "Your OTP Code for Verification"
                message = ("Dear User,\n\n"
                    f"Your One-Time Password (OTP) is: {user_otp.code}\n\n"
                    "Please enter this code to complete your verification.\n\n"
                    "This OTP is valid for 10 minutes.\n\n"
                    "If you did not request this, please ignore this email.\n\n"
                    "Thank you for signing up.\n")
                recipient_list = [data.get('email')]
                send_simple_email(subject, message, recipient_list)
                
                return Response({"message":"Verify Email OTP Send"})
        return Response({"message":"Some is wrong!"})


class VerifyEmail(APIView):
    def post(self,request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message":"OTP Verifies Successfully."})
        return Response(serializer.errors)
        

