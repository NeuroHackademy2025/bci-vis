import mne
import yaml
from mne_bids import BIDSPath, read_raw_bids

class BIDSDataLoader:
    def __init__(self, bids_root, subject, task, session=None, run=None, config=None, verbose=False):
        self.bids_root = bids_root
        self.subject = subject
        self.task = task
        self.session = session
        self.run = run
        self.config = config or {}
        self.verbose = verbose
    
        self.raw = None
        self.events = None
        self.event_id = None

    def load(self):
        bids_path = BIDSPath(
            root=self.bids_root,
            subject=self.subject,
            session=self.session,
            task=self.task,
            run=self.run,
            suffix="eeg",
            extension=".edf"
        )
        if self.verbose:
            print(f"Loading BIDS data from: {bids_path}")

        self.raw = read_raw_bids(bids_path=bids_path, verbose=self.verbose)
        self.events, self.event_id = mne.events_from_annotations(self.raw)

        if self.verbose:
            print("Original MNE event_id:", self.event_id)

        
    def summary(self):
        print(f"Subject: {self.subject}, Task: {self.task}, Run: {self.run}")
        print(f"Data shape: {self.raw.get_data().shape}")
        print(f"Sampling rate: {self.raw.info['sfreq']} Hz")
        print(f"Number of events: {len(self.events)}")
        print(f"Event ID map: {self.event_id}")

    def get_raw(self):
        return self.raw

    def get_events(self):
        return self.events, self.event_id

    @staticmethod
    def from_config(config_path, verbose=False):
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)

        return BIDSDataLoader(
            bids_root=cfg["bids_root"],
            subject=cfg["subject"],
            task=cfg["task"],
            run=cfg["run"],
            session=cfg.get("session", None),
            config=cfg,
            verbose=verbose
        )