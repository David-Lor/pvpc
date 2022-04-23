import pydantic
import datetime
import pathlib
import json
import os
import sys
try:
    import pvpc
except ModuleNotFoundError:
    sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
    import pvpc

String = pydantic.constr(strip_whitespace=True, min_length=1)


class Const:
    TODAY = "today"
    TOMORROW = "tomorrow"
    ENV_OUTPUT_DATE_FORMATTED = "PVPC_DATE_FORMATTED"
    ENV_OUTPUT_PCB_PATH_FORMATTED = "PVPC_OUTPUT_PCB_PATH_FORMATTED"
    ENV_OUTPUT_CM_PATH_FORMATTED = "PVPC_OUTPUT_CM_PATH_FORMATTED"


class Settings(pydantic.BaseSettings):
    # Paths must contain placeholders for year, month, date: {year}, {month}, {date}
    output_pcb_path: String
    output_cm_path: String
    date: datetime.date

    @pydantic.root_validator(pre=True)
    def _root_validator(cls, d):
        # Parse date
        date = d["date"]
        if date == Const.TODAY:
            date = datetime.date.today()
        elif date == Const.TOMORROW:
            date = datetime.date.today() + datetime.timedelta(days=1)
        elif isinstance(date, str):
            date = datetime.date.fromisoformat(date)
        d["date"] = date

        # Format paths
        for k in ["output_pcb_path", "output_cm_path"]:
            d[k] = _format_path(d[k], date)

        return d

    def export_github_env_variables(self):
        _export_github_env(Const.ENV_OUTPUT_DATE_FORMATTED, self.date.isoformat())
        _export_github_env(Const.ENV_OUTPUT_PCB_PATH_FORMATTED, self.output_pcb_path)
        _export_github_env(Const.ENV_OUTPUT_CM_PATH_FORMATTED, self.output_cm_path)

    class Config:
        env_prefix = "PVPC_"


class PVPCOutput(pydantic.BaseModel):
    day: datetime.date
    data: pvpc.PVPCHourlyPrice


def _export_github_env(key, value):
    github_env = os.getenv("GITHUB_ENV")
    if not github_env:
        return

    with open(github_env, "a") as f:
        f.write(f"\n{key}={value}\n")


def _write_file(path: str, content: str):
    # Create parent directories, if not exist
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        print(f"Writing on file {path}:\n{content}")
        f.write(content)


def _format_path(path: str, date: datetime.date) -> str:
    return path.format(
        year=date.year,
        month=str(date.month).zfill(2),
        day=str(date.day).zfill(2)
    )


def _export_json(day: datetime.date, location_data: pvpc.PVPCDay.PVPCDayData.PVPCDayByLocation, output_filename: str):
    output = PVPCOutput(
        day=day,
        data=location_data.hours
    )

    # dump, load and dump again the JSON for pretty-printing
    js = output.json()
    js = json.loads(js)
    js = json.dumps(js, indent=2)

    output_path = _format_path(output_filename, day)
    _write_file(output_path, js)


def main(date=None):
    settings_kwargs = dict()
    if date is not None:
        settings_kwargs["date"] = date
    settings = Settings(**settings_kwargs)
    settings.export_github_env_variables()

    print(f"Fetching PVPC data for {settings.date.isoformat()}...")
    data = pvpc.get_pvpc_day(settings.date)

    _export_json(settings.date, data.data.pcb, settings.output_pcb_path)
    _export_json(settings.date, data.data.cm, settings.output_cm_path)


if __name__ == '__main__':
    main()
