from src.bcivis.io.loader import BIDSDataLoader
from src.bcivis.preprocessing.cleaning_pipeline import preprocess_raw


class DatasetManager:
    def __init__(self, config):
        self.config = config
        self.loaders = []
        self.epochs_list = []


    def load_all(self):
        subjects = self.config.get("subjects") or [self.config.get("subject")]
        runs = self.config.get("runs") or [self.config.get("run")]

        if not subjects or not runs:
            raise ValueError("Subjects and runs must be specified in the configuration.")
        
        for subject in subjects:
            for run in runs:
                loader = BIDSDataLoader(
                    bids_root=self.config["bids_root"],
                    subject=subject,
                    task=self.config["task"],
                    run=run,
                    config=self.config,
                    verbose=self.config.get("verbose", False)
                )
                loader.load()
                self.loaders.append(loader)


    def preprocess_all(self):
        if not self.loaders:
            raise RuntimeError("No data loaders available. Please load data first.")
        
        for loader in self.loaders:
            raw = loader.get_raw()
            events, event_id = loader.get_events()
            epochs = preprocess_raw(raw, event_id, events, self.config)
            self.epochs_list.append(epochs)

    def get_all_epochs(self):
        return self.epochs_list