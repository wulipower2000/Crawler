import click
import io
import traceback
import sys
from loguru import logger
from Crawler import II_Crawler
from PythonFunctionMonitor.Doctor import porcess_decartor

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
@porcess_decartor('./config/monitor_prometheus.json')
def main(date, path):

    try:
        II_scraper = II_Crawler(date, f"{path}/{date}/II.csv")
        II_scraper.run()
    except:
        fp = io.StringIO()
        traceback.print_exc(file=fp)
        logger.error(fp.getvalue())
        sys.exit(2)

if __name__ == "__main__":

    main()
