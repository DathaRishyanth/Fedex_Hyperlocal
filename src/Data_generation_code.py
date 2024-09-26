import random
import pandas as pd
from geopy.distance import geodesic
from geopy.point import Point
from models import *  # Assuming models contain all necessary classes
from datetime import datetime, timedelta
import os

#Paths to config files
PATHS_TO_CONFIGS = []

i = 1
while True:
    path = f"../datasets/generated_datasets_and_input_instance/Instance_{i}/config.txt"
    try:
        with open(path, 'r') as file:
            PATHS_TO_CONFIGS.append(path)
    except FileNotFoundError:
        break
    i += 1

# Load config data from config files
config_data = []
for path in PATHS_TO_CONFIGS:
    with open(path, 'r') as file:
        config_data.append(file.readlines())



# Load city data from CSV
cities_df = pd.read_csv("../datasets/Raw_data/indian-cities.csv")
def generate_data(data):
        """Generate data for the Quick Commerce system."""
        # Constants
        NUM_CITIES = int(data[0].strip())
        NUM_OPERATORS = int(data[1].strip())
        NUM_STORES_PER_OPERATOR = int(data[2].strip())
        NUM_CUSTOMERS = int(data[3].strip())
        NUM_VEHICLES = int(data[4].strip())
        NUM_VEHICLE_TYPES = int(data[5].strip())
        NUM_ITEMS_FOR_INVENTORY = int(data[6].strip())
        NUM_SHIPMENT_REQUESTS = int(data[7].strip())

        print(f"Generating data for Instance {Index_Of_Config} with the following parameters:")
        print(f"NUM_CITIES: {NUM_CITIES}")
        print(f"NUM_OPERATORS: {NUM_OPERATORS}")
        print(f"NUM_STORES_PER_OPERATOR: {NUM_STORES_PER_OPERATOR}")
        print(f"NUM_CUSTOMERS: {NUM_CUSTOMERS}")
        print(f"NUM_VEHICLES: {NUM_VEHICLES}")
        print(f"NUM_VEHICLE_TYPES: {NUM_VEHICLE_TYPES}")
        print(f"NUM_ITEMS_FOR_INVENTORY: {NUM_ITEMS_FOR_INVENTORY}")
        print(f"NUM_SHIPMENT_REQUESTS: {NUM_SHIPMENT_REQUESTS}")


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
            store_id = 1  # Track the store_id across all operators and cities
            
            for i in range(NUM_OPERATORS):  # Loop through each operator
                for city_id in operators[i].operates_in:  # Loop through each city the operator operates in
                    store_points = generate_random_points(
                        Point(city_list[city_id - 1].center_latitude, city_list[city_id - 1].center_longitude),
                        radius=city_list[city_id - 1].radius, 
                        num_points=NUM_STORES_PER_OPERATOR
                    )
                    
                    for k in range(NUM_STORES_PER_OPERATOR):  # Create stores for this operator in this city
                        store = Store(
                            store_id=store_id,
                            operator_id=i + 1,
                            city_id=city_id,
                            location_latitude=store_points[k][0],
                            location_longitude=store_points[k][1],
                            contact_email=f"store{store_id}@{city_list[city_id - 1].name.lower()}.com",
                            contact_mobile=random.randint(9000000000, 9999999999),
                            start_time=datetime.combine(datetime.today(), datetime.strptime("09:00", "%H:%M").time()),
                            end_time=datetime.combine(datetime.today(), datetime.strptime("21:00", "%H:%M").time()),
                            inventory_capacity=random.randint(1000, 5000)
                        )
                        
                        # Add store_id to the operator's list_of_stores and increment store_id
                        operators[i].list_of_stores.append(store_id)
                        stores.append(store)
                        store_id += 1  # Increment the store ID to avoid duplicates
            
            return stores

        stores = generate_stores()  # Populate stores list

        def generate_customers():
            """Generate customer data with random locations within city boundaries."""
            customers = []
            for i in range(1, NUM_CUSTOMERS + 1):
                city_id = random.choice(range(1, NUM_CITIES + 1))
                city = city_list[city_id - 1]
                distance = random.uniform(0, city.radius)
                angle = random.uniform(0, 360)
                destination = geodesic(kilometers=distance).destination(Point(city.center_latitude, city.center_longitude), angle)
                customer = Customer(
                    customer_id=i,
                    city_id=city_id,
                    location_latitude=destination.latitude,
                    location_longitude=destination.longitude,
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
            vehicle_type_names=["two wheeler","three wheeler closed","three wheeler open","four wheeler closed","four wheeler open"]
            vehicle_types = []
            for i in range(1, NUM_VEHICLE_TYPES + 1):
                vehicle_type = VehicleType(
                    id=i,
                    name=vehicle_type_names[i],
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
            for city in city_list:
                for i in range(0,len(city.list_of_operators)):
                    for j in range(1, 6):
                        driver = Driver(
                            id=len(drivers) + 1,
                            name=f"Driver_{len(drivers) + 1}",
                            city=city.name,
                            pan=f"ABCDE{random.randint(1000, 9999)}F",
                            aadhar=f"{random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
                            dl_number=f"DL-{random.randint(1000, 9999)}-{random.randint(100000, 999999)}",
                            dl_for_vehicle_types=random.sample(range(1, NUM_VEHICLE_TYPES + 1), j),
                            Available=random.choice([True, False]),
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

        def Available_drivers():
            available_drivers = []
            for driver in drivers:
                if driver.Available:
                    available_drivers.append(driver)
            return available_drivers

        available_drivers = Available_drivers()  # Populate available drivers list

     


        # Save all generated data to respective CSV files
        operators_df = pd.DataFrame([vars(operator) for operator in operators])
        stores_df = pd.DataFrame([vars(store) for store in stores])
        drivers_df = pd.DataFrame([vars(driver) for driver in drivers])
        items_df = pd.DataFrame([vars(item) for item in items_for_inventory])
        customers_df = pd.DataFrame([vars(customer) for customer in customers])
        vehicles_df = pd.DataFrame([vars(vehicle) for vehicle in vehicles])
        vehicle_types_df = pd.DataFrame([vars(vehicle_type) for vehicle_type in vehicle_types])
        requests_df = pd.DataFrame([vars(request) for request in shipment_requests])
        available_drivers_df=pd.DataFrame([vars(driver) for driver in available_drivers])
        active_requests_df=pd.DataFrame()
        unserviced_requests_df=pd.DataFrame()
        completed_requests_df=pd.DataFrame()

        # Check if output directory exists
        output_directory = f"../datasets/Generated_datasets_and_input_instance/Instance_{Index_Of_Config}/Generated_data"
        os.makedirs(output_directory, exist_ok=True)

        # Save data to CSV files
        try:
            city_df.to_csv(f"{output_directory}/cities.csv", index=False)
            operators_df.to_csv(f"{output_directory}/operators.csv", index=False)
            stores_df.to_csv(f"{output_directory}/stores.csv", index=False)
            drivers_df.to_csv(f"{output_directory}/drivers.csv", index=False)
            items_df.to_csv(f"{output_directory}/items.csv", index=False)
            customers_df.to_csv(f"{output_directory}/customers.csv", index=False)
            vehicles_df.to_csv(f"{output_directory}/vehicles.csv", index=False)
            vehicle_types_df.to_csv(f"{output_directory}/vehicle_types.csv", index=False)
            requests_df.to_csv(f"{output_directory}/shipment_requests.csv", index=False)
            available_drivers_df.to_csv(f"{output_directory}/available_drivers.csv", index=False)
            active_requests_df.to_csv(f"{output_directory}/active_requests.csv", index=False)
            unserviced_requests_df.to_csv(f"{output_directory}/unserviced_requests.csv", index=False)
            completed_requests_df.to_csv(f"{output_directory}/completed_requests.csv", index=False)
        except Exception as e:
            print(f"Error saving data to CSV files: {e}")
    
# Generate data for each configuration
Index_Of_Config = 1
for data in config_data:
    generate_data(data)
    print(f"Data has been saved to the respective CSV files for Instance {Index_Of_Config}.")
    Index_Of_Config += 1


print("Data has been saved to the respective CSV files.")
