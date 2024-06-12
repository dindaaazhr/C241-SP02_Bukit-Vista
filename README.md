# API DOCUMENTATION

## Overview
This documentation provides details about the API endpoints available for interacting with our service. Below, you will find the descriptions, methods, request body formats, and response structures for each endpoint.

## Endpoints

### 1. Connect
This endpoint is used to check the connectivity status of the API.
- Method: `GET`

- URL: `/`

Body Request

- Format: `None required`

- Response
  ```json
  {
    "status": "SUCCESS", 
    "message": "Success connect"
  }
  ```

### Predict
- Method: `POST`

- URL: `/predict`

Body Request

- Format: `JSON`
  ```json
  {
    "unit_id": "test" 
  }
  ```

- Response
  ```json
  {
    "createdAt": "2024-06-12T13:57:54.458891",
    "id": "9e258b43-c9cd-4161-a230-fa3a8f90105b",
    "result": [
      {
        "area_distance_to_airport": 1.2,
        "area_name": "Dummy Area 1",
        "area_regency_city": 5,
        "avg_price_per_day": 500000.00,
        "bathroom": 1.0,
        "bedroom": 2.0,
        "beds": 2.0,
        "cluster_label": 2,
        "google_map_link": "https://goo.gl/maps/DummyLink1",
        "lat": -8.123456,
        "lng": 115.123456,
        "property_id": "PR1234",
        "property_name": "Dummy Property 1",
        "property_type": 3.0,
        "total_guest_capacity": 4.0,
        "type_desc": "Apartment",
        "unit_id": "UN1234",
        "unit_name": "Unit 1"
      },
      {
        "area_distance_to_airport": 2.5,
        "area_name": "Dummy Area 2",
        "area_regency_city": 7,
        "avg_price_per_day": 750000.00,
        "bathroom": 2.0,
        "bedroom": 3.0,
        "beds": 3.0,
        "cluster_label": 3,
        "google_map_link": "https://goo.gl/maps/DummyLink2",
        "lat": -8.654321,
        "lng": 115.654321,
        "property_id": "PR5678",
        "property_name": "Dummy Property 2",
        "property_type": 4.0,
        "total_guest_capacity": 6.0,
        "type_desc": "Villa",
        "unit_id": "UN5678",
        "unit_name": "Unit 2"
      },
      {
        "area_distance_to_airport": 3.8,
        "area_name": "Dummy Area 3",
        "area_regency_city": 9,
        "avg_price_per_day": 1000000.00,
        "bathroom": 3.0,
        "bedroom": 4.0,
        "beds": 4.0,
        "cluster_label": 4,
        "google_map_link": "https://goo.gl/maps/DummyLink3",
        "lat": -8.987654,
        "lng": 115.987654,
        "property_id": "PR91011",
        "property_name": "Dummy Property 3",
        "property_type": 5.0,
        "total_guest_capacity": 8.0,
        "type_desc": "House",
        "unit_id": "UN91011",
        "unit_name": "Unit 3"
      }
    ],
    "status": "SUCCESS"
  }
  ```
