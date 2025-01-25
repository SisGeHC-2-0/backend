from django.urls import path
from .import views
 

urlpatterns = [
    path("major/", views.MajorListCreate.as_view(), name="Major-view-create"),
    path("major/<int:pk>/", views.MajorRetreiveUpdateDestroy.as_view(), name="Major-view-retreive-update-delete"),

    path("complementary_activity/aluno/<int:studentId_id>/", views.ComplementaryActivitySerializerAluno.as_view(), name = "ComplementaryActivity-view-create"),
    path("complementary_activity/aluno/<int:studentId_id>/tipo/<int:ActivityTypeId_id>/", views.ComplementaryActivitySerializerAlunoTipo.as_view(), name = "ComplementaryActivity-view-create"),
    path("complementary_activity/aluno/<str:name>/", views.ComplementaryActivitySerializerAlunoName.as_view(), name = "ComplementaryActivity-view-create"),
    path("complementary_activity/curso/<int:majorId_id>/", views.ComplementaryActivitySerializerCurso.as_view(), name = "ComplementaryActivity-view-create"),
    path("complementary_activity/curso/<int:majorId_id>/tipo/<int:ActivityTypeId_id>/", views.ComplementaryActivitySerializerCursoTipo.as_view(), name = "ComplementaryActivity-view-create"),


    path("activity_type/", views.ActivityTypeListCreate.as_view(), name="ActivityType-view-create"),
    path("activity_type/<int:pk>/", views.ActivityTypeRetreiveUpdateDestroy.as_view(), name="ActivityType-view-retreive-update-delete"),
]