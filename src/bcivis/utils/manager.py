from src.bcivis.io.loader import BIDSDataLoader

class DatasetManager:
    def __init__(self, config):
        self.config = config
        self.loaders = []

    def load_all(self):
        subjects = self.config.get("subjects") or [self.config.get("subject")]
        runs = self.config.get("runs") or [self.config.get("run")]
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
