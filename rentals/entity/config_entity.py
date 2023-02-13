from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig",["dataset_download_url", "zip_download_dir",
                                "raw_data_dir", "ingested_train_dir", "ingested_test_dir"])