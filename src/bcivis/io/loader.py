from scipy.io import loadmat
import numpy as np
import mne

class MatMIDataLoader:
    def __init__(self, filepath: str, montage="standard_1020"):
        self.filepath = filepath
        self.montage = montage
        self.raw = None
        self.events = None
        self.labels = None
        self.trial_onsets = None

    def load(self):
        mat = loadmat(self.filepath)
        data = mat['data']

        X = data['X'][0, 0]               # shape: (n_samples, n_channels)
        fs = int(data['fs'][0, 0][0, 0])  # scalar
        channel_names = [ch[0] for ch in data['channel'][0, 0][0]]  # list of str

        ch_types = ['eeg'] * len(channel_names)  # all EEG for now

        info = mne.create_info(ch_names=channel_names, sfreq=fs, ch_types=ch_types)
        self.raw = mne.io.RawArray(X.T, info)  # MNE expects [n_channels x n_samples]

        # Apply standard montage
        if self.montage is not None:
            self.raw.set_montage(self.montage, on_missing='warn')

        # Store trial metadata for later use
        self.labels = data['y'][0, 0].flatten()           # shape: (n_trials,)
        self.trial_onsets = data['trial'][0, 0].flatten() # shape: (n_trials,)

    def get_raw(self):
        return self.raw

    def get_labels(self):
        return self.labels

    def get_trial_onsets(self):
        return self.trial_onsets
