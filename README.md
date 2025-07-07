This is a Taiwan public weather bureau data ETL project.
In this project , it will pull data like
````
record_time : recording the observation time
station_id : weather observation station id 
station_name :  weather observation station name
station_latitude : weather observation station latitude
station_longitude : weather observation station longitude
country_name : the country name in Chinese 
town_name : the town name in Chinese
weather_description : weather description like :
````

Deploy commands : (in kubernetes or minikube)
```
eval $(minikube docker-env) # If you are using minikube.
kubectl apply -f mysql-secret.yaml # Config map with your mysql password.

docker build -t weather-records-job:v1.0 .
kubectl apply -f cronjob.yaml
```