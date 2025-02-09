import os
import random
import time
import uuid

from confluent_kafka import SerializingProducer
import simplejson as json
from datetime import datetime, timedelta

from jobs.constants import *

current_time = datetime.now()
current_location = LONDON_COORDINATES.copy()

random.seed(42)


def get_current_time():
    global current_time
    current_time += timedelta(seconds=random.randint(30, 60))
    return current_time


def simulate_vehicle_movement():
    global current_location

    # move towards birmingham
    current_location['latitude'] += LATITUDE_INCREMENT
    current_location['longitude'] += LONGITUDE_INCREMENT

    # add some randomness to simulate actual road travel
    current_location['latitude'] += random.uniform(-0.005, 0.005)
    current_location['longitude'] += random.uniform(-0.005, 0.005)

    return current_location


def extract_vehicle_info(device_id):
    location = simulate_vehicle_movement()

    return {
        'id': uuid.uuid4(),
        'device_id': device_id,
        'timestamp': get_current_time().isoformat(),
        'location': (location['latitude'], location['longitude']),
        'speed': random.uniform(10, 40),
        'direction': 'North-East',
        'dealer': 'BMW',
        'model': 'C500',
        'year': 2024,
        'fuelType': 'Hybrid'
    }


def extract_gps_info(device_id, timestamp, vehicle_type='private'):
    return {
        'id': uuid.uuid4(),
        'device_id': device_id,
        'timestamp': timestamp,
        'speed': random.uniform(0, 40),  # km/h
        'direction': 'NorthEast',
        'vehicle_type': vehicle_type
    }


def extract_traffic_camera_info(device_id, timestamp, location, camera_id):
    return {
        'id': uuid.uuid4(),
        'device_id': device_id,
        'camera_id': camera_id,
        'location': location,
        'timestamp': timestamp,
        'snapshot': 'Base64EncodedString'
    }


def extract_weather_info(device_id, timestamp, location):
    return {
        'id': uuid.uuid4(),
        'device_id': device_id,
        'location': location,
        'timestamp': timestamp,
        'temperature': random.uniform(-5, 26),
        'weather_condition': random.choice(['Sunny', 'Cloudy', 'Rainy', 'Snowy']),
        'precipitation': random.uniform(0, 25),
        'wind_speed': random.uniform(0, 100),
        'humidity': random.randint(0, 100),
        'air_quality_index': random.uniform(0, 500)
    }


def extract_emergency_incident_info(device_id, timestamp, location):
    return {
        'id': uuid.uuid4(),
        'device_id': device_id,
        'incident_id': uuid.uuid4(),
        'type': random.choice(['Accident', 'Fire', 'Medical', 'Police', 'None']),
        'timestamp': timestamp,
        'location': location,
        'status': random.choice(['Active', 'Resolved']),
        'description': "Watch out!! There grand theft auto in the city"
    }


def json_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not Json serializable')


def delivery_report(err, msg):
    if err is not None:
        print(f'Message deliver failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


def produce_data_to_kafka(producer, topic, data):
    producer.produce(
        topic,
        key=str(data['id']),
        value=json.dumps(data, default=json_serializer).encode('utf-8'),
        on_delivery=delivery_report
    )
    producer.flush()


def simulate_journey(producer, device_id):
    while True:
        vehicle_data = extract_vehicle_info(device_id)
        timestamp = vehicle_data['timestamp']
        location = vehicle_data['location']

        gps_data = extract_gps_info(device_id, timestamp)
        traffic_data = extract_traffic_camera_info(device_id, timestamp, location, 'camera_stalking')
        weather_data = extract_weather_info(device_id, timestamp, location)
        emergency_data = extract_emergency_incident_info(device_id, timestamp, location)

        if location[0] >= BIRMINGHAM_COORDINATES['latitude'] and location[1] <= BIRMINGHAM_COORDINATES['longitude']:
            print('Vehicle has reached to Birmingham. Simulation ending...')
            break

        produce_data_to_kafka(producer, VEHICLE_TOPIC, vehicle_data)
        produce_data_to_kafka(producer, GPS_TOPIC, gps_data)
        produce_data_to_kafka(producer, TRAFFIC_TOPIC, traffic_data)
        produce_data_to_kafka(producer, WEATHER_TOPIC, weather_data)
        produce_data_to_kafka(producer, EMERGENCY_TOPIC, emergency_data)
        time.sleep(5)


if __name__ == '__main__':
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda error: print(f'Kafka error: {error}')
    }
    producer = SerializingProducer(producer_config)
    try:
        simulate_journey(producer, 'Lamborghini')

    except KeyboardInterrupt:
        print('Simulation ended by users')
    except Exception as e:
        print(f'Unexpected error occurred: {e}')
