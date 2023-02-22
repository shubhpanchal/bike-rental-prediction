from collections import namedtuple
from datetime import datetime
import uuid
from rentals.config.configuration import Configuration
from rentals.logger import logging, get_log_file_name
from rentals.exception import RentalException
from threading import Thread
from typing import List

from multiprocessing import Process
from rentals.entity.artifact_entity import DataIngestionArtifact
from rentals.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from rentals.component.data_ingestion import DataIngestion
import os, sys

class Pipeline(Thread):

    def __init__(self, config : Configuration)-> None:
        try:
            os.makedirs(config.training_pipeline_config.artifact_dir, exist_ok=True)
            super().__init__(daemon=False, name = "pipeline")
            self.config = config
        except Exception as e:
            raise RentalException(e, sys) from e
        
    def strat_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise RentalException(e,sys) from e
        

    def run_pipeline(self):
        try:
            logging.info(f" Starting Pipeline...")
        except Exception as e:
            raise RentalException(e, sys) from e