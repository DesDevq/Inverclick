from enum import Enum

class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

class IdentificationTypeEnum(str, Enum):
    CC = "CC"
    CE = "CE"
    PAS = "PAS"
    NIT = "NIT"
    PEP = "PEP"
    
