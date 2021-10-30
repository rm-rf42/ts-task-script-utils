from .utils import map_offset_to_seconds


class PipelineConfig:
    def __init__(
        self,
        day_first=None,
        year_first=None,
        tz_dict={},
        fold=None
    ):

        self.day_first = day_first
        self.year_first = year_first
        self.tz_dict = tz_dict
        self.tz_dict_seconds = map_offset_to_seconds(tz_dict)
        self.fold = fold

    def __str__(self):
        return (
            f"day_first={self.day_first}, "
            f"year_first={self.year_first}, "
            f"fold={self.fold}, "
            f"tz_dict={self.tz_dict}"
        )

DEFAULT_PIPELINE_CONFIG = PipelineConfig()
