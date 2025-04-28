from rest_framework import serializers
from .models import CustomUser, OTP




class CustomLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,write_only=True)
    class Meta:
        model = CustomUser  
        fields = ['email','password']

    def validate(self, attrs):
        email   = attrs.get('email')
        password   = attrs.get('password')
        print(email,password)
        if not email or not password:
            raise serializers.ValidationError("Invalid user or password.")
        try:
            user =  CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"email":"User with this Email doest not exist!"})
        

        if user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        if user.is_active == False:
            raise serializers.ValidationError("Invalid email or password.") 
       
        attrs['user'] = user
        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True
    )
    class Meta:
        model = CustomUser
        fields = ['email','phone','username','password']
        read_only_fields = ['is_staff', 'is_active', 'user_registere_at']

        # extra_kwargs = {'password': {'write_only': True}}


    def create(self,validated):
        password = validated.pop('password')

        try:
            user = CustomUser.objects.get(email=validated['email'])
        except CustomUser.DoesNotExist:    
            user = CustomUser.objects.create_user(
                **validated
                )
            user.set_password(password)
        # Generate otps for email
        otp = OTP.objects.create(user=user).generate_otp()
              
        return user


class OTPVerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

 
    class Meta:
        model = OTP
        fields = ['email','code']
        # read_only_fields = ['user']

    # def get_email(self,obj):
    #     return obj.user.email
    
    def validate(self,attrs):
        email = attrs.get('email')
        code  = attrs.get('code')
        print(email,code)

        try:
            user =  CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"email":"User with this Email doest not exist!"})
        
        try:
            otp = OTP.objects.filter(user=user,is_verified=False).latest("created_at")
        except OTP.DoesNotExist:
            raise serializers.ValidationError({"otp":"No active OTP Found for this user"})

        if otp.is_expired():
            raise serializers.ValidationError({"otp":"OTP has Expired"})

        if otp.code != code:
            otp.count_attempt += 1
            otp.save()
            raise serializers.ValidationError({"otp":"Invalid OTP Code"})
        
        # OTP Correct
        otp.is_verified = True
        otp.save()

        # user activivation
        user.is_active = True
        user.save()


        return attrs

    
