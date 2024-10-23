import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import logging


class InfluxDBHandler(logging.Handler):
    def __init__(self, url, token, org, bucket='dbhandler'):
        super().__init__()
        self.client = influxdb_client.InfluxDBClient(
            url=url,
            token=token,
            org=org
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = bucket
        self.org = org

    def emit(self, record):
        try:
            log_entry = self.format(record)
            point = influxdb_client.Point("log_memory") \
                .tag("level", record.levelname) \
                .field("message", log_entry)
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)

        except Exception as e:
            print(f"Failed to write log to InfluxDB: {e}")
