from rentals.entity.config_entity import DataIngestionConfig
import os, sys
from rentals.exception import RentalException
from rentals.logger import logging
from rentals.entity.artifact_entity import DataIngestionArtifact
import zipfile
import numpy as np
from six.moves import urllib
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:
    def __init__(self, data_ingestion_config : DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Starting Data Ingestion. {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise RentalException(e, sys)
        
    def download_rental_data(self,):
        try:
            # Extracting data from remote url
            download_url = self.data_ingestion_config.dataset_download_url

            # Folder location to download file
            zip_download_dir = self.data_ingestion_config.zip_download_dir
            os.makedirs(zip_download_dir, exist_ok=True)
            rental_file_name = os.path.basename(download_url)
            zip_file_path = os.path.join(zip_download_dir,rental_file_name)

            logging.info(f"Downloading File from :[{download_url}] into : [{zip_file_path}]")
            urllib.request.urlretrieve(download_url,zip_file_path)
            logging.info(f"File : [{zip_file_path}] has been successfully downloaded...")
            return zip_file_path
        except Exception as e:
            raise RentalException(e, sys) from e
            
    def extract_zip_file(self, zip_file_path):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir, exist_ok=True)

            logging.info(f"Extracting Zip File : [{zip_file_path}] into dir : [{raw_data_dir}]")

            with zipfile.ZipFile(zip_file_path,'r') as zip_file:
                zip_file.extractall(path= raw_data_dir)
            logging.info(f"Extraction Completed")

        except Exception as e:
            raise RentalException(e, sys) from e
        
    def split_data(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = os.listdir(raw_data_dir)[0]
            rental_file_path = os.path.join(raw_data_dir, file_name)
            logging.info(f"Reading CSV File : [{rental_file_path}]")
            rental_data_frame = pd.read_csv(rental_file_path)
            logging.info(f"Splitting Data into Train and Test...")

            strat_train_set = None
            strat_test_set = None
            split = StratifiedShuffleSplit(n_splits= 1, test_size = 0.2, random_state = 42)

            for train_index, test_index in split.split(rental_data_frame, rental_data_frame["Rented Bike Count"]):
                strat_train_set = rental_data_frame.loc[train_index].drop(["Rented Bike Count"], axis=1)
                strat_test_set = rental_data_frame.loc[test_index].drop(["Rented Bike Count"], axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, file_name)

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                logging.info(f"Exporting Training Dataset to [{train_file_path}]")
                strat_train_set.to_csv(train_file_path, index= False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                logging.info(f"Extracting Test Dataset to [{test_file_path}]")
                strat_test_set.to_csv(test_file_path, index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path, 
                                                            test_file_path=test_file_path,
                                                            is_ingested=True,
                                                            message=f"Data Ingestion Completed Successfully...")
            logging.info(f"Data Ingestion Artifact : [{data_ingestion_artifact}]")
            return data_ingestion_artifact
        
        except Exception as e:
            raise RentalException(e, sys) from e
        
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            zip_file_path = self.download_rental_data()
            self.extract_zip_file(zip_file_path=zip_file_path)
            return self.split_data()
        except Exception as e:
            raise RentalException(e, sys) from e
        
    def __del__(self):
        logging.info(f"{'>>'*20} Data Ingestion Log Completed {'<<'*20} \n\n")