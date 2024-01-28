import Requestor
import Parser
import Sink
from loguru import logger

class II_Crawler:
    def __init__(self, yyyymmdd: str, output_path: str):
        self.request = Requestor.II_Request(yyyymmdd)
        self.sink = Sink.csv()
        self.output_path = output_path

    def run(self):
        # Step 1: Send request and get response
        logger.info('========== Step 1: get request ==========')
        response = self.request.get_request()

        # Step 2-1: Parse HTML to DataFrame
        logger.info('========== Step 2: Parse to Pandas DataFrame ==========')
        self.parser = Parser.II_Parser(response)
        df = self.parser.parse_html_to_dataframe()

        # Step 2-2: Check data
        self.parser.check_data(df)

        # Step 3: Sink data to CSV
        logger.info('========== Step 3: sink data ==========')
        self.sink.sink(df, self.output_path)
