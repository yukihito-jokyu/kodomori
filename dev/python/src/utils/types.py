from pydantic import BaseModel


class PinAndDistance(BaseModel):
    p1_p2: float
    p1_p3: float
    p1_p4: float
    p2_p3: float
    p2_p4: float
    p3_p4: float
    pin_1_x: float
    pin_1_y: float
    pin_2_x: float
    pin_2_y: float
    pin_3_x: float
    pin_3_y: float
    pin_4_x: float
    pin_4_y: float


class Pin(BaseModel):
    pin_1_x: float
    pin_1_y: float
    pin_2_x: float
    pin_2_y: float
    pin_3_x: float
    pin_3_y: float
    pin_4_x: float
    pin_4_y: float
