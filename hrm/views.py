import operator
from functools import reduce
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from elasticsearch_dsl import Q as QQ
from hrm.documents import HRMDocument

from hrm.models import Employee
from hrm.serializers import EmployeeSerializer


class EmployeeViewset(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeeElasticSearchAPIView(APIView, PageNumberPagination):
    serializer_class = EmployeeSerializer
    document_class = HRMDocument

    """
    Example:
    elasticsearch==7.13.4
    elasticsearch-dsl==7.4.0
    django-elasticsearch-dsl==7.2.2   
    django-cors-headers==3.13.0
    Django==4.0.4
    djangorestframework==3.13.1
    http://127.0.0.1:8000/hrm/all-employees?search=software&company=Daffodil%20Family
    http://127.0.0.1:8000/hrm/all-employees?search=software&courses=Business%20Communication
    http://127.0.0.1:8000/hrm/all-employees?search=software&courses=Database
    http://127.0.0.1:8000/hrm/all-employees?search=software&company=Daffodil%20Family&courses=Database
    http://127.0.0.1:8000/hrm/all-employees?search=softwre&courses=Complr
    http://127.0.0.1:8000/hrm/all-employees?search=softwre&courses=Dataase
    http://127.0.0.1:8000/hrm/all-employees?search=softwre&skills=Elastic%20Search
    http://127.0.0.1:8000/hrm/all-employees?search=engineer&skills=python
    http://127.0.0.1:8000/hrm/all-employees?search=developer&skills=python
    http://127.0.0.1:8000/hrm/all-employees?courses=Accounting
    http://127.0.0.1:8000/hrm/all-employees?search=software&exp_gte=3&exp_lte=5
    http://127.0.0.1:8000/hrm/all-employees?search=software&exp_gte=4.1&exp_lte=5
    http://127.0.0.1:8000/hrm/all-employees?search=engineer&skills=java
    http://127.0.0.1:8000/hrm/all-employees?search=engineer&skills=java&level=INTERMEDIATE
    http://127.0.0.1:8000/hrm/all-employees?search=engineer&skills=elastic&level=INTERMEDIATE

    """

    def get(self, request):
        # print(request.META['QUERY_STRING'])
        try:
            finalquery = []
            q = request.GET.get('search', None)
            company = request.GET.get('company', None)
            courses = request.GET.get('courses', None)
            skills = request.GET.get('skills', None)
            level = request.GET.get('level', None)
            exp_gte = request.GET.get('exp_gte', None)
            exp_lte = request.GET.get('exp_lte', None)

            if q is not None and not q == '':
                finalquery.append(QQ(
                    'multi_match',
                    query=q,
                    fields=[
                        'name',
                        'current_job',

                    ],
                    fuzziness='auto'))

            if company is not None and not company == '':
                finalquery.append(QQ(
                    'match_phrase',
                    company__name=company,
                ))

            if courses is not None and not courses == '':
                finalquery.append(
                    QQ(
                        'multi_match',
                        query=courses,
                        fields=[

                            'courses',

                        ],
                        fuzziness='auto'),
                )
            if skills is not None and not skills == '':
                finalquery.append(
                    QQ(
                        'nested',
                        path="skills",
                        query=QQ("match_phrase", skills__name=skills.lower()),)
                )

            if len(finalquery) > 0:
                response = self.document_class.search().extra(size=10000).query(
                    reduce(operator.iand, finalquery)).to_queryset()

                if exp_gte is not None and not exp_gte == '' and exp_lte is not None and not exp_lte == '':

                    response = response.filter(
                        year_of_experience__gte=exp_gte, year_of_experience__lte=exp_lte)
                if skills is not None and not skills == '' and level is not None and not level == '':
                    response = response.filter(
                        skills__name__icontains=skills, skills__level=level)
                    print(response)

            else:
                response = Employee.objects.all().order_by('-id')

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)
