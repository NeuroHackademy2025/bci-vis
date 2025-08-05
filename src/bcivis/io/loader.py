import scipy.io
import numpy as np
import mne
import os
import yaml

class MatDataLoader:
    def __init__(self, filepath, config):
        self.filepath = filepath
        self.config = self._load_config(config)
        self.mat = None
        self.raw = None
        self.report = []
        self.labels = None
        self.trials = None

    def _load_config(self, config):
        if isinstance(config, str):  # path to .yaml
            with open(config, 'r') as f:
                return yaml.safe_load(f)
        elif isinstance(config, dict):
            return config
        else:
            raise ValueError("Config must be a dict or a path to a .yaml file.")

    def load(self):
        self.mat = scipy.io.loadmat(self.filepath, squeeze_me=True)


        # Debug: inspect the structure
        print("Mat keys:", list(self.mat.keys()))
        
        X = self._get_nested(self.config["data_key"])
        # Extract the first session data
        session_data = X[0].item()
        
        eeg_data = session_data[0]  
        fs = session_data[3]        
        class_names = session_data[4]  
        
        print("EEG data shape:", eeg_data.shape)
        print("Sampling frequency:", fs)
        print("Class names:", class_names)
        
        # Create channel names (assuming standard EEG montage)
        n_channels = eeg_data.shape[1]
        ch_names = [f'EEG{i+1:03d}' for i in range(n_channels)]
        
        # Transpose if needed: MNE expects (channels, samples)
        if eeg_data.shape[0] > eeg_data.shape[1]:
            eeg_data = eeg_data.T
        
        info = mne.create_info(ch_names=ch_names, sfreq=float(fs), ch_types=["eeg"] * n_channels)
        self.raw = mne.io.RawArray(eeg_data, info)

        if "montage" in self.config:
            self.raw.set_montage(self.config["montage"], on_missing="warn")

        if "labels_key" in self.config:
            self.labels = self._get_nested(self.config["labels_key"]).flatten()

        if "trials_key" in self.config:
            self.trials = self._get_nested(self.config["trials_key"]).flatten()

    def _get_nested(self, key_path):
        keys = key_path.split('.')
        obj = self.mat
        for key in keys:
            if isinstance(obj, dict):
                obj = obj.get(key)
            elif hasattr(obj, key):
                obj = getattr(obj, key)
            else:
                raise KeyError(f"Key '{key}' not found in path '{key_path}'")
        return obj

    def get_raw(self):
        return self.raw

    def get_labels(self):
        return self.labels

    def get_trial_onsets(self):
        return self.trials
