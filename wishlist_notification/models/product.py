from dataclasses import dataclass
from decimal import Decimal

@dataclass
class AMZNProduct:
    '''
    The Vehicle object contains lots of vehicles
    :param arg: The arg is used for ...
    :type arg: str
    :param `*args`: The variable arguments are used for ...
    :param `**kwargs`: The keyword arguments are used for ...
    :ivar arg: This is where we store arg
    :vartype arg: str
    '''
    iid: str = ""
    title: str = ""
    url: str = ""
    img_url: str = ""
    price: str = "" # json serialisation
    new_price: str = ""
    pct_change: str = ""
