import pydantic
import datetime
import export_pvpc


class Settings(pydantic.BaseSettings):
    date_from: datetime.date
    date_to: datetime.date

    def date_iterator(self):
        delta = datetime.timedelta(days=1)
        current_date = self.date_from
        while current_date <= self.date_to:
            yield current_date
            current_date += delta


def main():
    settings = Settings()

    for date in settings.date_iterator():
        export_pvpc.main(date)


if __name__ == '__main__':
    main()
