from enum import Enum


class BotState(Enum):

    # ==========================
    # SYSTEM
    # ==========================

    STANDBY = "STANDBY"

    PAUSED = "PAUSED"

    # ==========================
    # ENTRY
    # ==========================

    WAIT_ENTRY = "WAIT_ENTRY"

    BUYING = "BUYING"

    VERIFY_BUY = "VERIFY_BUY"

    # ==========================
    # POSITION
    # ==========================

    HOLDING = "HOLDING"

    TP_ZONE = "TP_ZONE"

    TRAILING = "TRAILING"

    # ==========================
    # EXIT
    # ==========================

    SELLING = "SELLING"

    VERIFY_SELL = "VERIFY_SELL"

    FINISHED = "FINISHED"

    FAILED = "FAILED"
