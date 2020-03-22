# image_catalog

#####build:
docker-compose up --build  

#####apply migrations:
docker-compose exec image_catalog bash  
python manage.py migrate

#####tests:
docker-compose exec image_catalog bash  
python manage.py test

#####routes:
0.0.0.0:8000/catalog/  
0.0.0.0:8000/upload/  
0.0.0.0:8000/detail/<int:image_id>  
0.0.0.0:8000/delete/<int:image_id>  