from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class City:
    city_id: int
    name: str
    center_latitude: float
    center_longitude: float
    radius: float
    district: str
    state: str
    country: str
    population: int


@dataclass
class Operator:
    operator_id: int
    name: str
    contact_email: str
    contact_phone: str
    contact_person_name: str
    registered_name: str
    registered_address: str
    maximum_order_per_vehicle: int
    operates_in: List[int]  # List of city IDs where the operator operates
    operating_hours: tuple[int, int]  # (start_hour, end_hour)


@dataclass
class Store:
    store_id: int
    operator_id: int
    city_id: int
    location_latitude: float
    location_longitude: float
    contact_email: str
    contact_mobile: str
    operating_hours: tuple[int, int]  # (start_hour, end_hour)
    maximum_weight_capacity: Optional[float]  # Capacity in kilograms, if applicable


@dataclass
class InventoryItem:
    item_id: int
    name: str
    item_type: str
    weight: float
    dimensions: tuple[float, float, float]  # (length, breadth, height)
    special_handling_requirements: List[str]  # Any specific requirements for handling this item


@dataclass
class Customer:
    customer_id: int
    location_latitude: float
    location_longitude: float
    address: str
    city_id: int
    preferred_delivery_window: Optional[tuple[str, str]] = None  # e.g., ("9 AM", "12 PM")


@dataclass
class Vehicle:
    vehicle_id: int
    owner: str
    driver: str
    vehicle_operator: int
    vehicle_type_id: int
    number_plate: str
    fuel_type: str
    vehicle_status: str


@dataclass
class VehicleType:
    id: int
    name: str
    weight_carrying_capacity: float  # Maximum weight the vehicle can carry in kilograms
    container_space_length: float
    container_space_breadth: float
    container_space_height: float


@dataclass
class Driver:
    id: int
    name: str
    city: str
    pan: str
    aadhar: str
    dl_number: str
    dl_for_vehicle_types: List[int]  # List of vehicle type IDs the driver is authorized to operate


@dataclass
class VehicleOperator:
    id: int
    name: str
    pan: str
    aadhar: str
    city: str
    address: str
    rating: Optional[float] = None  # Optional rating for the vehicle operator


@dataclass
class ShipmentRequest:
    shipment_id: str
    customer_id: str
    facility_id: str
    vehicle_id: str
    pickup_time: datetime
    delivery_time: datetime
    items_shipped: List[str]
    shipment_value: float
    payment_status: str


@dataclass
class UnservicedRequest:
    request_id: str
    customer_id: str
    requested_items: List[str]
    requested_weight: float
    requested_date: datetime
    reason_unserviced: str
    retry_attempts: int
    last_attempted_date: Optional[datetime] = None
    expected_service_date: Optional[datetime] = None


@dataclass
class AvailableDriver:
    driver_id: str
    name: str
    latitude: float
    longitude: float
    city_id: str
    vehicle_id: str
    current_status: str
    availability_time: Optional[datetime] = None  # Time when the driver is next available
    max_delivery_radius: float
    pending_orders_count: int


@dataclass
class ActiveOrder:
    current_status: str  # e.g., "Delivered", "Dispatched", "Out for Delivery"
    last_updated: datetime
    tracking_url: Optional[str] = None  # URL for tracking the order, if available
    delivery_window: Optional[str] = None  # e.g., "9 AM - 12 PM"
