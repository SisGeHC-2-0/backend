from django.urls import path
from .import views
 

urlpatterns = [
    path("major/", views.MajorListCreate.as_view(), name="Major-view-create"),
    path("major/<int:pk>/", views.MajorRetreiveUpdateDestroy.as_view(), name="Major-view-retreive-update-delete"),

    path("complementary_activity/student/<int:studentId_id>/", views.ComplementaryActivitySerializerStudent.as_view(), name = "ComplementaryActivity-view-create"),
    path("complementary_activity/student/<int:studentId_id>/type/<int:ActivityTypeId_id>/", views.ComplementaryActivitySerializerStudentType.as_view(), name = "ComplementaryActivity-view-create"),
    path("complementary_activity/student/<str:name>/", views.ComplementaryActivitySerializerStudentName.as_view(), name = "ComplementaryActivity-view-create"),
    path("complementary_activity/major/<int:majorId_id>/", views.ComplementaryActivitySerializerMajor.as_view(), name = "ComplementaryActivity-view-create"),
    path("complementary_activity/major/<int:majorId_id>/type/<int:ActivityTypeId_id>/", views.ComplementaryActivitySerializerMajorType.as_view(), name = "ComplementaryActivity-view-create"),


    path("activity_type/", views.ActivityTypeListCreate.as_view(), name="ActivityType-view-create"),
    path("activity_type/<int:pk>/", views.ActivityTypeRetreiveUpdateDestroy.as_view(), name="ActivityType-view-retreive-update-delete"),

    path("complementary_activity/", views.SubmitComplementaryActivityCreate.as_view(), name="SubmitComplementaryActivity-create"),


]