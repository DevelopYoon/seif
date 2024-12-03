
from rest_framework import serializers
# from django.contrib.auth import authenticate
from .models import *
from typing import Optional
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth.hashers import make_password
from django.conf import settings
from drf_spectacular.utils import extend_schema_field

class TbmanageHistory(serializers.ModelSerializer):
    class Meta:
        model = manageHistory
        fields ='__all__'

class TbClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields ='__all__'

class TbFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'

class TbHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'

class TbLawListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawList
        fields = '__all__'

class TbMaintenanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceList
        fields ='__all__'

class TbMaintenanceTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceTable
        fields ='__all__'
class TbProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields ='__all__'

class TbRiskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskList
        fields = '__all__'

class TbSafetyEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyEducation
        fields = '__all__'
        extra_kwargs = {
            'PID': {'read_only': True},
        }

class TbSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = '__all__'

class TbUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields ='__all__'




class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields =['user_id','password','username','co_Num','Tel','Department','email']

    def create(self, validated_data):
        user = Users(
            user_id=validated_data['user_id'],
            email=validated_data['email'],
            username=validated_data.get('username'),
            co_Num=validated_data.get('co_Num'),
            Tel=validated_data.get('Tel'),
            Department=validated_data.get('Department')
        )
        user.set_password(validated_data['password'])  # 비밀번호 해싱
        user.save()
        return user
    # def create(self, validated_data):
    #     validated_data['password'] = make_password(validated_data['password'])
    #     return super(SingupSerializer, self).create(validated_data)
    

#USER Serializer
    
class SendVerificationSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=50, required=True)
    Tel = serializers.CharField(max_length=50, required=True)
    
class CheckVerificationCodeSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=50, required=True)
    auth_code = serializers.CharField(max_length=6, required=True)
    
class ChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=50, required=True)
    auth_code = serializers.CharField(max_length=6, required=True)
    password = serializers.CharField(max_length=128)

class Userco_NumSerializer(serializers.Serializer):
    co_Num = serializers.CharField(max_length=50)   

class FacilityOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['name']

class UserMaintenanceListSerializer(serializers.Serializer):
    co_Num = serializers.CharField(max_length=50)
    place = serializers.CharField(max_length=50)

#유지관리 날짜출력관련

class UserMaintenanceListDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceList
        fields = ['date']


#유지관리 상세내용

class UserMaintenanceListDetailInputSerializer(serializers.Serializer):
    co_Num = serializers.CharField(max_length=50)
    place = serializers.CharField(max_length=50)
    date = serializers.DateField()

class UserMaintenanceListDetailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceList
        fields = ['writer','detail']


#같은 기관 사용자목록
class SameFacilityUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username','CEO_permission','safe_permission','Department','date_joined']

class string_Serializer(serializers.Serializer):
    string_data = serializers.CharField(max_length=50)  

class ReturnBoolSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=5)

class Problem_placeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['place']



class Problem_workSerializer(serializers.Serializer):
    place = serializers.CharField(max_length=50)
    co_Num = serializers.CharField(max_length=50)


class Problem_work_outputSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Solution
        fields = ['record','riskScore','is_last','writer','work','workstep']
    

class Problem_detailSerializer(serializers.Serializer):
    place = serializers.CharField(max_length=50)
    co_Num = serializers.CharField(max_length=50)
    work = serializers.CharField(max_length=50)


class Problem_detail_outputSerializer(serializers.ModelSerializer):

    bigCause = serializers.SerializerMethodField()
    midCause = serializers.SerializerMethodField()
    law = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()
    #pic
    pic_after = serializers.SerializerMethodField()
    pic_before = serializers.SerializerMethodField()
    class Meta:
        model = Solution
        fields = ['record','riskScore','is_last','writer','work','pid', 'bigCause', 'midCause', 'law', 'detail','dangerSolutionAfter','dangerSolutionBefore','pic_after','pic_before','workstep','place','co_Num','frequency','strength']

    def get_problem(self, obj):
        # obj.pid를 사용하여 Problem 객체를 조회합니다.
        try:
            return Problem.objects.get(co_Num=obj.co_Num, place=obj.place, work=obj.work)
        except Problem.DoesNotExist:
            return None
        
    @extend_schema_field(str)
    def get_bigCause(self, obj) -> Optional[Problem]:
        problem = self.get_problem(obj)
        return problem.bigCause if problem else None
    
    @extend_schema_field(str)
    def get_midCause(self, obj) -> Optional[str]:
        problem = self.get_problem(obj)
        return problem.midCause if problem else None
    
    @extend_schema_field(str)
    def get_law(self, obj) -> Optional[str]:
        problem = self.get_problem(obj)
        return problem.law if problem else None
    
    @extend_schema_field(str)
    def get_detail(self, obj) -> Optional[str]:
        problem = self.get_problem(obj)
        return problem.detail if problem else None 
      
    @extend_schema_field(str)
    def get_pic_after(self, obj) -> Optional[str]:
        if obj.pic_after:
            # Use request.build_absolute_uri to generate the full URL
            request = self.context.get('request')
            if request is not None:
                # This will generate the full URL including the domain and protocol
                return request.build_absolute_uri(obj.pic_after)
            else:
                # Fallback if request is not available
                return  obj.pic_after
        return None
    
    @extend_schema_field(str)
    def get_pic_before(self, obj) -> Optional[str]:
        if obj.pic_before:
            # Use request.build_absolute_uri to generate the full URL
            request = self.context.get('request')
            if request is not None:
                # This will generate the full URL including the domain and protocol
                return request.build_absolute_uri(obj.pic_before)
            else:
                # Fallback if request is not available
                return  obj.pic_before
        return None



class Same_Co_Num_UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = ['username','CEO_permission','safe_permission','Department','user_id']




class All_facility_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['name','co_Num']

class EducationList_Serializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyEducation
        fields = ['educationDate','manager','title','PID']

class EducationInput_Serializer(serializers.Serializer):
    PID = serializers.CharField(max_length=50)
    

class CreateSafetyEducationSerializer(serializers.ModelSerializer):
    peopleListPic = serializers.ImageField(required=False, allow_null=True)
    placePic = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = SafetyEducation
        fields = '__all__'


class User_idSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=50)         
    
    
class CreateFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['name','problemList','startDate','endDate','location','detail']


class MaintenancePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenancePic
        fields = ['PID', 'picture']
 
class UploadMaintenancePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenancePic
        fields = ['PID', 'picture', 'maintenance']     



class TwoStringSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    string_data = serializers.CharField(max_length=300)       

class UpdateMaintenanceSerializer(serializers.Serializer):
    PID = serializers.IntegerField()
    place = serializers.CharField(max_length=50)      

class UpdatePermissionSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=50)
    co_Num = serializers.CharField(max_length=50)


class CreateProblemSerializer(serializers.ModelSerializer):
    pic_after = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Solution
        fields = '__all__'
        extra_kwargs = {
            'dangerSolutionBefore': {'required': False, 'allow_blank': True},
            'pic_before': {'required': False, 'allow_blank': True},
        }

    @extend_schema_field(str)
    def get_pic_after(self, obj) -> Optional[str]:
        if obj.pic_after:
            # Use request.build_absolute_uri to generate the full URL
            request = self.context.get('request')
            if request is not None:
                # This will generate the full URL including the domain and protocol
                return request.build_absolute_uri(obj.pic_after)
            else:
                # Fallback if request is not available
                return 'http://211.237.0.230:10123'+settings.MEDIA_URL+ "prob" + obj.pic_after
        return None


class CreateProblemPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ['place','co_Num']

# class UploadUserProfileSerializer(serializers.ModelSerializer):
#     profile = serializers.ImageField(required=False, allow_null=True)
#     class Meta:
#         model = UserProfile
#         fields = '__all__'

class UploadUserProfileSerializer(serializers.ModelSerializer):
    profile = serializers.CharField(required=False, allow_null=True)  # CharField로 수정

    class Meta:
        model = UserProfile
        fields = ['profile']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('context', {}).get('user', None)
        super().__init__(*args, **kwargs)
    
    def create(self, validated_data):
        if self.user is None:
            raise ValueError("User must be provided")
        profile_instance, created = UserProfile.objects.update_or_create(
            user=self.user,
            defaults=validated_data
        )
        return profile_instance

class User_idSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=50)  

# class UserProfileSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), source='user_id')
#     class Meta:
#         model = UserProfile
#         fields = ['profile']
class UserProfileSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['user', 'profile'] 
        
    def get_profile(self, obj):
        return obj.profile if obj.profile else None
        

# class UserProfileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = UserProfile
#         fields = '__all__'
# class 
class CreateHistorySerializer(serializers.ModelSerializer):
    object = serializers.CharField(max_length=100, required=False)
    class Meta:
        model = manageHistory
        fields = ['co_Num', 'object'] 
    def create(self, validated_data):
        # Create the history entry using the validated data
        return manageHistory.objects.create(**validated_data)
 
class MaintenanceRequestSerializer(serializers.Serializer):
    facilityNum = serializers.CharField(max_length=50)
    place = serializers.CharField(max_length=50)
    checkDate = serializers.DateField()    
    
class MaintenancePlaceRequestSerializer(serializers.Serializer):
    facilityNum = serializers.CharField(max_length=50)
    place = serializers.CharField(max_length=50)    
    
    

class RiskPlaceSerializer(serializers.Serializer):
    facilityNum = serializers.CharField(max_length=50)
    place = serializers.CharField(max_length=50) 
    
class RiskPlaceWorkSerializer(serializers.Serializer):
    facilityNum = serializers.CharField(max_length=50)
    place = serializers.CharField(max_length=50) 
    work = serializers.CharField(max_length=50)
    
class EduTitleDateSerializer(serializers.Serializer):
    facilityNum = serializers.CharField(max_length=50)
    title = serializers.CharField(max_length=50)
    # work = serializers.CharField(max_length=50) 
    educationDate = serializers.DateField()     
    
class EduSerializer(serializers.Serializer):
    facilityNum = serializers.CharField(max_length=50)
    
class SolutionUserSerializer(serializers.Serializer):
    co_Num = serializers.CharField(max_length=50)
    leader = serializers.CharField(max_length=50)
    supervisor = serializers.CharField(max_length=50)
    safeManager = serializers.CharField(max_length=50)
    fieldManager = serializers.CharField(max_length=50)
    
    
class saveLawListSerializer(serializers.Serializer):
    law = serializers.CharField(max_length=50)  
    midCause = serializers.CharField()


    
class addRiskConfirmerSerializer(serializers.Serializer):
    co_Num = serializers.CharField(max_length=50)  
    place = serializers.CharField(max_length=50)
    work = serializers.CharField(max_length=50)
    date = serializers.DateField()
    user_id = serializers.CharField(max_length=50)

class riskSolutionIdSerializer(serializers.Serializer):
    solution_pid = serializers.IntegerField()


class confirmerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'user_id']