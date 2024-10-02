import pandas as pd
import numpy as np
import sys
import os
from math import sqrt, radians, sin, cos, atan2
from dataclasses import dataclass

@dataclass
class AvailableDriver:
    driver_id: str
    name: str
    latitude: float
    longitude: float
    city_id: str
    vehicle_id: str
    operators_id: str
    is_available: bool
    max_delivery_radius: float
    pending_orders_count: int
    availability_time: None  # Time when the driver is next available

RADIUS_OF_EARTH = 6371  # Radius of the Earth in kilometers

class KDTreeNode:
    def __init__(self, point, driver_id, left=None, right=None):
        self.point = point  # A tuple representing (latitude, longitude)
        self.driver_id = driver_id
        self.left = left
        self.right = right

class Rect:
    def __init__(self, min_point, max_point):
        self.min_point = min_point  # (min_latitude, min_longitude)
        self.max_point = max_point  # (max_latitude, max_longitude)

    def trim_left(self, cd, point):
        """Trim the left side of the bounding box based on the current dimension (cd) and point."""
        if cd == 0:  # Latitude
            return Rect(self.min_point, (point[0], self.max_point[1]))
        else:  # Longitude
            return Rect((self.min_point[0], self.min_point[1]), (self.max_point[0], point[1]))

    def trim_right(self, cd, point):
        """Trim the right side of the bounding box based on the current dimension (cd) and point."""
        if cd == 0:  # Latitude
            return Rect((point[0], self.min_point[1]), self.max_point)
        else:  # Longitude
            return Rect((self.min_point[0], point[1]), (self.max_point[0], self.max_point[1]))

class KDTree:
    def __init__(self, points_with_ids):
        """Initialize the KD-Tree with a list of points and driver IDs."""
        if not points_with_ids:
            self.root = None  # No data to build the tree
        else:
            self.root = self.build_tree(points_with_ids)

    def build_tree(self, points_with_ids_and_orders, depth=0):
        """Recursively build the KD-Tree from a list of points with driver IDs and orders count."""
        if not points_with_ids_and_orders:
            return None
        
        # Alternate between splitting on latitude and longitude
        k = len(points_with_ids_and_orders[0][0])  # k=2 for (latitude, longitude)
        axis = depth % k
        
        # Sort points and choose median as pivot
        points_with_ids_and_orders.sort(key=lambda x: x[0][axis])  # Sort by the axis (latitude or longitude)
        median_index = len(points_with_ids_and_orders) // 2
        
        # Create node and construct subtrees
        return KDTreeNode(
            point=points_with_ids_and_orders[median_index][0],
            driver_id=points_with_ids_and_orders[median_index][1],
            left=self.build_tree(points_with_ids_and_orders[:median_index], depth + 1),
            right=self.build_tree(points_with_ids_and_orders[median_index + 1:], depth + 1)
        )

    def distance(self, point1, point2):
        """Calculate the great-circle distance between two points on the Earth."""
        lat1, lon1 = map(radians, point1)
        lat2, lon2 = map(radians, point2)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        return RADIUS_OF_EARTH * c

    def point_to_rect_distance(self, point, rect):
        """Calculate the minimum distance from a point to the bounding box defined by the rectangle."""
        lat, lon = point
        min_lat, min_lon = rect.min_point
        max_lat, max_lon = rect.max_point

        # Compute the closest point on the rectangle to the point
        closest_lat = max(min_lat, min(lat, max_lat))
        closest_lon = max(min_lon, min(lon, max_lon))

        # Calculate the distance from the point to this closest point
        return sqrt((lat - closest_lat) ** 2 + (lon - closest_lon) ** 2)

    def nearest_neighbor(self, Q, T, cd, best, best_dist, BB):
        """Find the nearest neighbor to the query point Q in the KD-Tree T."""
        if T is None or self.point_to_rect_distance(Q, BB) > best_dist:
            return best, best_dist  # Return the current best if bounding box is too far

        # Calculate the distance from Q to the current node's point
        dist = self.distance(Q, T.point)
        
        # Update best point and distance if a better point is found
        if dist < best_dist and available_drivers[T.driver_id - 1].is_available:
            best = T
            best_dist = dist

        # Determine the next dimension (cd) to explore
        next_cd = (cd + 1) % len(Q)

        # Visit the subtrees in the most promising order
        if Q[cd] < T.point[cd]:
            # Explore left subtree first
            best, best_dist = self.nearest_neighbor(Q, T.left, next_cd, best, best_dist, BB.trim_left(cd, T.point))
            best, best_dist = self.nearest_neighbor(Q, T.right, next_cd, best, best_dist, BB.trim_right(cd, T.point))
        else:
            # Explore right subtree first
            best, best_dist = self.nearest_neighbor(Q, T.right, next_cd, best, best_dist, BB.trim_right(cd, T.point))
            best, best_dist = self.nearest_neighbor(Q, T.left, next_cd, best, best_dist, BB.trim_left(cd, T.point))

        return best, best_dist

# Loop through each instance
for instance in range(1, 4):
    try:
        available_drivers = []
        available_drivers_df = pd.read_csv(f"quick_commerce/Data/Generated_datasets_and_input_instance/Instance_{instance}/Generated_data/available_drivers.csv")
        for index, row in available_drivers_df.iterrows():
            available_drivers.append(
                AvailableDriver(
                    row["driver_id"],
                    row["name"],
                    row["latitude"],
                    row["longitude"],
                    row["city_id"],
                    row["vehicle_id"],
                    row["operators_id"],
                    row["is_available"],
                    row["max_delivery_radius"],
                    row["pending_orders_count"],
                    row["availability_time"]
                )
            )
        requests = pd.read_csv(f"quick_commerce/Data/Generated_datasets_and_input_instance/Instance_{instance}/Generated_data/requests.csv")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        continue  # Skip to the next instance if there's an error

    # Check if necessary columns exist in both CSVs
    required_columns_drivers = ['city_id', 'latitude', 'longitude', 'driver_id']
    required_columns_requests = ['Delivery_latitude', 'Delivery_longitude', 'Delivery_city_id', 'Request_id']

    if not all(column in available_drivers_df.columns for column in required_columns_drivers):
        print(f"Error: Required columns {required_columns_drivers} not found in available_drivers.csv for instance {instance}")
        continue

    if not all(column in requests.columns for column in required_columns_requests):
        print(f"Error: Required columns {required_columns_requests} not found in requests.csv for instance {instance}")
        continue

    # Create a dictionary of KD-Trees for each city
    city_kd_trees = {}

    for city_id, group in available_drivers_df.groupby('city_id'):
        driver_locations_with_ids = [(tuple([row['latitude'], row['longitude']]), row['driver_id']) for _, row in group.iterrows() if row['is_available']]
        if driver_locations_with_ids:
            city_kd_trees[city_id] = KDTree(driver_locations_with_ids)

    assignments = []

    # Iterate through each request
    for _, request in requests.iterrows():
        request_location = (request['Delivery_latitude'], request['Delivery_longitude'])
        city_id = request['Delivery_city_id']

        
        # Find the KD-Tree for the request's city
        kd_tree = city_kd_trees.get(city_id)
        
        if kd_tree is None or kd_tree.root is None:
            print(f"No drivers available in city with id {city_id} for instance {instance}")
            continue  # No drivers available in this city

        # Initialize bounding box for nearest neighbor search
        bounding_box = Rect((request['Delivery_latitude'] - 0.1, request['Delivery_longitude'] - 0.1),
                            (request['Delivery_latitude'] + 0.1, request['Delivery_longitude'] + 0.1))

        # Find the nearest driver
        best_driver_node, best_distance = kd_tree.nearest_neighbor(request_location, kd_tree.root, 0, None, float('inf'), bounding_box)

        if best_driver_node:
            best_driver = available_drivers[best_driver_node.driver_id - 1]
            # Assign driver to the request and mark as unavailable
            best_driver.is_available = False
            assignments.append({
                "Request_id": request['Request_id'],
                "Assigned_driver_id": best_driver.driver_id,
                "Assigned_Driver_latitude": best_driver.latitude,
                "Assigned_Driver_longitude": best_driver.longitude,
                "Request_latitude": request['Delivery_latitude'],
                "Request_longitude": request['Delivery_longitude'],
                "Distance": best_distance
            })

    # Save assignments to a CSV file
    assignments_df = pd.DataFrame(assignments)
    assignments_df.to_csv(f"quick_commerce/Algo_Output/Instance_{instance}/assignments.csv", index=False)

    print(f"Assignments for Instance {instance} saved to assignments.csv")
