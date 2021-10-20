from .utils import map_offset_to_seconds


class PipelineConfig:
    def __init__(
        self,
        day_first=None,
        year_first=None,
        formats_list=[],
        tz_dict={},
        fold=0
    ):

        self.day_first = day_first
        self.year_first = year_first
        self.format_list = formats_list
        self.tz_dict = tz_dict
        self.tz_dict_seconds = map_offset_to_seconds(tz_dict)
        self.fold = fold
