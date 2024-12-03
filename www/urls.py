from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static

#웹페이지
from . import views

urlpatterns = [
    path('table_info/', table_info, name='table-info'),
    path('mytest/',test_login, name='test_login'),
    path('protest/',pro, name='tes'),
    path('api/tb_classification/', TbClassificationListView.as_view(), name='tb_classification'),
    path('api/tb_facility/', TbFacilityListView.as_view(), name='tb_facility'),
    path('api/tb_history/', TbHistoryListView.as_view(), name='tb_history'),
    path('api/tb_lawList/', TbLawListListView.as_view(), name='tb_lawList'),
    path('api/tb_maintenanceList/', TbMaintenanceListListView.as_view(), name='tb_maintenanceList'),
    path('api/tb_maintenanceTable/', TbMaintenanceTableListView.as_view(), name='tb_maintenanceTable'),
    path('api/tb_problem/', TbProblemListView.as_view(), name='tb_problem'),
    path('api/tb_riskList/', TbRiskListListView.as_view(), name='tb_riskList'),
    path('api/tb_safetyEducation/', TbSafetyEducationListView.as_view(), name='tb_safetyEducation'),
    path('api/tb_solution/', TbSolutionListView.as_view(), name='tb_solution'),
    path('api/tb_user/', TbUserListView.as_view(), name='tb_user'),

    path('register/signup/', UserRegistrationView.as_view(), name='user-registration'),
    path('register/login/', UserLoginView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('update/update_User/', UpdateUserView.as_view(), name='update_User'),
    path('update/updateMaintenance/', UpdateMaintenanceView.as_view(), name='UpdateMaintenance'),
    path('update/Updatesafe_Permission/', Updatesafe_PermissionView.as_view(), name='Updatesafe_Permission'),
    path('update/UpdateCEO_Permission/', UpdateCEO_PermissionView.as_view(), name='UpdateCEO_Permission'),

    path('history/getHistory/', getHistoryView.as_view(), name='getHistory'),

    path('user_api/MaintenanceTable/', UserMaintenanceTableView.as_view(), name='user_Maintenance'),
    path('user_api/facility/', UserFacilityView.as_view(), name='user_facility'),
    path('user_api/MaintenanceList/', UserMaintenanceListView.as_view(), name='user_MaintenanceList'),
    path('user_api/MaintenanceListDetail/', UserMaintenanceListDetailView.as_view(), name='user_MaintenanceListDetail'),
    path('user_api/UserFacilityInfo/', UserFacilityInfoView.as_view(), name='UserFacilityInfo'),
    path('user_api/FacilityUserList/', FacilityUserListView.as_view(), name='FacilityUserList'),
    path('user_api/Same_Co_Num_User/', Same_Co_Num_UserView.as_view(), name='Same_Co_Num_User'),
    path('user_api/EducationDetail/', EducationDetailView.as_view(), name='EducationDetail'),
    path('user_api/SafetyEducation_List/', SafetyEducation_ListView.as_view(), name='SafetyEducation_List'),
    path('user_api/EmailVerification/', SendVerificationView.as_view(), name='EmailVerification'),
    path('user_api/AuthCodeCheck/', VerificaitonCodeView.as_view(), name='AuthCodeCheck'),
    path('user_api/ChangePw/', PasswordChangeView.as_view(), name='ChangePw'),
    path('user_api/GetConfirmerList/', ConfirmerListView.as_view(), name='GetConfirmerList'),

    path('token/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('bool/user_id_boolView/', user_id_boolView.as_view(), name='user_id_bool'),
    path('bool/email_boolView/', email_boolView.as_view(), name='email_bool'),
    path('bool/Co_Num_bool/', Co_Num_boolView.as_view(), name='Co_Num_bool'),
    

    path('problem/Problem_place/', Problem_placeView.as_view(), name='Problem_place'),
    path('problem/Problem_work/', Problem_workView.as_view(), name='Problem_work'),
    path('problem/Problem_detail/', Problem_detailView.as_view(), name='Problem_detail'),

    path('master/All_FacilityList/', All_FacilityListView.as_view(), name='All_FacilityList'),

    path('profile/UploadUserProfile/', UploadUserProfileView.as_view(), name='UploadUserProfile'),
    path('profile/GetUserProfile/', GetUserProfileView.as_view(), name='GetUserProfile'),
    path('profile/DeleteUserProfile/', DeleteUserProfileView.as_view(), name='DeleteUserProfile'),

    path('create/CreateSafetyEducation/', CreateSafetyEducationView.as_view(), name='CreateSafetyEducation'),
    path('create/CreateFacility/', CreateFacilityView.as_view(), name='CreateFacility'),
    path('create/CreateMaintenanceTable/', CreateMaintenanceTableView.as_view(), name='CreateMaintenanceTable'),
    path('create/CreateProblemDetail/', CreateProblemDetailView.as_view(), name='CreateProblemDetail'),
    path('create/CreateProblemPlace/', CreateProblemPlaceView.as_view(), name='CreateProblemPlace'),
    path('create/CreateProblemSubject/', CreateProblemSubjectView.as_view(), name='CreateProblemSubject'),
    path('create/CreateMaintenanceList/', CreateMaintenanceListView.as_view(), name='CreateMaintenanceList'),
    path('create/UploadMaintenancePic/', UploadMaintenancePicView.as_view(), name='UploadMaintenancePic'),
    path('create/GetMaintenancePic/', GetMaintenancePicView.as_view(), name='GetMaintenancePic'),

    path('delete/DeleteMaintenanceTable/', DeleteMaintenanceTableView.as_view(), name='DeleteMaintenanceTable'),    
    path('delete/DeleteMaintenancePic/', DeleteMaintenancePicView.as_view(), name='DeleteMaintenancePic'),  
    path('delete_user/DeleteUser/<str:user_id>/', DeleteUserView.as_view(), name='delete_user'),
    
    path('create/SendMaintenanceDate/', MaintenanceDateView.as_view(), name='SendMaintenanceDate'),
    path('create/SendMaintenancePlace/', MaintenancePlaceView.as_view(), name='SendMaintenancePlace'),
    path('create/SendMaintenanceFacility/', MaintenanceFacilityView.as_view(), name='SendMaintenanceFacility'),

    path('create/SendRiskFacility/', RiskFacilityView.as_view(), name='SendRiskFacility'),
    path('create/SendRiskPlaceFacility/', RiskFacilityPlaceView.as_view(), name='SendRiskPlaceFacility'),
    path('create/SendRiskPlaceWorkFacility/', SendRiskPlaceWorkFacilityView.as_view(), name='SendRiskPlaceWorkFacility'),
    
    path('create/SendEdu/', SendEduView.as_view(), name='SendEdu'),
    path('create/SendEduTitleDate/', SendEduTitleDateView.as_view(), name='SendEduTitleDate'),
    path('create/SolutionUserSerializer/', SolutionUserSerializerView.as_view(), name='SolutionUserSerializer'),
    path('create/AddRiskConfirmer/', AddRiskConfirmerView.as_view(), name='AddRiskConfirmer'),
    
    path('get/saveLawListSerializer/', saveLawListSerializerView.as_view(), name='saveLawListSerializer'),
    
    #웹페이지
    path('', views.home, name='home'),
    path('quit/', quit_view, name='quit'),
    path('personal_information/', personal_information_view, name='personal_information'),
    path('login/', login_view, name='login'),
    path('facility/', facility_view, name='facility'),
    path('addFacility/', addFacility_view, name='addFacility'),
    
    
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
