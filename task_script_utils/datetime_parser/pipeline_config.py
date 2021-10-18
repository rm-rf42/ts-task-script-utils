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
        self.fold = fold

    @classmethod
    def from_dict(cls, config_dict):
        assert type(config_dict) == dict, TypeError(
            "config_dict must be a python dict.")

        config = {
            "day_first": config_dict.get("day_first", None),
            "year_first": config_dict.get("year_first", None),
            "formats_list": config_dict.get("formats_list", []),
            "tz_dict": config_dict.get("tz_dict",{}),
            "fold": config_dict.get("fold", 0)
        }
        return cls(**config)
