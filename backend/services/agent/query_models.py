from enum import Enum


class Intent(Enum):

    EXPLAIN_SYMBOL = "explain_symbol"

    FIND_CALLERS = "find_callers"

    FIND_CALLEES = "find_callees"

    IMPACT_ANALYSIS = "impact_analysis"

    FIND_FILE = "find_file"

    UNKNOWN = "unknown"