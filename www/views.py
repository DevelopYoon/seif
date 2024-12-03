# my_app/views.py
#기관번호용
import random
import string
from django.core.files.storage import default_storage

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import OpenApiResponse, extend_schema

from django.contrib.auth import authenticate, login as auth_login

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken

from django.http import HttpResponse
from .maintance_date import *
from .maintance_place import *
from .maintenance_facility import *
from .risk_date import *
from django.core.mail import EmailMessage
from .create_edu import *


# import os
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# from django.core.files.storage import FileSystemStorage
# from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework_simplejwt.settings import api_settings
# from django.contrib.auth.hashers import check_password
#test할게용
def test_login(request):
    
    return render(request,'test.html')

def pro(request):
    
    return render(request,'profiletest.html')


def generate_unique_code(length=6):
        # 기관번호 난수돌리기 
        while True:
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            if not Facility.objects.filter(co_Num=code).exists():
                return code

@csrf_exempt
def table_info(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]
        return JsonResponse({'tables': tables})
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=400)
    



@extend_schema(
    summary="대분류 위험요인",
    description="대분류 위험요인,중분류 위험요인",
    responses=TbClassificationSerializer(many=True),
)
class TbClassificationListView(generics.ListAPIView):
    queryset = Classification.objects.all()
    serializer_class = TbClassificationSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint

    
@extend_schema(
    summary="기관/시설물",
    description="기관에 대한 상세정보입니다.",
    responses=TbFacilitySerializer(many=True),
)
class TbFacilityListView(generics.ListAPIView):
    queryset = Facility.objects.all()
    serializer_class = TbFacilitySerializer
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint
   

@extend_schema(
    summary="확인기록",
    description="대처방안에 대한 확인기록입니다.",
    responses=TbHistorySerializer(many=True),
)
class TbHistoryListView(generics.ListAPIView):
    queryset = History.objects.all()
    serializer_class = TbHistorySerializer
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint

 
@extend_schema(
    summary="관련법목록",
    description="관련법 목록입니다.",
    responses=TbLawListSerializer(many=True),
)
class TbLawListListView(generics.ListAPIView):
    queryset = LawList.objects.all()
    serializer_class = TbLawListSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint

    
@extend_schema(
    summary="유지관리 목록",
    description="유지관리표에 대한 유지관리 사항데이터",
    responses=TbMaintenanceListSerializer(many=True),
)
class TbMaintenanceListListView(generics.ListAPIView):
    queryset = MaintenanceList.objects.all()
    serializer_class = TbMaintenanceListSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint


   
@extend_schema(
    summary="유지관리표",
    description="시설물에 대한 여러개의 유지관리표",
    responses=TbMaintenanceTableSerializer(many=True),
)
class TbMaintenanceTableListView(generics.ListAPIView):
    queryset = MaintenanceTable.objects.all()
    serializer_class = TbMaintenanceTableSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint

   
@extend_schema(
    summary="위험성 평가표",
    description="시설물에 대한 위험성 평가표입니다.",
    responses=TbProblemSerializer(many=True),
)
class TbProblemListView(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = TbProblemSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint


   
@extend_schema(
    summary="위험성 목록",
    description="위험성평가표 작성시 사고내용인 상세요인에 관한 목록들입니다.ex) 화학물질적 요인 -> 3.6 자연발화(화재,폭발)->여기부분",
    responses=TbRiskListSerializer(many=True),
)
class TbRiskListListView(generics.ListAPIView):
    queryset = RiskList.objects.all()
    serializer_class = TbRiskListSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint
 
@extend_schema(
    summary="안전교육",
    description="기관마다 안전교육받은 기록데이터",
    responses=TbSafetyEducationSerializer(many=True),
)
class TbSafetyEducationListView(generics.ListAPIView):
    queryset = SafetyEducation.objects.all()
    serializer_class = TbSafetyEducationSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint


   
@extend_schema(
    summary="대처방안",
    description="기관별 위험성평가표 대처방안 데이터목록",
    responses=TbSolutionSerializer(many=True),
)
class TbSolutionListView(generics.ListAPIView):
    queryset = Solution.objects.all()
    serializer_class = TbSolutionSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint

   
@extend_schema(
    summary="사용자",
    description="사용자정보데이터",
    responses=TbUserSerializer(many=True),
)
class TbUserListView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = TbUserSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint


@extend_schema(
    summary="회원가입_1",
    description="기관번호와 아이디 비밀번호 입력",
    request=SignupSerializer,
    responses={201: SignupSerializer}
)
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(SignupSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@extend_schema(
    summary="로그인",
    description="아이디와 비밀번호를 입력하여 로그인합니다. 로그인 성공 시 JWT를 반환합니다.",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description="로그인 성공 및 JWT 반환",
            response=LoginSerializer  # You might want to use a different serializer for successful responses
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=LoginSerializer
        ),
    }
)
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            password = serializer.validated_data['password']
            user = authenticate(user_id=user_id, password=password)
            try:
                
                if user:
                    # Generate JWT token
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    refresh_token = str(refresh)
                    CEO_token = user.CEO_permission 
                    safe_token = user.safe_permission
                    co_Num = user.co_Num
                    username = user.username
                    email = user.email
                    Tel = user.Tel
                    Department = user.Department
                    return Response({
                        "message": "로그인 성공",
                        "access": access_token,
                        "refresh": refresh_token,
                        "CEO_permission" : CEO_token,
                        "safe_permission" : safe_token,
                        "co_Num" : co_Num,
                        "username" : username,
                        "email" : email,
                        "Tel" : Tel,
                        "Department" : Department,

                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "로그인 실패. 잘못된 user_id 또는 비밀번호입니다."}, status=status.HTTP_400_BAD_REQUEST)
                
            except Users.DoesNotExist:
                return Response({"error": "로그인 실패. 잘못된 user_id 또는 비밀번호입니다.",
                                 'password':password}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@extend_schema(
    summary="비밀번호 변경시 이메일 인증",
    description="아이디와 전화번호 받아서 인증 메일 전송",
    request=SendVerificationSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=SendVerificationSerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=SendVerificationSerializer
        ),
    }
)
class SendVerificationView(APIView):
    def post(self, request):
        # 시리얼라이저로 요청 데이터 검증
        serializer = SendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['user_id']
        tel = serializer.validated_data['Tel']

        try:
            # user_id와 Tel이 모두 일치하는 사용자를 찾음
            user = Users.objects.get(user_id=uid, Tel=tel)

            # 인증 코드 생성 (랜덤 문자열 생성)
            verification_code = generate_unique_code()

            # 처음 인증인 경우와 아닌 경우 구분
            if (UserEmailVerification.objects.filter(user_id=uid).exists()):
                userVerification = UserEmailVerification.objects.get(user_id=uid)
                userVerification.auth_code = verification_code
                userVerification.save()
            else:
                userVerification = UserEmailVerification(user_id=uid, auth_code=verification_code)
                userVerification.save()

            # 이메일 내용 정의
            subject = "비밀번호 변경을 위한 이메일 인증 코드"
            message = f"안녕하세요, {user.username}님!\n\n" \
                      f"세잎 비밀번호 변경을 위한 인증코드는\n\n"\
                      f"{verification_code}\n\n"\
                      f"입니다.\n\n"\
                      f"안전하고 행복한 하루 되세요!"

            #이메일 전송
            email = EmailMessage(
                subject = '[세잎] 비밀번호 변경 인증코드 안내',
                body = message,
                to = [user.email],
                from_email= "Seif@google.com",
                headers={'From': 'Seif@google.com'}  
            )
            result = email.send()

            return Response({'message': '인증 메일이 발송되었습니다.'}, status=status.HTTP_200_OK)

        except Users.DoesNotExist:
            raise Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # 그 외 에러 처리
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



@extend_schema(
    summary="인증 코드 확인",
    description="인증 코드 확인",
    request=CheckVerificationCodeSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=CheckVerificationCodeSerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=CheckVerificationCodeSerializer
        ),
    }
)
class VerificaitonCodeView(APIView):
    def post(self, request):
        # 시리얼라이저로 요청 데이터 검증
        serializer = CheckVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['user_id']
        auth_code = serializer.validated_data['auth_code']

        try:
            # user_id와 auth_code 모두 일치하는 사용자를 찾음
            user = UserEmailVerification.objects.get(user_id=uid, auth_code=auth_code)

            return Response({'message': '인증에 성공하였습니다'}, status=status.HTTP_200_OK)

        except Users.DoesNotExist:
            raise Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # 그 외 에러 처리
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



@extend_schema(
    summary="비밀번호 변경",
    description="비밀번호 변경",
    request=ChangePasswordSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=ChangePasswordSerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=ChangePasswordSerializer
        ),
    }
)
class PasswordChangeView(APIView):
    def post(self, request):
        # 시리얼라이저로 요청 데이터 검증
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['user_id']
        auth_code = serializer.validated_data['auth_code']
        new_password = serializer.validated_data['password']

        try:
            # user_id와 auth_code 모두 일치하는 사용자를 찾음
            # auth_code 없으면 user_id와 API만 알아도 비밀번호 변경 가능해짐
            userVerification = UserEmailVerification.objects.get(user_id=uid, auth_code=auth_code)
            user = Users.objects.get(user_id=userVerification.user_id)
            user.set_password(new_password) 
            user.save()

            return Response({'message': '비밀번호가 변경되었습니다'}, status=status.HTTP_200_OK)

        except Users.DoesNotExist:
            raise Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # 그 외 에러 처리
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="사용자유지관리표 장소목록",
    description="기관번호 입력시 해당 사용자의 해당장소 유지관리표목록 반환 || ex: 2",
    request=Userco_NumSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=TbMaintenanceTableSerializer(many=True)  # You might want to use a different serializer for successful responses
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=TbMaintenanceTableSerializer
        ),
    }
)
class UserMaintenanceTableView(APIView):
    authentication_classes = [JWTAuthentication]
    
    
    def post(self, request, *args, **kwargs):
        input_serializer = Userco_NumSerializer(data=request.data)
        if input_serializer.is_valid():
            co_num = input_serializer.validated_data['co_Num']
            # place = input_serializer.validated_data['place']
            
            
           
            # Query the database for matching records
            queryset = MaintenanceTable.objects.filter(facilityNum=co_num)#, place=place
            if queryset.exists():
                # Serialize the queryset for the response
                output_serializer = TbMaintenanceTableSerializer(queryset, many=True)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No matching records found"}, status=status.HTTP_404_NOT_FOUND)
        
       
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
@extend_schema(
    summary="메인페이지",
    description="기관번호 입력 || ex: 2",
    request=Userco_NumSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=FacilityOutputSerializer  # You might want to use a different serializer for successful responses
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=Userco_NumSerializer
        ),
    }
)
class UserFacilityView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Validate input data
        input_serializer = Userco_NumSerializer(data=request.data)
        if input_serializer.is_valid():
            co_Num = input_serializer.validated_data['co_Num']
            
            # Query the database for the facility with the given PID
            try:
                queryset = Facility.objects.get(co_Num=co_Num)
                # Serialize the single facility record for the response
                output_serializer = FacilityOutputSerializer(queryset)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            except Facility.DoesNotExist:
                return Response({"error": "No matching records found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#날짜별 항목
@extend_schema(
    summary="유지관리표 내용",
    description="기관번호,장소 입력하면 날짜반환",
    request=UserMaintenanceListSerializer,#입력받는곳
    responses={
        200: OpenApiResponse(
            description="성공",
            response=UserMaintenanceListDateSerializer(many=True)  # 출력양식넣는곳
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=UserMaintenanceListDateSerializer # 에러나는곳
        ),
    }
)
class UserMaintenanceListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        input_serializer = UserMaintenanceListSerializer(data=request.data)#입력받는곳양식
        if input_serializer.is_valid():
            co_Num = input_serializer.validated_data['co_Num']
            place = input_serializer.validated_data['place']
            
            
            queryset = MaintenanceList.objects.filter(co_Num=co_Num, place=place)#비교데이터테이블
            
            if queryset.exists():
                # Serialize the queryset for the response
                output_serializer = UserMaintenanceListDateSerializer(queryset, many=True)#츌력받는곳의 양식
                
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No matching records found"}, status=status.HTTP_404_NOT_FOUND)
        
       
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#날짜별 항목의 상세 내용
@extend_schema(
    summary="유지관리표 상세 내용",
    description="기관번호,장소,기간 입력하면 내용,작성자 반환",
    request=UserMaintenanceListDetailInputSerializer,#입력받는곳
    responses={
        200: OpenApiResponse(
            description="성공",
            response=UserMaintenanceListDetailOutputSerializer  # 출력양식넣는곳
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=UserMaintenanceListDetailOutputSerializer # 에러나는곳
        ),
    }
)
class UserMaintenanceListDetailView(APIView):

    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        input_serializer = UserMaintenanceListDetailInputSerializer(data=request.data)#입력받는곳양식
        if input_serializer.is_valid():
            co_Num = input_serializer.validated_data['co_Num']
            place = input_serializer.validated_data['place']
            date= input_serializer.validated_data['date']
              
            try:
                queryset =MaintenanceList.objects.filter(co_Num=co_Num, place=place,date=date)
                # Serialize the single facility record for the response
                output_serializer = UserMaintenanceListDetailOutputSerializer(queryset.first())
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            except MaintenanceList.DoesNotExist:
                return Response({"error": "No matching records found"}, status=status.HTTP_404_NOT_FOUND)
       
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#사용자 기관 정보

@extend_schema(
    summary="사용자 기관 상세 내용",
    description="기관번호 입력하면 작성자의 기관정보 반환",
    request=Userco_NumSerializer,#입력받는곳
    responses={
        200: OpenApiResponse(
            description="성공",
            response=TbFacilitySerializer  # 출력양식넣는곳
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=TbFacilitySerializer # 에러나는곳
        ),
    }
)
class UserFacilityInfoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        input_serializer = Userco_NumSerializer(data=request.data)#입력받는곳양식
        if input_serializer.is_valid():
            co_Num = input_serializer.validated_data['co_Num']
            try:
                queryset = Facility.objects.get(co_Num=co_Num)
                # Serialize the single facility record for the response
                output_serializer = TbFacilitySerializer(queryset)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            except Facility.DoesNotExist:
                return Response({"error": "No matching records found"}, status=status.HTTP_404_NOT_FOUND)
       
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#현재사용자목록

@extend_schema(
    summary="현재사용자목록",
    description="기관번호 입력하면 현재사용자목록 반환",
    request=Userco_NumSerializer,#입력받는곳
    responses={
        200: OpenApiResponse(
            description="성공",
            response=SameFacilityUserSerializer  # 출력양식넣는곳
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=SameFacilityUserSerializer # 에러나는곳
        ),
    }
)
class FacilityUserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        input_serializer = Userco_NumSerializer(data=request.data)#입력받는곳양식
        if input_serializer.is_valid():
            co_Num = input_serializer.validated_data['co_Num']
            
            queryset = Users.objects.filter(co_Num=co_Num) #비교데이터테이블
            
            if queryset.exists():
                # Serialize the queryset for the response
                output_serializer = SameFacilityUserSerializer(queryset, many=True)#츌력받는곳의 양식
                
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No matching records found"}, status=status.HTTP_404_NOT_FOUND)
        
       
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@extend_schema(
    summary="user_id",
    description="이름 중복여부 확인",
    request=string_Serializer,
    responses={
        200: OpenApiResponse(description=" y 성공"),
        400: OpenApiResponse(description=" n 실패"),
    }
)
class user_id_boolView(APIView):

    permission_classes = [AllowAny]
    
    def post(self, request):
        input_serializer = string_Serializer(data=request.data)#입력받는곳양식
        if input_serializer.is_valid():
            user_id = input_serializer.validated_data['string_data']
            queryset =Users.objects.filter(user_id=user_id)
              
            if queryset.exists():
                
                
                return Response("y", status=status.HTTP_200_OK)
            else:
                return Response("n",  status=status.HTTP_200_OK)
       
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema(
    summary="email",
    description="이메일 중복여부 확인",
    request=string_Serializer,
    responses={
        200: OpenApiResponse(description=" y 성공"),
        400: OpenApiResponse(description=" n 실패"),
    }
)
class email_boolView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        input_serializer = string_Serializer(data=request.data)#입력받는곳양식
        if input_serializer.is_valid():
            email = input_serializer.validated_data['string_data']
            queryset =Users.objects.filter(email=email)
              
            if queryset.exists():
                
                
                return Response("y", status=status.HTTP_200_OK)
            else:
                return Response("n",  status=status.HTTP_200_OK)
       
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema(
    summary="co_Num",
    description="기관번호 중복여부 확인",
    request=string_Serializer,
    responses={
        200: OpenApiResponse(description=" y 성공"),
        400: OpenApiResponse(description=" n 실패"),
    }
)
class Co_Num_boolView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        input_serializer = string_Serializer(data=request.data)#입력받는곳양식
        if input_serializer.is_valid():
            co_Num = input_serializer.validated_data['string_data']
            queryset =Facility.objects.filter(co_Num=co_Num)
              
            if queryset.exists():
                
                
                return Response("n", status=status.HTTP_200_OK)
            else:
                return Response("y",  status=status.HTTP_200_OK)
       
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#위험성평가표장소조회
@extend_schema(
    summary="co_Num",
    description="기관번호로 장소 조회",
    request=Userco_NumSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=Problem_placeSerializer(many=True)
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
        404: OpenApiResponse(
            description="찾을 수 없음",
            response=None
        ),
    }
)
class Problem_placeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        input_serializer = Userco_NumSerializer(data=request.data)  # 입력받는 양식
        if input_serializer.is_valid():
            co_Num = input_serializer.validated_data['co_Num']
            
            # 비즈니스 로직에 맞는 필터링
            queryset = Problem.objects.filter(co_Num=co_Num)
            
            if queryset.exists():
                # Serialize the queryset for the response
                output_serializer = Problem_placeSerializer(queryset, many=True)
                #중복제거
                seen = set()
                unique_data = []
                for item in output_serializer.data:
                    place = item['place']
                    if place not in seen:
                        seen.add(place)
                        unique_data.append({'place': place})


                return Response(unique_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No matching records found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#위험성평가표작업명조회
@extend_schema(
    summary="위험성평가표 작업명 목록조회",
    description="기관번호 중복여부 확인",
    request=Problem_workSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=Problem_work_outputSerializer(many=True)
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
        404: OpenApiResponse(
            description="찾을 수 없음",
            response=None
        ),
    }
)
class Problem_workView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        input_serializer = Problem_workSerializer(data=request.data)  # 입력받는 양식
        if input_serializer.is_valid():
            co_Num = input_serializer.validated_data['co_Num']
            place = input_serializer.validated_data['place']
            # 비즈니스 로직에 맞는 필터링
            queryset = Solution.objects.filter(co_Num = co_Num,place = place,is_last='Y')
            
            if queryset.exists():
                # Serialize the queryset for the response
                output_serializer = Problem_work_outputSerializer(queryset, many=True)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No Problem"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#위험성평가표상세조회
@extend_schema(
    summary="co_Num",
    description="기관번호 중복여부 확인",
    request=Problem_detailSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=Problem_detail_outputSerializer(many=True)
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
        404: OpenApiResponse(
            description="찾을 수 없음",
            response=None
        ),
    }
)
class Problem_detailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        input_serializer = Problem_detailSerializer(data=request.data)  # 입력받는 양식
        if input_serializer.is_valid():
            co_Num = input_serializer.validated_data['co_Num']
            place = input_serializer.validated_data['place']
            work = input_serializer.validated_data['work']

            # 비즈니스 로직에 맞는 필터링
            queryset = Solution.objects.filter(co_Num = co_Num,place = place,is_last='Y',work=work)
            
            if queryset.exists():
                # Serialize the queryset for the response
                output_serializer = Problem_detail_outputSerializer(queryset.first())
                
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No matching records found"}, status=status.HTTP_404_NOT_FOUND)
        
        

        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#사용자목록조회
@extend_schema(
    summary="사용자목록조회",
    description="같은 기관번호의 사용자 목록및 권한반환",
    request=string_Serializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=Same_Co_Num_UserSerializer(many=True)
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
        404: OpenApiResponse(
            description="찾을 수 없음",
            response=None
        ),
    }
)
class Same_Co_Num_UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        input_serializer = string_Serializer(data=request.data)  # 입력받는 양식
        if input_serializer.is_valid():
            co_Num = input_serializer.validated_data['string_data']
            
            # 비즈니스 로직에 맞는 필터링
            queryset = Users.objects.filter(co_Num = co_Num)
            
            if queryset.exists():
                # Serialize the queryset for the response
                output_serializer = Same_Co_Num_UserSerializer(queryset, many=True)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No matching records found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
@extend_schema(
    summary="관리자 기관/시설물 조회",
    description="전체 모든 기관목록입니다.",
    responses=All_facility_Serializer(many=True),
)
class All_FacilityListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Facility.objects.all()
    serializer_class = All_facility_Serializer
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint



#안전교육목록조회
@extend_schema(
    summary="안전교육이수 목록조회",
    description="안전교육목록조회",
    request=Userco_NumSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=EducationList_Serializer(many=True)
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
        404: OpenApiResponse(
            description="찾을 수 없음",
            response=None
        ),
    }
)
class SafetyEducation_ListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        input_serializer = Userco_NumSerializer(data=request.data)  # 입력받는 양식
        if input_serializer.is_valid():
            co_Num = input_serializer.validated_data['co_Num']
            
            # 비즈니스 로직에 맞는 필터링
            queryset = SafetyEducation.objects.filter(co_Num = co_Num)
            
            if queryset.exists():
                # Serialize the queryset for the response
                output_serializer = EducationList_Serializer(queryset, many=True)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No list is ok"},status=status.HTTP_200_OK)
        
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#안전교육 목록상세 조회
@extend_schema(
    summary="안전교육이수 상세조회",
    description="안전교육상세조회",
    request=EducationInput_Serializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=TbSafetyEducationSerializer(many=True)
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
        404: OpenApiResponse(
            description="찾을 수 없음",
            response=None
        ),
    }
)
class EducationDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        input_serializer = EducationInput_Serializer(data=request.data)  # 입력받는 양식
        if input_serializer.is_valid():
            PID = input_serializer.validated_data['PID']
            
            # 비즈니스 로직에 맞는 필터링
            queryset = SafetyEducation.objects.filter(PID = PID)
            
            if queryset.exists():
                # Serialize the queryset for the response
                output_serializer = TbSafetyEducationSerializer(queryset.first())
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No matching records found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@extend_schema(
    summary="개인정보변경",
    description="title : [email, Tel, username, Department,password] string_data : [바꿀내용]",
    request=TwoStringSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=TwoStringSerializer  # 성공 응답 시의 직렬화된 데이터 구조를 지정합니다.
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
        404: OpenApiResponse(
            description="찾을 수 없음",
            response=None
        ),
    }
)
class UpdateUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # 인증 없이 접근을 허용합니다. 필요에 따라 수정할 수 있습니다.

    def patch(self, request, *args, **kwargs):  # HTTP 메서드를 PATCH로 수정
        # Authorization 헤더에서 JWT 토큰 추출
        auth_header = request.headers.get('Authorization')
            
        if not auth_header:
            return Response({"error": "JWT 토큰이 제공되지 않았거나 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 토큰 추출 (Bearer 접두어가 있는 경우)
        token_str = auth_header.split(' ')[1] if ' ' in auth_header else auth_header

        # JWT 토큰에서 user_id 추출
        try:
            access_token = AccessToken(token_str)
            user_id = access_token.payload.get('user_id')  # payload에서 user_id를 가져옵니다.
            
        except Exception as e:
            return Response({"error": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 입력 데이터 유효성 검사
        serializer = TwoStringSerializer(data=request.data)
        if serializer.is_valid():
            string_data = serializer.validated_data['string_data']
            title = serializer.validated_data['title']
            if title  in ['Tel', 'email', 'username', 'password', 'Department']:
                # user_id로 사용자 찾기
                try:
                    user = Users.objects.get(user_id=user_id)
                except Users.DoesNotExist:
                    return Response({"error": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

                # 필드 업데이트
                if hasattr(user, title):

                    if title == 'password':
                        user.set_password(string_data)
                    else : 
                        setattr(user, title, string_data)
                    
                    user.save()
                    return Response({"message": "데이터가 성공적으로 업데이트되었습니다."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": f"필드 {title}가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
            else : 
                return Response({"error": f"필드 {title}가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(
    summary="유지관리표",
    description="유지관리표 고유번호 : PID , 바꿀 장소 : place",
    request=UpdateMaintenanceSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=None  # 성공 응답 시의 직렬화된 데이터 구조를 지정합니다.
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
        404: OpenApiResponse(
            description="찾을 수 없음",
            response=None
        ),
    }
)
class UpdateMaintenanceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    def patch(self, request, *args, **kwargs):
        serializer = UpdateMaintenanceSerializer(data=request.data)
        
        if serializer.is_valid():
                replace = serializer.validated_data['place']
                PID = serializer.validated_data['PID']
                
                # user_id로 사용자 찾기
                try:
                    MaintenanceField = MaintenanceTable.objects.get(PID=PID)
                    MaintenanceTable.objects.filter(PID=PID).update(place=replace)
                except MaintenanceTable.DoesNotExist:
                    return Response({"error": "장소를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

                MaintenanceList.objects.filter(place=MaintenanceField.place).update(place=replace)
                
                return Response({"message": "데이터가 성공적으로 업데이트되었습니다."}, status=status.HTTP_200_OK)
                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@extend_schema(
    summary="책임자 권한변경",
    description="책임자의 직책 권한 변경",
    request=UpdatePermissionSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=None  # 성공 응답 시의 직렬화된 데이터 구조를 지정합니다.
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
        404: OpenApiResponse(
            description="찾을 수 없음",
            response=None
        ),
    }
)
class Updatesafe_PermissionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    def patch(self, request, *args, **kwargs):

        
        
       
        serializer = UpdatePermissionSerializer(data=request.data)
        putHistory = CreateHistorySerializer(data = request.data)

        
        
        if serializer.is_valid() :
           
            if putHistory.is_valid() :
                co_Num = serializer.validated_data['co_Num']
                user_id = serializer.validated_data['user_id']  
                normal_user = Users.objects.filter(co_Num=co_Num,safe_permission = 'Y',CEO_permission='N').first()
                # user_id로 사용자 찾기
                try:
                    
                    user = Users.objects.get(user_id=user_id)
                    
                    
                    
                    putHistory.save(object = user.username)
                except Users.DoesNotExist:
                    return Response({"error": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

                # 필드 업데이트
                if hasattr(user, 'user_id'):
                    if normal_user : 
                        setattr(normal_user, 'CEO_permission', 'N')
                        setattr(normal_user, 'safe_permission', 'N')
                        normal_user.save()

                    setattr(user, 'CEO_permission', 'N')
                    setattr(user, 'safe_permission', 'Y')  
                    user.save()
                    
                    
                    return Response({"message": "데이터가 성공적으로 업데이트되었습니다."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": f"필드가 존재하지 않습니다."}, status=status.HTTP_40_BAD_REQUEST)
                
            else:    
                return Response(putHistory.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="대표 권한변경",
    description="대표 직책 권한 부여",
    request=User_idSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=None  # 성공 응답 시의 직렬화된 데이터 구조를 지정합니다.
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
        404: OpenApiResponse(
            description="찾을 수 없음",
            response=None
        ),
    }
)
class UpdateCEO_PermissionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    def patch(self, request, *args, **kwargs):




        serializer = User_idSerializer(data=request.data)
        
        if serializer.is_valid():
                
                user_id = serializer.validated_data['user_id']
                # user_id로 사용자 찾기
                try:
                    user = Users.objects.get(user_id=user_id)
                except Users.DoesNotExist:
                    return Response({"error": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

                # 필드 업데이트
                if hasattr(user, 'user_id'):
                    setattr(user, 'CEO_permission', 'Y')
                    setattr(user, 'safe_permission', 'N')  
                    user.save()
                    return Response({"message": "데이터가 성공적으로 업데이트되었습니다."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": f"필드가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="새로운 기관 추가",
    description="새로운 기관 추가",
    request=CreateFacilitySerializer,
    responses={
        201: OpenApiResponse(
            description="성공적으로 생성됨",
            response=TbFacilitySerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)
class CreateFacilityView(APIView): 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]     
    def post(self, request, *args, **kwargs):
        # 랜덤 코드 생성 (중복되지 않도록)
        co_Num = generate_unique_code()
        # 요청 데이터에 랜덤 코드를 추가
        data = request.data.copy()  # 데이터를 복사하여 수정 가능하게 함
        data['co_Num'] = co_Num
        serializer = TbFacilitySerializer(data=data)
        if serializer.is_valid():
            # 유효한 데이터를 가지고 새 Facility 인스턴스 생성
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="새로운 유지관리표 추가",
    description="새로운 유지관리표 추가",
    request=TbMaintenanceTableSerializer,
    responses={
        201: OpenApiResponse(
            description="성공적으로 생성됨",
            response=TbMaintenanceTableSerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)
class CreateMaintenanceTableView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = TbMaintenanceTableSerializer(data=request.data)
        
        if serializer.is_valid():
            # 유효한 데이터를 가지고 새 SafetyEducation 인스턴스 생성
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 윤
@extend_schema(
    summary="유지관리표 삭제",
    description="유지관리표를 삭제합니다.",
    request=MaintenanceTable,
    responses={
        200: OpenApiResponse(
            description="성공적으로 삭제됨",
            response=None
        ),
        404: OpenApiResponse(
            description="유지관리표를 찾을 수 없음",
            response=None
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)
class DeleteMaintenanceTableView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    def delete(self, request, *args, **kwargs):
        # 쿼리 매개변수에서 데이터 가져오기
        facilityNum = request.query_params.get('facilityNum')
        place = request.query_params.get('place')
        
        # 필수 파라미터 확인
        if not facilityNum or not place:
            return Response({"error": "facilityNum and place are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if MaintenancePic.objects.filter(facilityNum=facilityNum, place=place).exists:
                mPic = MaintenancePic.objects.get(facilityNum=facilityNum, place=place)
                mPic.delete()
            if MaintenanceList.objects.filter(facilityNum=facilityNum, place=place).exists:
                mList = MaintenanceList.objects.get(facilityNum=facilityNum, place=place)
                mList.delete()
            if MaintenanceTable.objects.filter(facilityNum=facilityNum, place=place).exists:
                mTable = MaintenanceTable.objects.get(facilityNum=facilityNum, place=place)
                mTable.delete()
            return Response({"message": "유지관리표가 성공적으로 삭제되었습니다."}, status=status.HTTP_200_OK)
        except MaintenanceTable.DoesNotExist:
            return Response({"error": "유지관리표를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        

@extend_schema(
    summary="유지관리표 사진삭제",
    description="유지관리표를 사진삭제합니다.",
    request=None,
    responses={
        200: OpenApiResponse(
            description="성공적으로 삭제됨",
            response=None
        ),
        404: OpenApiResponse(
            description="유지관리표를 찾을 수 없음",
            response=None
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)
class DeleteMaintenancePicView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    
    def delete(self, request, *args, **kwargs):
        # Get 'picture' parameters as a list (even if there’s only one, this will handle it)
        pictures = request.query_params.getlist('picture')  # Using getlist() to handle multiple values
        
        # Check if pictures list is empty
        if not pictures:
            return Response({"error": "One or more pictures are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Track successfully deleted pictures and missing ones
        deleted_pictures = []
        missing_pictures = []
        
        # Iterate through all the provided picture values
        for picture in pictures:
            try:
                maintenance = MaintenancePic.objects.get(picture=picture)
                maintenance.delete()
                deleted_pictures.append(picture)
            except MaintenancePic.DoesNotExist:
                missing_pictures.append(picture)
        
        # Prepare the response message
        response_message = {
            "message": "Pictures processed.",
            "deleted": deleted_pictures,
            "missing": missing_pictures
        }
        
        return Response(response_message, status=status.HTTP_200_OK)       
        

@extend_schema(
    summary="유지관리 사진 등록",
    description="유지관리 사진 등록",
    request=UploadMaintenancePicSerializer,
    responses={
        201: OpenApiResponse(
            description="Picture upload successful",
            response=UploadMaintenancePicSerializer(many=True)
        ),
        400: OpenApiResponse(description="Invalid input or missing fields"),
        404: OpenApiResponse(description="Maintenance entry not found"),
    }
)
class UploadMaintenancePicView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        co_Num = request.data.get("co_Num")
        place = request.data.get("place")
        date = request.data.get("date")

        if not co_Num or not place or not date:
            return Response({"error": "co_Num, place, and date are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            maintenance = MaintenanceList.objects.get(co_Num=co_Num, place=place, date=date)
        except MaintenanceList.DoesNotExist:
            return Response({"error": "Maintenance entry not found"}, status=status.HTTP_404_NOT_FOUND)

        # 파일 업로드 처리
        picture_files = request.FILES.getlist('picture')
        if not picture_files:
            return Response({"error": "At least one picture file is required"}, status=status.HTTP_400_BAD_REQUEST)

        saved_pictures = []
        for i, picture_file in enumerate(picture_files):
            file_name = f"{co_Num}_{place}_{date}_{i}.jpg"
            file_path = default_storage.save(f"maintenance/{file_name}", picture_file)
            picture_url = "https://safeit.eleng.co.kr" + default_storage.url(file_path)

            # MaintenancePic 항목 생성 및 저장
            pic_instance = MaintenancePic.objects.create(maintenance=maintenance, picture=picture_url, facilityNum=co_Num, place=place, checkDate=date)
            saved_pictures.append({
                "PID": pic_instance.PID,
                "picture": pic_instance.picture,
                "facilityNum": co_Num,  # 저장된 데이터
                "place": place,  # 저장된 데이터
                "checkDate": date  # 저장된 데이터
            })

        return Response(saved_pictures, status=status.HTTP_201_CREATED)

@extend_schema(
    summary="유지관리표 사진 조회",
    description="유지관리표 항목에 연결된 사진들을 조회합니다.",
    request=None,
    responses={
        200: OpenApiResponse(
            description="성공적으로 조회됨",
            response=MaintenancePicSerializer(many=True)
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
        404: OpenApiResponse(
            description="유지보수 항목을 찾을 수 없음",
            response=None
        ),
    }
)
class GetMaintenancePicView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        facilityNum = request.query_params.get("facilityNum")
        place = request.query_params.get("place")
        checkDate = request.query_params.get("checkDate")
        
        if not facilityNum or not place or not checkDate:
            return Response({"error": "facilityNum, place, and checkDate are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # MaintenancePic에서 해당 조건으로 필터링
            pictures = MaintenancePic.objects.filter(facilityNum=facilityNum, place=place, checkDate=checkDate)
            if not pictures.exists():
                return Response({"error": "No pictures found for the provided facilityNum, place, and checkDate"}, status=status.HTTP_404_NOT_FOUND)
            
            # 사진 URL 리스트를 가져옴
            response_data = [pic.picture for pic in pictures]
            
            # 현재 시간 (또는 파일 수정 시간)을 쿼리 매개변수로 추가
            response_data = [f"{pic}?t={int(timezone.now().timestamp())}" for pic in response_data]  
            
            return Response(response_data, status=status.HTTP_200_OK)
        except MaintenancePic.DoesNotExist:
            return Response({"error": "no picture"}, status=status.HTTP_200_OK)





@extend_schema(
    summary="새로운 유지관리표 상세추가******",
    description="새로운 유지관리표 상세추가 detail은 JSON으로 표시해야함",
    request=TbMaintenanceListSerializer,
    responses={
        200: OpenApiResponse(
            description="detail 업데이트 성공",
            response=TbMaintenanceListSerializer  # You might want to use a different serializer for successful responses
        ),
        201: OpenApiResponse(
            description="detail 신규생성 성공",
            response=TbMaintenanceListSerializer  # You might want to use a different serializer for successful responses
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=TbMaintenanceListSerializer
        ),
    }
)
class CreateMaintenanceListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = TbMaintenanceListSerializer(data=request.data)
        if serializer.is_valid():
            co_Num = serializer.validated_data['co_Num']
            place = serializer.validated_data['place']
            date = serializer.validated_data['date']
            new_detail = serializer.validated_data['detail']
            
            try:
                # 같은 항목이 있는지 조회
                same_list = MaintenanceList.objects.get(co_Num=co_Num, place=place, date=date)
                
                # 같은 항목이 있으면 업데이트
                if same_list:
                    same_list.detail = new_detail
                    same_list.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            
            except MaintenanceList.DoesNotExist:
                # 같은 항목이 없으면 새로 생성
                instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        
        # 직렬화된 데이터가 유효하지 않은 경우
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
@extend_schema(
    summary="새로운 위험성평가표 중 장소만 추가",
    description="새로운 위험성평가표 중 장소 추가",
    request=CreateProblemPlaceSerializer,
    responses={
        201: OpenApiResponse(
            description="성공적으로 생성됨",
            response=CreateProblemPlaceSerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)
class CreateProblemPlaceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = CreateProblemPlaceSerializer(data=request.data)
        
        if serializer.is_valid():
            # 유효한 데이터를 가지고 새 SafetyEducation 인스턴스 생성
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@extend_schema(
    summary="새로운 위험성평가표 항목 추가",
    description="새로운 위험성평가표 항목 추가",
    request=TbProblemSerializer,
    responses={
        201: OpenApiResponse(
            description="성공적으로 생성됨",
            response=TbProblemSerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)
class CreateProblemSubjectView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = TbProblemSerializer(data=request.data)
        if serializer.is_valid():
            # 유효한 데이터를 가지고 새 SafetyEducation 인스턴스 생성
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@extend_schema(
    summary="안전 교육 데이터 추가",
    description="새로운 안전 교육 데이터 추가 peopleListPic,placePic은 사진공간",
    request=CreateSafetyEducationSerializer,
    responses={
        201: OpenApiResponse(
            description="성공적으로 생성됨",
            response=CreateSafetyEducationSerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)
class CreateSafetyEducationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        
        # Extract values from request.data
        co_Num = request.data.get('co_Num', [None])[:] if 'co_Num' in request.data else None
        educationDate = request.data.get('educationDate', [None])[0:10] if 'educationDate' in request.data else None
        startEducationTime = request.data.get('startEducationTime', [None])[0:4] if 'startEducationTime' in request.data else None
        endEducationTime = request.data.get('endEducationTime', [None])[0:4] if 'endEducationTime' in request.data else None
        manager = request.data.get('manager', [None])[:] if 'manager' in request.data else None
        place = request.data.get('place', [None])[:] if 'place' in request.data else None
        detail = request.data.get('detail', [None])[:] if 'detail' in request.data else None
        title = request.data.get('title', [None])[:] if 'title' in request.data else None

        # Handle file uploads
        people_list_pic = request.FILES.get('peopleListPic')
        place_pic = request.FILES.get('placePic')

        # Prepare data for serializer
        data = {
            'co_Num': co_Num,
            'educationDate': educationDate,
            'startEducationTime': startEducationTime,
            'endEducationTime': endEducationTime,
            'manager': manager,
            'place': place,
            'detail': detail,
            'title': title
        }

        # Use serializer with prepared data
        serializer = CreateSafetyEducationSerializer(data=data)
        try:
            if serializer.is_valid():
                instance = serializer.save()

                # File processing
                if people_list_pic:
                    file_path = default_storage.save(f"edu/{instance.co_Num}_{instance.PID}_0.jpg", people_list_pic)
                    instance.peopleListPic = "https://safeit.eleng.co.kr" + default_storage.url(file_path)

                if place_pic:
                    file_path = default_storage.save(f"edu/{instance.co_Num}_{instance.PID}_1.jpg", place_pic)
                    instance.placePic ="https://safeit.eleng.co.kr" + default_storage.url(file_path)

                instance.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Handle unexpected exceptions
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
@extend_schema(
    summary="새로운 위험성평가표 개선사항추가",
    description="새로운 위험성평가표 개선사항추가",
    request=CreateProblemSerializer,
    responses={
        201: OpenApiResponse(
            description="성공적으로 생성됨",
            response=None
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)
class CreateProblemDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny] 
    
    def post(self, request, *args, **kwargs):
            
    

            co_Num = request.data.get("co_Num", [None])[:] if "co_Num" in request.data else None
            dangerSolutionAfter = request.data.get("dangerSolutionAfter", [None])[:] if "dangerSolutionAfter" in request.data else None
            dangerSolutionBefore = (request.data.get("dangerSolutionBefore", [None])[:] if "dangerSolutionBefore" in request.data else None)
            record = request.data.get("record", [None])[:] if "record" in request.data else None
            pic_before = request.data.get("pic_before", [None])[:] if "pic_before" in request.data else None
            place = request.data.get("place", [None])[:] if "place" in request.data else None
            workstep = request.data.get("workstep", [None])[:] if "workstep" in request.data else None 
            frequency =1+int(request.data.get("frequency", 0))
            strength = 1+int(request.data.get("strength", 0))
            riskScore = int(request.data.get("riskScore", 0)) 
            writer = request.data.get("writer", [None])[:] if "writer" in request.data else None  
            work = request.data.get("work", [None])[:] if "work" in request.data else None  
            is_last = request.data.get("is_last", [None])[:] if "is_last" in request.data else None
            if dangerSolutionBefore == "":
                dangerSolutionBefore = None
            # 유효성 검사된 데이터 추출
            update_co_Num = co_Num
            update_place = place
            update_work = work
            # 마지막 "is_last"인 Solution 객체 찾기
            data = {
                "co_Num": co_Num,
                "dangerSolutionAfter": dangerSolutionAfter,
                "dangerSolutionBefore":  dangerSolutionBefore,
                "record": record,
                "pic_before": pic_before,
                "place": place,
                "workstep": workstep,
                "frequency": int(frequency),
                "strength": int(strength),
                "riskScore": int(riskScore),
                "writer": writer,
                "work": work,
                "is_last": is_last
            }
            serializer = CreateProblemSerializer(data=data)
            if serializer.is_valid():    
                try:
                
                    last_is = Solution.objects.get(co_Num=update_co_Num, place=update_place, is_last='Y', work=update_work)


                        # 찾은 Solution 객체 업데이트
                    if hasattr(last_is, 'is_last'):
                        setattr(last_is, 'is_last', 'N')
                        last_is.save()
                except Solution.DoesNotExist:
                # Solution 객체가 없는 경우 처리
                    pass

            
                instance = serializer.save()
                pic_afters = request.FILES.get('pic_after')
                if pic_afters:
                        file_path = default_storage.save(f"prob/{instance.co_Num}_{instance.pid}.jpg", pic_afters)
                        instance.pic_after = "https://safeit.eleng.co.kr" + default_storage.url(file_path)
                # else:
                #     instance.pic_after = None
                       
                instance.save()
                
                # 파일 업로드 처리
                    
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)         

    
@extend_schema(
    summary="사용자 프로필사진 등록",
    description="사용자 프로필사진 등록",
    request=UploadUserProfileSerializer,#id,사진
    responses={
        201: OpenApiResponse(
            description="성공적으로 생성됨",
            response=None
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)
#윤
class UploadUserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = Users.objects.get(user_id=user_id)
        except Users.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        profile = request.FILES.get('profile')
        if profile:
            # Create instance or get existing one
            instance, created = UserProfile.objects.get_or_create(user=user)
            
            # Define the file path where the image will be stored
            new_file_path = f"profile/{user_id}.jpg"
            
            # If the file already exists, delete it before saving the new one
            if default_storage.exists(new_file_path):
                default_storage.delete(new_file_path)
            
            # Save the new profile image
            default_storage.save(new_file_path, profile)
            
            # Update the instance profile URL
            instance.profile = "https://safeit.eleng.co.kr" + default_storage.url(new_file_path)
            instance.save()

            serializer = UserProfileSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Profile image is required"}, status=status.HTTP_400_BAD_REQUEST)      



@extend_schema(
    summary="사용자 프로필사진 조회",
    description="사용자 프로필사진 조회",
    request=User_idSerializer,
    responses={
        200: OpenApiResponse(
            description="성공적으로 생성됨",
            response=None
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)        
class GetUserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):

        input_serializer = User_idSerializer(data=request.query_params)
        if input_serializer.is_valid():
            userid = input_serializer.validated_data['user_id']
            
            try:
                queryset = UserProfile.objects.get(user_id=userid)
                output_serializer = UserProfileSerializer(queryset)
                
                # 현재 시간 (또는 파일 수정 시간)을 쿼리 매개변수로 추가
                profile_url = output_serializer.data.get('profile')
                timestamp = timezone.now().timestamp()  # 또는 파일의 마지막 수정 시간
                profile_url_with_timestamp = f"{profile_url}?t={int(timestamp)}"
                
                
                # 데이터에 캐시 무효화를 위한 URL 적용
                response_data = output_serializer.data
                response_data['profile'] = profile_url_with_timestamp
                
                return Response(response_data, status=status.HTTP_200_OK)
            except UserProfile.DoesNotExist:
                return Response({"error": "No profile picture"}, status=status.HTTP_200_OK)
                
        return Response({"프로필이 없지만 괜춘"},  status=status.HTTP_200_OK)
    
@extend_schema(
    summary="사용자 프로필사진 삭제",
    description="사용자 프로필사진 삭제",
    request=User_idSerializer,
    responses={
        200: OpenApiResponse(
            description="성공적으로 삭제됨",
            response=None
        ),
        404: OpenApiResponse(
            description="찾을 수 없음",
            response=None
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)
class DeleteUserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        
        

        # Authorization 헤더에서 JWT 토큰 추출
        auth_header = request.headers.get('Authorization')
            
        if not auth_header:
            return Response({"error": "JWT 토큰이 제공되지 않았거나 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 토큰 추출 (Bearer 접두어가 있는 경우)
        token_str = auth_header.split(' ')[1] if ' ' in auth_header else auth_header

        # JWT 토큰에서 user_id 추출
        try:
            access_token = AccessToken(token_str)
            user_id = access_token.payload.get('user_id')  # payload에서 user_id를 가져옵니다.
            
        except Exception as e:
            return Response({"error": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)

        
            
        try:
            # 특정 user_id를 가진 프로필을 조회
            user_profile = UserProfile.objects.get(user_id=user_id)
                
            # 조회된 프로필 삭제
            user_profile.delete()
                
            return Response({"message": "프로필이 성공적으로 삭제되었습니다."}, status=status.HTTP_200_OK)
                
        except UserProfile.DoesNotExist:
            return Response({"error": "일치하는 프로필을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
                


   

@extend_schema(
    summary="사용자 삭제",
    description="사용자 삭제를 수행합니다. URL 경로에 user_id를 포함시켜 사용자를 삭제합니다.",
    request=Users,
    responses={
        200: OpenApiResponse(
            description="성공적으로 삭제됨",
            response=None
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
        404: OpenApiResponse(
            description="찾을 수 없음",
            response=None
        ),
    }
)
class DeleteUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')

        if not user_id:
            return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # User를 찾습니다.
            user = Users.objects.get(user_id=user_id)

            user.delete()

            return Response({"success": "User deleted successfully"}, status=status.HTTP_200_OK)

        except Users.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # 다른 예외 처리
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        


@extend_schema(
    summary="기관 history",
    description="기관번호 입력",
    request=Userco_NumSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=TbmanageHistory  # You might want to use a different serializer for successful responses
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=TbmanageHistory
        ),
    }
)
class getHistoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Validate input data
        input_serializer = Userco_NumSerializer(data=request.data)
        if input_serializer.is_valid():
            co_Num = input_serializer.validated_data['co_Num']
            
            # Query the database for the facility with the given PID
            try:
                queryset = manageHistory.objects.filter(co_Num=co_Num)
                # Serialize the single facility record for the response
                output_serializer = TbmanageHistory(queryset,many=True)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            except Facility.DoesNotExist:
                return Response({"error": "No matching records found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="유지관리표 날짜별 출력",
    description="기관번호/장소/날짜 (facilityNum, place, checkDate)를 통해 유지관리표를 출력합니다.",
    request=MaintenanceRequestSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=None
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)
class MaintenanceDateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # API로부터 파라미터를 받아오는 부분
        facilityNum = request.data.get('facilityNum')
        place = request.data.get('place')
        checkDate = request.data.get('checkDate')
        processType=1

        # 파라미터가 제공되지 않은 경우 기본값 설정
        if not facilityNum or not place or not checkDate:
            return Response({"error": "필수 파라미터가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 외부 스크립트의 함수 호출
        try:
            fileDir = f'/home/safeit/seif/media/exel/{facilityNum}'
            output_path = f'{fileDir}/유지관리표_{place}_{checkDate}.xlsx'
            if (os.path.isfile(output_path)):
                os.remove(output_path)
            file_url = process_excel_file(processType, facilityNum, place, checkDate)
            if file_url:
                return Response({"message": "엑셀 파일 처리가 완료되었습니다.", "file_url": file_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "파일 처리 중 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"오류 발생: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
@extend_schema(
    summary="유지관리표 장소별 출력",
    description="기관번호/장소 (facilityNum, place)를 통해 유지관리표를 출력합니다.",
    request=MaintenancePlaceRequestSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=None
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)
class MaintenancePlaceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # API로부터 파라미터를 받아오는 부분
        facilityNum = request.data.get('facilityNum')
        place = request.data.get('place')

        # 파라미터가 제공되지 않은 경우 기본값 설정
        if not facilityNum or not place:
            return Response({"error": "필수 파라미터가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        mList = MaintenanceList.objects.filter(co_Num = facilityNum, place = place)
        dates = []
        for m in mList:
            dates.append(m.date)
            
        # 외부 스크립트의 함수 호출
        try:
            fileDir = f'/home/safeit/seif/media/exel/{facilityNum}'
            output_path = f'{fileDir}/유지관리표_{place}.xlsx'
            if (os.path.isfile(output_path)):
                os.remove(output_path)
            file_url = process_excel_file_place(facilityNum, place, dates)
            if file_url:
                return Response({"message": "엑셀 파일 처리가 완료되었습니다.", "file_url": file_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "파일 처리 중 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"오류 발생: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@extend_schema(
    summary="유지관리표 기관별 출력",
    description="기관번호 (facilityNum)를 통해 유지관리표를 출력합니다.",
    request=Userco_NumSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=None
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)
class MaintenanceFacilityView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # API로부터 파라미터를 받아오는 부분
        facilityNum = request.data.get('co_Num')

        # 파라미터가 제공되지 않은 경우 기본값 설정
        if not facilityNum:
            return Response({"error": "필수 파라미터가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        mList = list(MaintenanceList.objects.filter(co_Num = facilityNum))
            
        # 외부 스크립트의 함수 호출
        try:
            fileDir = f'/home/safeit/seif/media/exel/{facilityNum}'
            output_path = f'{fileDir}/유지관리표_총합본.xlsx'
            if (os.path.isfile(output_path)):
                os.remove(output_path)
            file_url = process_excel_file_facility(facilityNum, mList)
            if file_url:
                return Response({"message": "엑셀 파일 처리가 완료되었습니다.", "file_url": file_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "파일 처리 중 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"오류 발생: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


@extend_schema(
    summary="위험성평가표1 기관전체 출력",
    description="기관번호 (facilityNum)를 통해 위험성평가표를 출력합니다.",
    request=Userco_NumSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=None
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=None
        ),
    }
)
class RiskFacilityView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # API로부터 파라미터를 받아오는 부분
        facilityNum = request.data.get('co_Num')
        processType=1

        # 파라미터가 제공되지 않은 경우 기본값 설정
        if not facilityNum:
            return Response({"error": "필수 파라미터가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
            
        # 외부 스크립트의 함수 호출
        try:
            file_url = createRiskDateExcel(processType, facilityNum)
            if file_url:
                return Response({"message": "엑셀 파일 처리가 완료되었습니다.", "file_url": file_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "파일 처리 중 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"오류 발생: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@extend_schema(
    summary="위험성평가표2 장소전체 출력",
    description="기관번호 (facilityNum), 장소(place)를 통해 위험성평가표를 출력합니다.",
    request=RiskPlaceSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=RiskPlaceSerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=RiskPlaceSerializer
        ),
    }
)
class RiskFacilityPlaceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # API로부터 파라미터를 받아오는 부분
        facilityNum = request.data.get('facilityNum')
        place = request.data.get('place')
        processType=2

        # 파라미터가 제공되지 않은 경우 기본값 설정
        if not facilityNum or not place:
            return Response({"error": "필수 파라미터가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
            
        # 외부 스크립트의 함수 호출
        try:
            file_url = createRiskDateExcel(processType, facilityNum, place)
            if file_url:
                return Response({"message": "엑셀 파일 처리가 완료되었습니다.", "file_url": file_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "파일 처리 중 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"오류 발생: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        
 
@extend_schema(
    summary="위험성평가표3 작업전체 출력",
    description="기관번호 (facilityNum), 장소(place), 작업(work)를 통해 위험성평가표를 출력합니다.",
    request=RiskPlaceWorkSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=RiskPlaceWorkSerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=RiskPlaceWorkSerializer
        ),
    }
)
class SendRiskPlaceWorkFacilityView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # API로부터 파라미터를 받아오는 부분
        facilityNum = request.data.get('facilityNum')
        place = request.data.get('place')
        work = request.data.get('work')
        processType=3

        # 파라미터가 제공되지 않은 경우 기본값 설정
        if not facilityNum or not place or not work:
            return Response({"error": "필수 파라미터가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
            
        # 외부 스크립트의 함수 호출
        try:
            file_url = createRiskDateExcel(processType, facilityNum, place, work)
            if file_url:
                return Response({"message": "엑셀 파일 처리가 완료되었습니다.", "file_url": file_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "파일 처리 중 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"오류 발생: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            
        
        
        
@extend_schema(
    summary="안전교육기록서2 출력",
    description="기관번호 (facilityNum), 제목(title), 날짜(educationDate)를 통해 안전교육기록서를 출력합니다.",
    request=EduTitleDateSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=EduTitleDateSerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=EduTitleDateSerializer
        ),
    }
)
class SendEduTitleDateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # API로부터 파라미터를 받아오는 부분
        facilityNum = request.data.get('facilityNum')
        title = request.data.get('title')
        work = request.data.get('work')
        educationDate = request.data.get('educationDate')
        processType=2

        # 파라미터가 제공되지 않은 경우 기본값 설정
        if not facilityNum or not title or not educationDate:
            return Response({"error": "필수 파라미터가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
            
        # 외부 스크립트의 함수 호출
        try:
            file_url = createEduExcel(processType, facilityNum, title, educationDate)
            if file_url:
                return Response({"message": "엑셀 파일 처리가 완료되었습니다.", "file_url": file_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "파일 처리 중 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"오류 발생: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
        
        
@extend_schema(
    summary="안전교육기록서1 전체 출력",
    description="기관번호 (facilityNum)를 통해 안전교육기록서를 출력합니다.",
    request=EduSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=EduSerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=EduSerializer
        ),
    }
)
class SendEduView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # API로부터 파라미터를 받아오는 부분
        facilityNum = request.data.get('facilityNum')
        processType=1

        # 파라미터가 제공되지 않은 경우 기본값 설정
        if not facilityNum:
            return Response({"error": "필수 파라미터가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
            
        # 외부 스크립트의 함수 호출
        try:
            file_url = createEduExcel(processType, facilityNum)
            if file_url:
                return Response({"message": "엑셀 파일 처리가 완료되었습니다.", "file_url": file_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "파일 처리 중 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"오류 발생: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
        
        
        
@extend_schema(
    summary="실행팀확인팀 입력받는 API",
    description="leader, supervisor, safeManager, fieldManager 를 입력받고 co_Num을 전달받아 DB에 저장",
    request=SolutionUserSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=SolutionUserSerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=SolutionUserSerializer
        ),
    }
)
class SolutionUserSerializerView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # API로부터 파라미터를 받아오는 부분
        co_Num = request.data.get('co_Num')
        leader = request.data.get('leader')
        supervisor = request.data.get('supervisor')
        safeManager = request.data.get('safeManager')
        fieldManager = request.data.get('fieldManager')

        # 파라미터가 제공되지 않은 경우 기본값 설정
        if not co_Num:
            return Response({"error": "필수 파라미터가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
            
         # SolutionUser 모델에 데이터를 저장
        try:
            solution_user = SolutionUser.objects.create(
                co_Num=co_Num,
                leader=leader,
                supervisor=supervisor,
                safeManager=safeManager,
                fieldManager=fieldManager
            )
            solution_user.save()

            # 성공적으로 저장되면 응답
            return Response({"message": "데이터가 성공적으로 저장되었습니다."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@extend_schema(
    summary="관련법목록 입력받는 API",
    description="law를 입력받고 midCause를 전달받아 DB에 저장",
    request=saveLawListSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=saveLawListSerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=saveLawListSerializer
        ),
    }
)
class saveLawListSerializerView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # API로부터 파라미터를 받아오는 부분
        law = request.data.get('law')
        midCause = request.data.get('midCause')

        # 파라미터가 제공되지 않은 경우 기본값 설정
        if not law or not midCause:
            return Response({"error": "필수 파라미터가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            lawList = saveLawList.objects.create(
                law=law,
                midCause=midCause
            )
            lawList.save()

            # 성공적으로 저장되면 응답
            return Response({"message": "데이터가 성공적으로 저장되었습니다."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        


@extend_schema(
    summary="위험성 관리표 확인자 등록 API",
    description="위험성 관리표 확인시 자동으로 추가",
    request=addRiskConfirmerSerializer,
    responses={
        200: OpenApiResponse(
            description="성공",
            response=addRiskConfirmerSerializer
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=addRiskConfirmerSerializer
        ),
    }
)
class AddRiskConfirmerView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # API로부터 파라미터를 받아오는 부분
        co_Num = request.data.get('co_Num')
        place = request.data.get('place')
        work = request.data.get('work')
        date = request.data.get('date')

        user_id = request.data.get('user_id')

        try:
            solution = Solution.objects.get(co_Num=co_Num, place=place,work=work, record=date, is_last='Y')
        except Solution.DoesNotExist:
            return Response({"error": "위험성 관리표를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    
        try:
            confirmer = RiskSolutionConfirmer.objects.create(
                solution_pid=solution,
                user_id=user_id,
                date=timezone.now()
            )
            confirmer.save()

            # 성공적으로 저장되면 응답
            return Response({"message": "데이터가 성공적으로 저장되었습니다."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="확인자 목록",
    description="",
    request=riskSolutionIdSerializer,#입력받는곳
    responses={
        200: OpenApiResponse(
            description="성공",
            response=confirmerListSerializer  # 출력양식넣는곳
        ),
        400: OpenApiResponse(
            description="잘못된 요청",
            response=confirmerListSerializer # 에러나는곳
        ),
    }
)
class ConfirmerListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        solution_pid = request.data.get('solution_pid')
        
        confirmers = RiskSolutionConfirmer.objects.filter(solution_pid=solution_pid).values_list('user_id') #비교데이터테이블
        if confirmers.exists():
            users = Users.objects.filter(user_id__in=confirmers) #비교데이터테이블
        else:
            return Response({"error": "No Confirmers Exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if users.exists():
            # Serialize the queryset for the response
            output_serializer = confirmerListSerializer(users, many=True)
            
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No Such User"}, status=status.HTTP_404_NOT_FOUND)
        


#웹페이지
def home(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

def facility_view(request):
    return render(request, 'facility.html')

def addFacility_view(request):
    return render(request, 'addFacility.html')

def personal_information_view(request):
    return render(request, 'personal_information.html')

def quit_view(request):
    return render(request, 'quit.html')

def upload_image(request):
    if request.method == 'POST':
        # 이미지 업로드 처리 로직
        return HttpResponse("이미지가 업로드되었습니다.")
    else:
        return HttpResponseForbidden("허용되지 않는 요청입니다.")