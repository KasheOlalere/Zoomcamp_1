# Zoomcamp_1
Week one assignment of the data talks zoomcamp

Question 1. Understanding docker first run
docker run -it --entrypoint bash python:3.12.8

Question 2. Understanding Docker networking and docker-compose
### Script for creating and running the green taxi ingest image
docker build -t green_ingest:1 .

docker run -it \
  --network=assignment_default \
green_ingest:1 \
  --user=postgres \
  --password=postgres \
  --host=db \
  --port=5432 \
  --db=ny_taxi \
  --table_name=green_taxi \
  --url='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz'  

#### Script for creating and running the zone ingest image
docker build -t zone_ingest:1 .

docker run -it \
  --network=assignment_default \
zone_ingest:1 \
  --user=postgres \
  --password=postgres \
  --host=db \
  --port=5432 \
  --db=ny_taxi \
  --table_name=zones \
  --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

```sql
-- Question 3. Trip Segmentation Count

SELECT count(1)
FROM public.green_taxi
WHERE trip_distance >= 1;

SELECT count(1)
FROM public.green_taxi
WHERE trip_distance > 1 AND trip_distance <= 3;

SELECT count(1)
FROM public.green_taxi
WHERE trip_distance > 3 AND trip_distance <= 7;

SELECT count(1)
FROM public.green_taxi
WHERE trip_distance > 7 AND trip_distance <= 10;

SELECT count(1)
FROM public.green_taxi
WHERE trip_distance > 10;
```

```sql
-- Question 4. Longest trip for each day
SELECT lpep_pickup_datetime
FROM public.green_taxi
WHERE trip_distance = 
	(SELECT MAX (trip_distance)
	 FROM public.green_taxi);
```

```sql
-- Question 5. Three biggest pickup zones
SELECT z."Zone","PULocationID", SUM(total_amount)
FROM public.green_taxi AS g
JOIN zones AS z
ON g."PULocationID" = z."LocationID"
WHERE DATE(lpep_pickup_datetime) = '2019-10-18'
GROUP BY 1,2
ORDER BY 3 DESC
LIMIT 3;
```

```sql
-- Question 6. Largest tip
SELECT 
    dz."Zone" AS dropoff_zone,
    MAX(g.tip_amount) AS max_tip_amount
FROM public.green_taxi AS g
JOIN zones AS pz  -- Join for pickup zone
    ON g."PULocationID" = pz."LocationID"
JOIN zones AS dz  -- Join for dropoff zone
    ON g."DOLocationID" = dz."LocationID"
WHERE pz."Zone" = 'East Harlem North'  
  AND g.lpep_pickup_datetime >= '2019-10-01'
  AND g.lpep_pickup_datetime < '2019-11-01'
GROUP BY dz."Zone"
ORDER BY max_tip_amount DESC
LIMIT 1;
```
