import click
from loguru import logger
from Crawler import II_Crawler
from application_monitor.Exporter import doctor

trace = logger.add(
    sink="./crawler.log",
    retention="1 days",
    rotation="500MB",
    encoding="utf-8",
    compression='zip',
    format="{time:YYYY-MM-DD HH:mm:ss} {level} From {module}.{function} : {message}"

)


@logger.catch
@click.command(no_args_is_help=True)
@click.option('-d', '--date', 'date', help='--date yyyymmdd')
@click.option('-p', '--path', 'path', help='--path [path/to/data/folder]')
@doctor('./monitor.json')
def main(date, path):

    II_scraper = II_Crawler(date, f"{path}/{date}/II.csv")
    II_scraper.run()

if __name__ == "__main__":

    main()
