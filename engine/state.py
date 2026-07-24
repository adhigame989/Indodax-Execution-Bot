from enum import Enum


class BotState(Enum):

    STANDBY = "STANDBY"

    WAIT_ENTRY = "WAIT_ENTRY"

    BUYING = "BUYING"

    VERIFY_ORDER = "VERIFY_ORDER"

    HOLDING = "HOLDING"

    TP_ZONE = "TP_ZONE"

    TRAILING = "TRAILING"

    SELLING = "SELLING"

    FINISHED = "FINISHED"

    PAUSED = "PAUSED"
