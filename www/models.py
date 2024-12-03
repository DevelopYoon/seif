
# my_app/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager,AbstractUser#PermissionsMixin

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken as BaseOutstandingToken, BlacklistedToken as BaseBlacklistedToken
import datetime
import json


class Classification(models.Model):
    evaluation = models.CharField(max_length=50, primary_key=True) 
    riskFactor = models.CharField(max_length=50)  
      
    class Meta:
        db_table = 'tb_classification'
        managed = False  
    def __str__(self):
        return self.name
    
class Facility(models.Model):
    name = models.CharField(max_length=50)  
    co_Num = models.CharField(max_length=50,primary_key=True)  
    
    problemList = models.CharField(
        max_length=20,
        choices=[
            ( '학교', 'school'),  
            ( '제조업', 'factory'),   
            ( '공사업체', 'build'),  
            ( '관리주체', 'management'),  
        ],
        default='학교',  # 기본값 설정 (선택 사항)
    )
    startDate = models.DateField()
    endDate = models.DateField()
    location = models.CharField(max_length=50)
    detail = models.CharField(max_length=50)
    class Meta:
        db_table = 'tb_facility'
        managed = False 
    def __str__(self):
        return self.name
    
class History(models.Model):
    name = models.CharField(max_length=50, primary_key=True) 
    date = models.DateField()
    
    class Meta:
        db_table = 'tb_history'
        managed = False  
    def __str__(self):
        return self.name
    
class LawList(models.Model):
    law = models.CharField(max_length=50, primary_key=True)  
    detail = models.CharField(max_length=250)  
    class Meta:
        db_table = 'tb_lawList'
        managed = False  
    def __str__(self):
        return self.name

# 윤    
class MaintenanceList(models.Model):
    PID = models.AutoField(primary_key=True) 
    date = models.DateField() 
    place = models.CharField(max_length=50)  
    writer = models.CharField(max_length=50)
    co_Num = models.CharField(max_length=50)
    detail = models.JSONField()
    
    class Meta:
        db_table = 'tb_maintenanceList'
        managed = False
        # unique_together = ('co_Num', 'place', 'date')

    def __str__(self):
        return f"{self.co_Num} - {self.place} - {self.date} - {json.dumps(self.detail, ensure_ascii=False)}"
    
class MaintenancePic(models.Model):
    PID = models.AutoField(primary_key=True)  # 자동 증가하는 기본 키
    picture = models.CharField(max_length=270)
    maintenance = models.ForeignKey(
        MaintenanceList,
        on_delete=models.CASCADE,
        db_column='maintenance',  # 실제 데이터베이스의 외래 키 컬럼
        to_field='PID'  # ForeignKey가 참조할 필드
    )
    facilityNum = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    checkDate = models.DateField()

    class Meta:
        db_table = 'tb_maintenancePic'
        managed = False

    def __str__(self):
        return f"Picture {self.PID} for {self.maintenance.co_Num} at {self.maintenance.place} on {self.maintenance.date}"
     
    
class MaintenanceTable(models.Model):
    facilityNum = models.CharField(max_length=50) 
    PID = models.AutoField( primary_key=True)
    checkDate = models.DateField()
    writer = models.CharField(max_length=50) 
    place = models.CharField(max_length=50) 
    
   
    class Meta:
        db_table = 'tb_maintenanceTable'
        managed = False 
    def __str__(self):
        return self.name
    
class Problem(models.Model):
    co_Num = models.CharField(max_length=50)
    PID = models.AutoField(primary_key=True) 
    firstDate = models.DateField(default=datetime.date.today)
    writer = models.CharField(max_length=50)  
    place = models.CharField(max_length=50)  
    work = models.CharField(max_length=50)    
    bigCause = models.CharField(max_length=50)  
    midCause = models.CharField(max_length=50)  
    peopleList = models.CharField(max_length=50, default='평가팀명단(ex. 운석신이사 정슬일부장 이상헌선임 박정란 선임 차선호이사)')  
    detail = models.CharField(max_length=50)  
    law = models.CharField(max_length=50)  
    workstep = models.CharField(max_length=50) 
    
    class Meta:
        db_table = 'tb_problem'
        managed = False 
        
    def __str__(self):
        return f"Problem {self.PID} - {self.co_Num} - {self.place} - {self.work} - {self.writer}"
    
class RiskList(models.Model):
    accident = models.CharField(max_length=50, primary_key=True) 
    midCausse = models.CharField(max_length=50) 
    class Meta:
        db_table = 'tb_riskList'
        managed = False 
    def __str__(self):
        return self.name
    
class SafetyEducation(models.Model):
    co_Num = models.CharField(max_length=50)
    PID = models.AutoField(primary_key=True) 
    educationDate = models.DateField()
    startEducationTime = models.TimeField()
    endEducationTime = models.TimeField()
    manager = models.CharField(max_length=50) 
    place = models.CharField(max_length=50) 
    peopleListPic =models.CharField(max_length=500) 
    placePic = models.CharField(max_length=500) 
    detail =  models.CharField(max_length=50) 
    title =  models.CharField(max_length=50) 
    class Meta:
        db_table = 'tb_safetyEducation'
        managed = False 
    def __str__(self):
        return self.name
    
class Solution(models.Model):
    co_Num = models.CharField(max_length=50)
    pid = models.AutoField(primary_key=True)
    
    dangerSolutionAfter = models.CharField(max_length=500)
    dangerSolutionBefore = models.CharField(max_length=500, blank=True, null=True)  
    record = models.DateField()  
    pic_before = models.CharField(max_length=500)
    pic_after = models.CharField(max_length=500, blank=True, null=True, default="")
    place = models.CharField(max_length=50)
    workstep = models.CharField(max_length=50)
    frequency = models.IntegerField()
    strength = models.IntegerField()
    riskScore = models.IntegerField()
    writer = models.CharField(max_length=50)
    work = models.CharField(max_length=50)
    is_last = models.CharField(
        max_length=1,
        choices=[
            ('Y', 'Yes'),
            ('N', 'No'),
        ],
        default='Y',
    )

    class Meta:
        db_table = 'tb_solution'
        managed = False

    def __str__(self):
        return f"Solution {self.pid} for Problem {self.problem.PID}"
        



class AppUserManager(BaseUserManager):
    def create_user(self, user_id, email, password=None, name=None, co_Num=None, Tel=None, Department=None, **extra_fields):
        if not user_id:
            raise ValueError('The ID field must be set')
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        
        user = self.model(
            user_id=user_id,
            email=email,
            name=name,
            co_Num=co_Num,
            Tel=Tel,
            Department=Department,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, email, password=None, name=None, co_Num=None, Tel=None, Department=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            user_id,
            email,
            password,
            name=name,
            co_Num=co_Num,
            Tel=Tel,
            Department=Department,
            **extra_fields
        )

class Users(AbstractUser):
    PID = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50, unique=True)  # This will be the username field
    username = models.CharField(max_length=50)
    co_Num = models.CharField(max_length=50)
    Tel = models.CharField(max_length=50)
    Department = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True)


    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email']

    CEO_permission = models.CharField(
        max_length=1,
        choices=[
            ('Y', 'Yes'),
            ('N', 'No'),
        ],
        default='N',
    )
    safe_permission = models.CharField(
        max_length=1,
        choices=[
            ('Y', 'Yes'),
            ('N', 'No'),
        ],
        default='N',
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)  # Changed to DateTimeField
    last_login = models.DateTimeField(null=True, blank=True, default=timezone.now)  # Changed to DateTimeField
    first_name = models.CharField(max_length=150,null=True)
    last_name = models.CharField(max_length=150,null=True)   
    objects = AppUserManager()

    

    class Meta:
        db_table = 'tb_user'

    def __str__(self):
        return self.user_id

    
class OutstandingToken(models.Model):
    User = Users()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outstanding_tokens')
    created_at = models.DateTimeField(auto_now_add=True)
    # JWT 관련 필드를 직접 추가할 수 있습니다. (예: token, type 등)

    class Meta:
        db_table = 'outstandingtoken'
        verbose_name = 'Outstanding Token'
        verbose_name_plural = 'Outstanding Tokens'

class BlacklistedToken(models.Model):
    User = Users()
    token = models.CharField(max_length=255)
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    # 필요한 추가 필드를 정의할 수 있습니다.

    class Meta:
        db_table = 'blacklistedtoken'
        verbose_name = 'Blacklisted Token'
        verbose_name_plural = 'Blacklisted Tokens'

# class UserProfile(models.Model):
#     user_id = models.CharField(max_length=50)
#     profile = models.CharField(max_length=270)
#     class Meta:
#         db_table = 'user_profile_pic'
    
class UserProfile(models.Model):
    user = models.OneToOneField(
        'Users',
        on_delete=models.CASCADE,
        to_field='user_id',
        db_column='user_id',
        primary_key=True
    )
    profile = models.CharField(max_length=270)
    
    class Meta:
        db_table = 'user_profile_pic'
        
        
class manageHistory(models.Model):
    PID = models.AutoField(primary_key=True)
    object = models.CharField(max_length=50)
    co_Num = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)    
    class Meta:
        db_table = 'tb_manageHistory'
    

class UserEmailVerification(models.Model):
    PID = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20)
    auth_code = models.CharField(max_length=6) 
    class Meta:
        db_table = 'tb_user_auth'
        
        
class SolutionUser(models.Model):
    Pid = models.AutoField(primary_key=True)
    co_Num = models.CharField(max_length=50)
    leader = models.CharField(max_length=50)
    supervisor = models.CharField(max_length=50)
    safeManager = models.CharField(max_length=50)
    fieldManager = models.CharField(max_length=50)
    class Meta:
        db_table = 'tb_solutionUser'
        
        
class saveLawList(models.Model):
    PID = models.AutoField(primary_key=True)
    law = models.CharField(max_length=50)
    midCause = models.TextField()

    class Meta:
        db_table = 'tb_lawList'
        managed = False

    def __str__(self):
        return self.law
    


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='img/')  # 'img/'는 MEDIA_ROOT 내의 하위 폴더입니다.


class RiskSolutionConfirmer(models.Model):
    PID = models.AutoField(primary_key=True)
    solution_pid = models.ForeignKey(
        Solution,
        on_delete=models.CASCADE,
        db_column='solution_pid',  # 실제 데이터베이스의 외래 키 컬럼
        to_field='pid'  # ForeignKey가 참조할 필드
    )
    user_id = models.CharField(max_length=50)
    date = models.DateField()
    class Meta:
        db_table = 'tb_confirmer'