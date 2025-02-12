from django.urls import path
from .import views
 

urlpatterns = [
    path("major/", views.MajorListCreate.as_view(), name="Major-view-create"),
    path("major/<int:pk>/", views.MajorRetreiveUpdateDestroy.as_view(), name="Major-view-retreive-update-delete"),

    path("complementary_activity/student/<int:studentId_id>/", views.ComplementaryActivitySerializerStudent.as_view(), name = "ComplementaryActivity-view-student"),
    path("complementary_activity/student/<int:studentId_id>/type/<int:ActivityTypeId_id>/", views.ComplementaryActivitySerializerStudentType.as_view(), name = "ComplementaryActivity-view-student-type"),
    path("complementary_activity/student/<str:name>/", views.ComplementaryActivitySerializerStudentName.as_view(), name = "ComplementaryActivity-view-student-name"),
    path("complementary_activity/major/<int:majorId_id>/", views.ComplementaryActivitySerializerMajor.as_view(), name = "ComplementaryActivity-view-major"),
    path("complementary_activity/major/<int:majorId_id>/type/<int:ActivityTypeId_id>/", views.ComplementaryActivitySerializerMajorType.as_view(), name = "ComplementaryActivity-view-major-type"),
    path("complementary_activity/<int:ComplementaryActivity_id>/", views.ComplementaryActivitySerializerEditApprovedRecuseFeedbak.as_view(), name = "ComplementaryActivity-view-edit-approved-recuse-feedback"),
    path("complementary_activity/coordenador/<int:majorId_id>/", views.ComplementaryActivitySerializerCoordenadorMajor.as_view(), name = "ComplementaryActivity-view-coordenador-approved-or-recuse"),
    path("complementary_activity/coordenador/approved/<int:majorId_id>/", views.ComplementaryActivitySerializerCoordenadorMajorApproved.as_view(), name = "ComplementaryActivity-view-coordenador-approved"),

    path("event/", views.EventListCreate.as_view(), name="Event-view-create"),
    path("event/<int:pk>/", views.EventRetreiveUpdateDestroy.as_view(), name="Event-view-retreive-update-delete"),
    path("event/<str:name>/", views.EventRetreiveUpdateDestroy.as_view(), name="Event-view-retreive-update-delete"),

    path("student/", views.StudentListCreate.as_view(), name="Student-view-create"),
    path("student/<int:pk>/", views.StudentRetreiveUpdateDestroy.as_view(), name="Student-view-retreive-update-delete"),

    path("activity_type/", views.ActivityTypeListCreate.as_view(), name="ActivityType-view-create"),
    path("activity_type/<int:pk>/", views.ActivityTypeRetreiveUpdateDestroy.as_view(), name="ActivityType-view-retreive-update-delete"),

    path("complementary_activity/", views.SubmitComplementaryActivityCreate.as_view(), name="SubmitComplementaryActivity-create"),

    path("certificate/<int:pk>/", view=views.CertificateRetrieve.as_view(), name="Certificate-Retrieve"),
    path("certificate/<int:event_id>/<int:student_id>", views.CertificateRetrieveByEventAndStudent.as_view(), name="Certificate-Retrievr-By-Event-Student"),
    
    
    path("files/certificates/<str:cer_name>", views.retrieve_certificate, name="slugma"),
    path("files/images/<str:entitty_name>/<str:pic_name>", views.retrieve_img, name="slugma"),

    path("qr/image/<str:event_id>/<str:student_id>", views.gen_qr_code, name="qr-code-generation")
    # path("files/images/<str:entitty_name>/<str:pic_name>", views.retrieve_img, name="")

]