from dataclasses import dataclass
from typing import List, Optional,Tuple
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
    list_of_companies: List[int]
    list_of_operators: List[int]


@dataclass
class Company:
    company_id: int
    name: str
    contact_email: str
    contact_phone: str
    contact_person_name: str
    registered_name: str
    registered_address: str
    Max_number_of_orders_each_vehicle_can_take : int
    operates_in: List[int]
    start_time : datetime
    end_time : datetime
    list_of_operators: List[int]
    # list_of_cites = List[int]

@dataclass
class Operator:
    operator_id: int
    name: str
    contact_email: str
    contact_phone: str
    contact_person_name: str
    registered_name: str
    registered_address: str
    operates_in: List[int]
    list_of_stores: List[int]


@dataclass
class Store:
    store_id: int   
    operator_id: int 
    city_id: int
    location_latitude: float
    location_longitude: float
    contact_email: str
    contact_mobile: str
    start_time : datetime
    end_time : datetime 
    list_of_items: List[int]
    inventory_capacity: Optional[float] 
    
@dataclass
class InventoryItem:
    item_id: int
    name: str
    item_type: str 
    weight: float
    dimensions: tuple[float, float, float]
    special_handling_requirements: Optional[str] = None

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
    weight_carrying_capacity: float 
    container_space_length: float
    container_space_breadth: float
    container_space_height: float

@dataclass
class VehicleOperator:
    vehicle_operator_id: int
    Name: str
    PAN: str
    Aadhar:str
    City:str
    Address:str 
    Rating:float

@dataclass
class VehicleOwner:
    vehicle_owner_Id : int
    Name : str
    PAN : str
    Aadhar :str
    City:str
    Address :str
    Rating:float



@dataclass
class Driver:
    id: int
    name: str
    city: str
    pan: str
    aadhar: str
    dl_number: str
    dl_for_vehicle_types: List[int] 
    Available : bool
    rating: Optional[float] = None 


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
    company_id : int
    is_available: bool
    max_delivery_radius: float
    pending_orders_count: int
    availability_time: Optional[datetime] = None  

@dataclass
class Request:
    Request_id: str
    Customer_id : str
    company_id : int
    operator_id: int
    store_id: int
    Delivery_latitude: float
    Delivery_longitude: float
    Delivery_city_id: int
    Delivery_address: str
    items_in_this_request: List[Tuple]
    Request_placing_time: Optional[datetime] = None


@dataclass
class ActiveOrder:
    current_status: str  
    last_updated: datetime
    tracking_url: Optional[str] = None  
    delivery_window: Optional[str] = None 

@dataclass
class vehicle_operator:
    vehicle_operator_id: int
    name : str
    PAN: str
    Aadhar: str
    Adress: str
    Rating: float

@dataclass
class Inventory:
    id: int
    List_of_items: List[int]
    number_of_items_per_type: List[int]  
    total_number_of_items: int
    store_id: int
    operator_id: int
    city_id: int
