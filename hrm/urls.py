from django.urls import path
from rest_framework.routers import SimpleRouter

from hrm import views


app_name = 'hrm'

router = SimpleRouter()
router.register(
    prefix=r'',
    viewset=views.EmployeeViewset
)
urlpatterns = router.urls

urlpatterns += [
    path('all-employees',views.EmployeeElasticSearchAPIView.as_view())
]