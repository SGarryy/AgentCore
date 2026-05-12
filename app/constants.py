"""Application constants."""

from enum import Enum


class Intent(str, Enum):
    """Valid intents for task routing."""

    HR = "hr_agent"
    FINANCE = "finance_agent"
    IT = "it_agent"
    SALES = "sales_agent"
    OPERATIONS = "operations_agent"


class Priority(str, Enum):
    """Task priority levels."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Status(str, Enum):
    """Task execution status."""

    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"


# ML/Router Configuration
TF_IDF_MAX_FEATURES = 5000
TF_IDF_NGRAM_RANGE = (1, 2)
MODEL_TEST_SIZE = 0.15
MODEL_RANDOM_STATE = 42

# API Configuration
MAX_INPUT_LENGTH = 2000
MIN_INPUT_LENGTH = 1
API_REQUEST_TIMEOUT = 30
RATE_LIMIT_PER_MINUTE = 60

# ID Prefixes
TICKET_ID_PREFIX = "TKT"
TASK_ID_PREFIX = "TSK"
REQUEST_ID_PREFIX = "REQ"
LEAD_ID_PREFIX = "LEAD"
OPS_ID_PREFIX = "OPS"

# Timeouts (seconds)
OLLAMA_TIMEOUT = 60
DATABASE_TIMEOUT = 30
EXTERNAL_API_TIMEOUT = 30

# Default values
DEFAULT_DUPLICATES_RANGE = (1, 5)
DEFAULT_LEADS_RANGE = (3, 10)
