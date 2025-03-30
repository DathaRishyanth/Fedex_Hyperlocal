import pandas as pd
import numpy as np
import os
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from math import sqrt, radians, sin, cos, atan2
from scipy.optimize import linear_sum_assignment  # To use Hungarian algorithm

@dataclass
class AvailableDriver:
    driver_id: str
    name: str
    latitude: float
    longitude: float
    city_id: str
    vehicle_id: str
    company_id : int
    is_available: bool
    max_delivery_radius: float
    pending_orders_count: int
    availability_time: Optional[datetime] = None 

# Constants
RADIUS_OF_EARTH = 6371  # Radius of the Earth in kilometers

# KDTreeNode class for KD-Tree construction
class KDTreeNode:
    def __init__(self, point, driver_id, left=None, right=None):
        self.point = point  # A tuple representing (latitude, longitude)
        self.driver_id = driver_id
        self.left = left
        self.right = right

# Rect class for bounding box in KD-Tree
class Rect:
    def __init__(self, min_point, max_point):
        self.min_point = min_point  # (min_latitude, min_longitude)
        self.max_point = max_point  # (max_latitude, max_longitude)

# KDTree class with nearest neighbor search
class KDTree:
    def __init__(self, points_with_ids):
        if not points_with_ids:
            self.root = None
        else:
            self.root = self.build_tree(points_with_ids)

    def build_tree(self, points_with_ids, depth=0):
        if not points_with_ids:
            return None
        
        k = len(points_with_ids[0][0])
        axis = depth % k
        points_with_ids.sort(key=lambda x: x[0][axis])
        median_index = len(points_with_ids) // 2
        
        return KDTreeNode(
            point=points_with_ids[median_index][0],
            driver_id=points_with_ids[median_index][1],
            left=self.build_tree(points_with_ids[:median_index], depth + 1),
            right=self.build_tree(points_with_ids[median_index + 1:], depth + 1)
        )

    def distance(self, point1, point2):
        lat1, lon1 = map(radians, point1)
        lat2, lon2 = map(radians, point2)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return RADIUS_OF_EARTH * c

# Function to construct cost matrix for all drivers and requests
def construct_cost_matrix(drivers, stores, requests):
    n_drivers = len(drivers)
    n_requests = len(requests)
    cost_matrix = np.full((n_drivers, n_requests), np.inf)
    
    for i, driver in enumerate(drivers):
        for j, request in requests.iterrows():
            store_id = request['store_id']
            store = next((s for s in stores if s['store_id'] == store_id), None)
            if store is None:
                continue
            driver_location = (driver.latitude, driver.longitude)
            store_location = (store['location_latitude'], store['location_longitude'])
            request_location = (request['Delivery_latitude'], request['Delivery_longitude'])
            
            distance_driver_to_store = kd_tree.distance(driver_location, store_location)
            distance_store_to_request = kd_tree.distance(store_location, request_location)
            total_distance = distance_driver_to_store + distance_store_to_request
            
            cost_matrix[i, j] = total_distance
    
    return cost_matrix

# Main algorithm to find the optimal assignment
def assign_drivers_to_requests(drivers, requests, stores, kd_tree):
    # Construct the cost matrix where each entry represents the distance for a driver-request pair
    cost_matrix = construct_cost_matrix(drivers, stores, requests)
    
    # Solve the assignment problem using the Hungarian algorithm
    driver_indices, request_indices = linear_sum_assignment(cost_matrix)
    
    # Extract assignments and calculate total travel distance
    assignments = []
    total_travel_distance = 0
    for d_idx, r_idx in zip(driver_indices, request_indices):
        driver = drivers[d_idx]
        request = requests.iloc[r_idx]
        store_id = request['store_id']
        store = next((s for s in stores if s['store_id'] == store_id), None)
        
        driver_location = (driver.latitude, driver.longitude)
        store_location = (store['location_latitude'], store['location_longitude'])
        request_location = (request['Delivery_latitude'], request['Delivery_longitude'])
        
        distance_driver_to_store = kd_tree.distance(driver_location, store_location)
        distance_store_to_request = kd_tree.distance(store_location, request_location)
        total_distance = distance_driver_to_store + distance_store_to_request
        total_travel_distance += total_distance
        
        assignments.append({
            "Request_id": request['Request_id'],
            "Assigned_driver_id": driver.driver_id,
            "Distance_from_driver_to_store": distance_driver_to_store,
            "Distance_store_to_customer": distance_store_to_request,
            "Total_distance": total_distance
        })
    
    return assignments, total_travel_distance

# Load data and run the algorithm for each instance
for instance in range(1, 4):
    try:
        # Fix path resolution by using os.path.join
        base_path = os.path.join(os.path.dirname(__file__), "..", "..", "Data", "Generated_datasets_and_input_instance", f"Instance_{instance}", "Generated_data")
        
        # Load drivers data
        available_drivers = []
        available_drivers_df = pd.read_csv(os.path.join(base_path, "available_drivers.csv"))
        for index, row in available_drivers_df.iterrows():
            available_drivers.append(
                AvailableDriver(
                    row["driver_id"],
                    row["name"],
                    row["latitude"],
                    row["longitude"],
                    row["city_id"],
                    row["vehicle_id"],
                    row["company_id"],
                    row["is_available"],
                    row["max_delivery_radius"],
                    row["pending_orders_count"],
                    row["availability_time"]
                )
            )
        
        # Load requests data
        requests = pd.read_csv(os.path.join(base_path, "requests.csv"))
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"Current working directory: {os.getcwd()}")  # Add this for debugging
        print(f"Attempted path: {base_path}")  # Add this for debugging
        continue

    # Check columns
    required_columns_drivers = ['city_id', 'latitude', 'longitude', 'driver_id', "company_id"]
    required_columns_requests = ['Delivery_latitude', 'Delivery_longitude', 'Delivery_city_id', 'Request_id', "company_id", "store_id"]
    
    if not all(column in available_drivers_df.columns for column in required_columns_drivers):
        print(f"Error: Required columns {required_columns_drivers} not found in available_drivers.csv for instance {instance}")
        continue
    if not all(column in requests.columns for column in required_columns_requests):
        print(f"Error: Required columns {required_columns_requests} not found in requests.csv for instance {instance}")
        continue

    # Create a dictionary of KD-Trees for each city
    print(f"Creating KD-Trees for instance {instance}")
    city_kd_trees = {}
    for city_id, group in available_drivers_df.groupby('city_id'):
        drivers = group[['latitude', 'longitude', 'driver_id', "company_id"]].values
        driver_ids = group['driver_id'].values
        driver_points_with_ids = [(tuple(driver), driver_id) for driver, driver_id in zip(drivers, driver_ids)]
        kd_tree = KDTree(driver_points_with_ids)
        city_kd_trees[city_id] = kd_tree

    # Load stores data
    stores_df = pd.read_csv(os.path.join(base_path, "stores.csv"))
    stores = stores_df.to_dict('records')

    # Run optimal assignment and save results
    assignments, total_travel_distance = assign_drivers_to_requests(available_drivers, requests, stores, kd_tree)
    assignments_df = pd.DataFrame(assignments)
    assignments_df.sort_values(by='Total_distance', inplace=True)
    
    # Create output directory using os.path.join
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "Algo_Output", "Algo_Optimal", f"Instance_{instance}")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save results
    output_file = os.path.join(output_dir, "assignments.csv")
    assignments_df.to_csv(output_file, index=False)
    print(f"Assignments for Instance {instance} saved to {output_file} with total travel distance {total_travel_distance}")