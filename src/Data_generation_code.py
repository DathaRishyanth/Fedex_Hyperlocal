import random
import pandas as pd
from geopy.distance import geodesic
from geopy.point import Point
from models import *  # Assuming models contain all necessary classes
from datetime import datetime, timedelta

# Constants for configuration
NUM_CITIES = 25
NUM_OPERATORS = 10
NUM_STORES_PER_OPERATOR = 10
NUM_CUSTOMERS = 10
NUM_SHIPMENT_REQUESTS = 10
NUM_VEHICLES = 50
NUM_VEHICLE_TYPES = 5
NUM_ITEMS_FOR_INVENTORY = 10

# Load city data from CSV
cities_df = pd.read_csv("../datasets/Raw_data/indian-cities.csv")

# Lists to hold generated data
city_list = []

def generate_cities():
    """Generate city data based on input CSV and store in city_list."""
    for i in range(NUM_CITIES):
        city = City(
            city_id=i + 1,
            name=cities_df.iloc[i]['City'],
            center_latitude=cities_df.iloc[i]['Lat'],
            center_longitude=cities_df.iloc[i]['Long'],
            radius=random.uniform(10, 30),  # Random radius between 10 and 30 km
            district=cities_df.iloc[i]['City'],
            state=cities_df.iloc[i]['State'],
            country=cities_df.iloc[i]['country'],
            population=random.randint(1_000_000, 15_000_000),  # Random population between 1M and 15M
            list_of_operators=[]
        )
        city_list.append(city)

generate_cities()  # Populate city_list
city_df = pd.DataFrame([vars(city) for city in city_list])  # Create DataFrame from city_list

def generate_random_points(center_point, radius, num_points):
    """Generate random geographic points within a specified radius of a center point."""
    points = []
    for _ in range(num_points):
        distance = random.uniform(0, radius)
        angle = random.uniform(0, 360)
        destination = geodesic(kilometers=distance).destination(center_point, angle)
        points.append((destination.latitude, destination.longitude))
    return points

def generate_operators():
    """Generate operator data with random attributes."""
    operators = []
    for i in range(NUM_OPERATORS):
        operator = Operator(
            operator_id=i + 1,
            name=f"Operator_{i + 1}",
            contact_email=f"help@operator{i + 1}.com",
            contact_phone=f"+91-{random.randint(9000000000, 9999999999)}",
            contact_person_name=f"Person_{i + 1}",
            registered_name=f"Registered_Operator_{i + 1}",
            registered_address=f"Address_{i + 1}",
            operates_in=random.sample(range(1, NUM_CITIES + 1),10),
            start_time=datetime.combine(datetime.today(), datetime.strptime("09:00", "%H:%M").time()),
            end_time=datetime.combine(datetime.today(), datetime.strptime("21:00", "%H:%M").time()),
            list_of_stores=[]
        )
        # Associate operator with the cities they operate in
        for j in operator.operates_in:
            city_list[j - 1].list_of_operators.append(operator.operator_id)
        operators.append(operator)
    return operators

operators = generate_operators()  # Populate operators list

def generate_stores():
    """Generate store data for each operator in their respective cities."""
    stores = []
    for i in range(NUM_OPERATORS):
        for j in operators[i].operates_in:
            store_points = generate_random_points(
                Point(city_list[j - 1].center_latitude, city_list[j - 1].center_longitude),
                radius=city_list[j - 1].radius, num_points=NUM_STORES_PER_OPERATOR
            )
            for k in range(NUM_STORES_PER_OPERATOR):
                store = Store(
                    store_id=i * NUM_STORES_PER_OPERATOR + k + 1,
                    operator_id=i + 1,
                    city_id=j,
                    location_latitude=store_points[k][0],
                    location_longitude=store_points[k][1],
                    contact_email=f"store{i * NUM_STORES_PER_OPERATOR + k + 1}@{city_list[j - 1].name.lower()}.com",
                    contact_mobile=random.randint(9000000000, 9999999999),
                    start_time=datetime.combine(datetime.today(), datetime.strptime("09:00", "%H:%M").time()),
                    end_time=datetime.combine(datetime.today(), datetime.strptime("21:00", "%H:%M").time()),
                    inventory_capacity=random.randint(1000, 5000)
                )
                # Avoid duplicate store IDs for the same operator
                if store.store_id not in operators[store.operator_id - 1].list_of_stores:
                    operators[store.operator_id - 1].list_of_stores.append(store.store_id)
                stores.append(store)
    return stores

stores = generate_stores()  # Populate stores list

def generate_customers():
    """Generate customer data with random locations within city boundaries."""
    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        city_id = random.choice(range(1, NUM_CITIES + 1))
        city = city_list[city_id - 1]
        customer = Customer(
            customer_id=i,
            city_id=city_id,
            location_latitude=random.uniform(city.center_latitude - city.radius, city.center_latitude + city.radius),
            location_longitude=random.uniform(city.center_longitude - city.radius, city.center_longitude + city.radius),
            address=f"Address_{i}",
            preferred_delivery_window=(f"{random.randint(1, 12)} AM", f"{random.randint(1, 12)} PM")
        )
        customers.append(customer)
    return customers

customers = generate_customers()  # Populate customers list

def generate_vehicles():
    """Generate vehicle data with random attributes."""
    vehicles = []
    for i in range(1, NUM_VEHICLES + 1):
        vehicle = Vehicle(
            vehicle_id=i,
            vehicle_type_id=random.choice(range(1, NUM_VEHICLE_TYPES + 1)),
            owner=f"Owner_{i}",
            driver=f"Driver_{i}",
            vehicle_operator=random.choice(range(1, NUM_OPERATORS + 1)),
            fuel_type=random.choice(["Petrol", "Diesel", "Electric"]),
            vehicle_status=random.choice(["Available", "In Use", "Under Maintenance"]),
            number_plate=f"AB-{random.randint(10, 99)}-AB-{random.randint(1000, 9999)}"
        )
        vehicles.append(vehicle)
    return vehicles

vehicles = generate_vehicles()  # Populate vehicles list

def generate_vehicle_types():
    """Generate vehicle type data with random attributes."""
    vehicle_types = []
    for i in range(1, NUM_VEHICLE_TYPES + 1):
        vehicle_type = VehicleType(
            id=i,
            name=f"Vehicle_Type_{i}",
            weight_carrying_capacity=round(random.uniform(500, 2000), 2),
            container_space_length=round(random.uniform(1, 10), 2),
            container_space_breadth=round(random.uniform(1, 10), 2),
            container_space_height=round(random.uniform(1, 10), 2)
        )
        vehicle_types.append(vehicle_type)
    return vehicle_types

vehicle_types = generate_vehicle_types()  # Populate vehicle types list

def generate_drivers():
    """Generate driver data with random attributes."""
    drivers = []
    for i in range(1, 51):
        driver = Driver(
            id=i,
            name=f"Driver_{i}",
            city=random.choice(city_list).city_id,
            pan=f"ABCD{random.randint(1000, 9999)}E",
            aadhar=f"{random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
            dl_number=f"DL-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            dl_for_vehicle_types=random.sample(range(1, 6), 3),
            Available=random.choice([True, False]),
            rating=round(random.uniform(1, 5), 1)
        )
        drivers.append(driver)
    return drivers

drivers = generate_drivers()  # Populate drivers list

def generate_items_for_inventory():
    """Generate inventory items with random attributes."""
    items = []
    for i in range(1, NUM_ITEMS_FOR_INVENTORY + 1):
        item = InventoryItem(
            item_id=i,
            name=f"Item_{i}",
            item_type=random.choice(["Electronics", "Clothing", "Food", "Furniture", "Books"]),
            weight=round(random.uniform(0.1, 10), 2),
            dimensions=(round(random.uniform(0.1, 1), 2), round(random.uniform(0.1, 1), 2), round(random.uniform(0.1, 1), 2)),
            special_handling_requirements=random.choice(["Fragile", "Perishable", "Hazardous", "None"])
        )
        items.append(item)
    return items

items_for_inventory = generate_items_for_inventory()  # Populate inventory items list

def generate_random_time(start_time, end_time):
    """Generate a random time between start_time and end_time."""
    time_delta = end_time - start_time
    random_seconds = random.randint(0, int(time_delta.total_seconds()))
    return start_time + timedelta(seconds=random_seconds)

def generate_shipment_requests():
    """Generate shipment requests with random pickup and delivery times."""
    shipment_requests = []
    start_time = datetime.combine(datetime.today(), datetime.strptime("09:00", "%H:%M").time())
    end_time = datetime.combine(datetime.today(), datetime.strptime("21:00", "%H:%M").time())

    for i in range(NUM_SHIPMENT_REQUESTS):
        pickup_time = generate_random_time(start_time, end_time)
        delivery_time = generate_random_time(pickup_time, end_time)

        shipment = ShipmentRequest(
            shipment_id=f"shipment_{i + 1}",
            facility_id=random.choice(range(1, NUM_STORES_PER_OPERATOR + 1)),
            customer_id=random.choice(range(1, NUM_CUSTOMERS + 1)),
            vehicle_id=random.choice(range(1, NUM_VEHICLES + 1)),
            pickup_time=pickup_time,
            delivery_time=delivery_time,
            items_shipped=random.sample(range(1, NUM_ITEMS_FOR_INVENTORY + 1), random.randint(1, 5)),
            shipment_value=random.uniform(100, 1000),
            payment_status=random.choice(["Paid", "Unpaid"])
        )
        shipment_requests.append(shipment)

    return shipment_requests

shipment_requests = generate_shipment_requests()  # Populate shipment requests list

# Save all generated data to respective CSV files
city_df.to_csv("../datasets/Generated_datasets/indian_cities.csv", index=True)
operators_df = pd.DataFrame([vars(operator) for operator in operators])
stores_df = pd.DataFrame([vars(store) for store in stores])
drivers_df = pd.DataFrame([vars(driver) for driver in drivers])
items_df = pd.DataFrame([vars(item) for item in items_for_inventory])
customers_df = pd.DataFrame([vars(customer) for customer in customers])
vehicles_df = pd.DataFrame([vars(vehicle) for vehicle in vehicles])
vehicle_types_df = pd.DataFrame([vars(vehicle_type) for vehicle_type in vehicle_types])
available_drivers_df=pd.DataFrame()
requests_df=pd.DataFrame()
active_requests_df=pd.DataFrame()
unserviced_requests_df=pd.DataFrame()
completed_requests_df=pd.DataFrame()


# Save data to CSV files
operators_df.to_csv("../datasets/Generated_datasets/operators.csv", index=True)
stores_df.to_csv("../datasets/Generated_datasets/stores.csv", index=True)
drivers_df.to_csv("../datasets/Generated_datasets/drivers.csv", index=True)
items_df.to_csv("../datasets/Generated_datasets/items_for_inventory.csv", index=True)
customers_df.to_csv("../datasets/Generated_datasets/customers.csv", index=True)
vehicles_df.to_csv("../datasets/Generated_datasets/vehicles.csv", index=True)
available_drivers_df.to_csv("../datasets/Generated_datasets/available_drivers.csv", index=True)
requests_df.to_csv("../datasets/Generated_datasets/requests.csv", index=True)
active_requests_df.to_csv("../datasets/Generated_datasets/active_requests.csv", index=True)
unserviced_requests_df.to_csv("../datasets/Generated_datasets/unserviced_requests.csv", index=True)
completed_requests_df.to_csv("../datasets/Generated_datasets/completed_requests.csv", index=True)

print("Data has been saved to the respective CSV files.")
