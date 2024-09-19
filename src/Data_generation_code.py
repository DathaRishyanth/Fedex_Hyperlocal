import random
import pandas as pd
from geopy.distance import geodesic
from geopy.point import Point

def generate_random_points(center_point, radius, num_points):
    points = []
    for _ in range(num_points):
        distance = random.uniform(0, radius)
        angle = random.uniform(0, 360)
        destination = geodesic(kilometers=distance).destination(center_point, angle)
        points.append((destination.latitude, destination.longitude))
    return points

cities = [
    (1, "Mumbai", 19.0760, 72.8777, 10, "Mumbai", "Maharashtra", "India", 20411000),
    (2, "Delhi", 28.7041, 77.1025, 15, "New Delhi", "Delhi", "India", 31870000),
    (3, "Bangalore", 12.9716, 77.5946, 12, "Bangalore", "Karnataka", "India", 12000000),
    (4, "Hyderabad", 17.3850, 78.4867, 10, "Hyderabad", "Telangana", "India", 10000000),
    (5, "Chennai", 13.0827, 80.2707, 10, "Chennai", "Tamil Nadu", "India", 11000000),
    (6, "Kolkata", 22.5726, 88.3639, 8, "Kolkata", "West Bengal", "India", 14900000),
    (7, "Ahmedabad", 23.0225, 72.5714, 10, "Ahmedabad", "Gujarat", "India", 8200000),
    (8, "Pune", 18.5204, 73.8567, 10, "Pune", "Maharashtra", "India", 7200000),
    (9, "Jaipur", 26.9124, 75.7873, 12, "Jaipur", "Rajasthan", "India", 3500000),
    (10, "Lucknow", 26.8467, 80.9462, 10, "Lucknow", "Uttar Pradesh", "India", 3300000)
]

operators = [
    (1, "Swiggy", "help@swiggy.in","12345678","JohnDae","Swiggy pvt ltd","Bangalore","India", "9 AM - 9 PM"),
    (2, "Zomato", "help@zomato.in","12345678","JohnDae","Zomato pvt ltd","Bangalore","India", "9 AM - 9 PM"),
    (3, "Dunzo", "help@dunzo.in","12345678","JohnDae","Dunzo pvt ltd","Bangalore","India", "9 AM - 9 PM"),
    (4, "BigBasket", "help@bigbasket.in","12345678","JohnDae","BigBasket pvt ltd","Bangalore","India", "9 AM - 9 PM"),
    (5, "Amazon", "help@amazon.in","12345678","JohnDae","Amazon pvt ltd","Bangalore","India", "9 AM - 9 PM"),
    (6, "Zepto", "help@zepto.in","12345678","JohnDae","Zepto pvt ltd","Bangalore","India", "9 AM - 9 PM"),
    (7, "Flipkart", "help@flipkart.in","12345678","JohnDae","Flipkart pvt ltd","Bangalore","India", "9 AM - 9 PM"),
    (8, "Blinkit", "help@blinkit.in","12345678","JohnDae","Blinkit pvt ltd","Bangalore","India", "9 AM - 9 PM")
]

items_for_inventory = [
    (1, "Laptop", "Electronics", "2kg", "30x20x3 cm", "Fragile"),
    (2, "Chair", "Furniture", "5kg", "50x50x90 cm", "Handle with care"),
    (3, "Mobile Phone", "Electronics", "0.2kg", "15x7x1 cm", "Fragile"),
    (4, "Book", "Stationary", "0.5kg", "25x18x5 cm", "None"),
    (5, "Refrigerator", "Appliances", "50kg", "180x80x70 cm", "Heavy"),
    (6, "T-shirt", "Clothing", "0.1kg", "30x20x2 cm", "None"),
    (7, "Television", "Electronics", "8kg", "100x60x10 cm", "Fragile"),
    (8, "Shoes", "Footwear", "1kg", "35x20x15 cm", "None"),
    (9, "Washing Machine", "Appliances", "60kg", "150x100x80 cm", "Heavy"),
    (10, "Air Conditioner", "Appliances", "30kg", "90x60x50 cm", "Fragile")
]

store_data = []
store_id = 1
for city_id, city_name, lat, lon, radius, district, state, country, population in cities:
    center_point = Point(lat, lon)
    stores = generate_random_points(center_point, radius=radius, num_points=100)
    operator = random.choice(operators)
    operator_id = operator[0]
    
    for store in stores:
        store_data.append([
            store_id,
            operator_id,
            city_id,
            store[0],
            store[1],
            f"store{store_id}@{city_name.lower()}.com",
            random.randint(9000000000, 9999999999),
            "9 AM - 9 PM",
            random.randint(50, 500)
        ])
        store_id += 1

customers = []
for i in range(1, 51):
    city = random.choice(cities)
    customers.append((
        i, 
        random.uniform(city[2] - 0.05, city[2] + 0.05),  # Latitude around the city center
        random.uniform(city[3] - 0.05, city[3] + 0.05),  # Longitude around the city center
        f"Customer_{i} Address",  # Address
        city[0],  # City_id
        f"9 AM - 12 PM" if i % 2 == 0 else "3 PM - 6 PM"  # Preferred delivery window
    ))

# Data for Vehicles
vehicles = []
for i in range(1, 21):
    vehicles.append((
        i, 
        f"Owner_{i}", 
        f"Driver_{i}", 
        random.choice(operators)[0],  # Vehicle Operator (Operator_id)
        random.randint(1, 5),  # Vehicle Type_id
        f"AB{i:02d}XY1234",  # Number Plate
        random.choice(["Petrol", "Diesel", "Electric"]),  # Fuel_Type
        random.choice(["Active", "Inactive"])  # Vehicle_Status
    ))

# Data for Vehicle Types
vehicle_types = [
    (1, "Bike", "50kg", "50cm", "30cm", "30cm"),
    (2, "Small Van", "200kg", "100cm", "100cm", "80cm"),
    (3, "Large Van", "500kg", "200cm", "150cm", "150cm"),
    (4, "Truck", "1000kg", "500cm", "300cm", "250cm"),
    (5, "Mini Truck", "750kg", "300cm", "200cm", "200cm")
]

# Data for Drivers
drivers = []
for i in range(1, 16):
    drivers.append((
        i,
        f"Driver_{i}",
        random.choice(cities)[1],  # City
        f"PAN{i:05d}",
        f"Aadhar{i:012d}",
        f"DL{i:08d}",
        random.sample(range(1, 6), random.randint(1, 3))  # List of vehicle types for DL
    ))


cities_df = pd.DataFrame(cities, columns=[
    "City_id", "Name", "Center_latitude", "Center_longitude", "Radius", 
    "District", "State", "Country", "Population"
])
cities_df.to_csv("indian_cities.csv", index=False)

operators_df = pd.DataFrame(operators, columns=[
    "Operator_id", "Name", "Contact_email", "Contact_phone", "Contact_person_name", 
    "Registered_name", "Registered_address", "Operates_in", "Operating_Hours"
])
operators_df.to_csv("indian_quick_commerce_operators.csv", index=False)

stores_df = pd.DataFrame(store_data, columns=[
    "Store_id", "Operator_id", "City_id", "Location_latitude", "Location_longitude", 
    "Contact_email", "Contact_mobile", "Operating_Hours", "Inventory_capacity"
])
stores_df.to_csv("indian_stores.csv", index=False)

drivers_df = pd.DataFrame(drivers, columns=[
    "Id", "Name", "City", "PAN", "Aadhar", "DL_number", "DL_for_vehicle_types"
])
drivers_df["DL_for_vehicle_types"] = drivers_df["DL_for_vehicle_types"].apply(lambda x: ','.join(map(str, x)))

# Create DataFrames and save as CSVs
items_df = pd.DataFrame(items_for_inventory, columns=[
    "Id", "Name", "Type", "Weight", "Dimensions", "Special_Handling_Requirements"
])
items_df.to_csv("items_for_inventory.csv", index=False)

customers_df = pd.DataFrame(customers, columns=[
    "Customer_id", "Location_latitude", "Location_longitude", "Address", "City_id", "Preferred_Delivery_Window"
])
customers_df.to_csv("customers.csv", index=False)

vehicles_df = pd.DataFrame(vehicles, columns=[
    "Vehicle_id", "Owner", "Driver", "Vehicle_operator", "Vehicle_type_id", "Number_plate", "Fuel_Type", "Vehicle_Status"
])
vehicles_df.to_csv("vehicles.csv", index=False)

vehicle_types_df = pd.DataFrame(vehicle_types, columns=[
    "Id", "Name", "Weight_Carrying_Capacity", "Container_Space_Length", "Container_Space_Breadth", "Container_Space_Height"
])
vehicle_types_df.to_csv("vehicle_types.csv", index=False)

drivers_df.to_csv("drivers.csv", index=False)

cities_df.to_csv("DataGenerated/indian_cities.csv", index=False)
operators_df.to_csv("DataGenerated/indian_quick_commerce_operators.csv", index=False)
stores_df.to_csv("DataGenerated/indian_stores.csv", index=False)
drivers_df.to_csv("DataGenerated/drivers.csv", index=False)

items_df.to_csv("DataGenerated/items_for_inventory.csv", index=False)
customers_df.to_csv("DataGenerated/customers.csv", index=False)
vehicles_df.to_csv("DataGenerated/vehicles.csv", index=False)
vehicle_types_df.to_csv("DataGenerated/vehicle_types.csv", index=False)

print("Data has been saved to indian_cities.csv, indian_quick_commerce_operators.csv, and indian_stores.csv.")
