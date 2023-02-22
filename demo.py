from rentals.pipeline.pipeline import Pipeline
from rentals.exception import RentalException
from rentals.logger import logging
from rentals.config.configuration import Configuration
from rentals.component.data_ingestion import DataIngestion
import os, sys

def main():
    try:
        config_path = os.path.join("config", "config.yaml")
        pipeline = Pipeline(Configuration(config_file_path=config_path))
        pipeline.start()
        logging.info(f"Testing the Data Ingestion Pipeline...")
        data_ingestion_config = Configuration().get_data_ingestion_config()
        print(data_ingestion_config)
        
    except Exception as e:
        raise RentalException(e, sys) from e