from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    feature_store_file_path: str


@dataclass
class DataValidationArtifact:
    report_file_path: str
