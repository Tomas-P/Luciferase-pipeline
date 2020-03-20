import enum

class ParameterName(enum.Enum):
    DATADIR = "data dir"
    MASK = "segment img"
    GROUPS = "group archive"
    NORM = "normalize?"
    ALIGN = "align?"
    USE_EXIST = "use existing rois?"
    SAVE_GEN = "save generated rois?"
    EXIST_ROI = "existing roi archive"
    NEW_ROI = "new roi archive"
    BG = "background"
    START = "start time"
    INTERVAL = "interval"
    HOUR = "hour"
    MINUTE = "minute"

Pname = ParameterName
