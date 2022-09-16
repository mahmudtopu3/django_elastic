# Django Elastic - An example project to learn ElasticSearch with Django Rest Framework
![](https://miro.medium.com/max/2400/1*fkEPSDBvqNwtpjaaFceyww.png)

### _Implemented object field, nested field, manytomany field filtering_
#### Using fuzzy logic even if the search keyword is misspelled or a long sentence, the results will be matched. [See query 2]


### Used Packages
- Django==4.1.1
- djangorestframework==3.13.1
- elasticsearch==7.13.4
- elasticsearch-dsl==7.4.0
- django-elasticsearch-dsl==7.2.2
##### _Note: we have used elastic search version 7.17.5 so python packages are also 7.x.x_

#
##### _To install elastic search please follow my article https://mahmudtopu3.medium.com/play-with-elastic-search-with-python-django-on-ubuntu-part-1-d063af7edc00_
## Installation
---
1. Clone Project from github and add database information and elasticsearch information in settings.py
2. Create virtualenv
      ```sh
    $ python -m venv venv
    ```
3. Activate Virtualenv
   ```sh
    $ venv/Scripts/activate
    ```

4. Make migration
    ```sh
    $ python manage.py makemigrations
    ```
5. Migrate
    ```sh
    $ python manage.py migrate
    ```
6. Create Superuser
    ```sh
    $ python manage.py createsuperuser
    ```
8. Start Server
    ```sh
    $ python manage.py runserver
    ```
8. Load Demo data
    ```sh
    $ python manage.py loaddata hrm.json
    ```
8. Index data to elastic search
    ```sh
    $ python manage.py search_index --rebuild
    ```
####  Settings.py 
  ```sh
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://elastic:123456@localhost:9200/',   
        # also can be basic auth url
    },
}
```
####  To check mapping of
  ```sh
http://localhost:9200/hrm_index/_mapping
```
## Queries 
    http://127.0.0.1:8000/hrm/all-employees?search=software&company=Daffodil%20Family
    http://127.0.0.1:8000/hrm/all-employees?search=softwae
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
   
    
    
#### Please send your pull requests if you want to contribute.
#### For professional support mail me at mahmudtopu3@gmail.com

