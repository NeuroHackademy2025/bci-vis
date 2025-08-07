import mne
import matplotlib.pyplot as plt


def plot_raw(raw, config):
    vis_cfg = config.get("visualization", {})
    duration = vis_cfg.get("duration", 60.0)
    start = vis_cfg.get("start", 0.0)
    n_channels = vis_cfg.get("n_channels", 8)
    scalings = vis_cfg.get("scalings", dict(eeg=1e2))
    show_events = vis_cfg.get("show_events", True)

    raw_copy = raw.copy()

    if not show_events:
        raw_copy.set_annotations(None)

    raw_copy.plot(duration=duration,
                  start=start,
                  scalings=scalings,
                  n_channels=n_channels,
                  title="Raw EEG Signal")

def plot_psd(raw, config):
    vis_cfg = config.get("visualization", {})
    fmin = vis_cfg.get("psd_fmin", 0.1)
    fmax = vis_cfg.get("psd_fmax", 45.0)
    average = vis_cfg.get("psd_average", True)

    raw.plot_psd(fmin=fmin, fmax=fmax, average=average)


def apply_montage(raw, config):
    vis_cfg = config.get("visualization", {})
    if vis_cfg.get("use_montage", False):
        montage_kind = vis_cfg.get("montage_kind", "standard_1020")
        montage = mne.channels.make_standard_montage(montage_kind)
        raw.set_montage(montage)


def plot_sensors(raw, config):
    vis_cfg = config.get("visualization", {})
    if vis_cfg.get("use_montage", False):
        raw.plot_sensors(kind='topomap', ch_type='eeg', show_names=True)


def plot_all_conditionwise(epochs, event_labels, config):
    vis_cfg = config.get("visualization", {})
    fmin = vis_cfg.get("psd_fmin", 1)
    fmax = vis_cfg.get("psd_fmax", 40)
    topomap_times = vis_cfg.get("topomap_times", [0.5, 1.0, 1.5])

    for label in event_labels:
        epochs[label].plot_image(picks="eeg", combine="mean")
        
        # Evoked
        evoked = epochs[label].average()
        if not evoked.info.get("dig"):
            montage_kind = vis_cfg.get("montage_kind", "standard_1020")
            evoked.set_montage(mne.channels.make_standard_montage(montage_kind))
        evoked.plot_topomap(times=topomap_times, ch_type='eeg')

        # PSD
        psds, freqs = epochs[label].compute_psd(fmin=fmin, fmax=fmax).get_data(return_freqs=True)
        psds_mean = psds.mean(axis=0)
        psds_std = psds.std(axis=0)

        plt.figure()
        plt.plot(freqs, psds_mean.T)
        plt.fill_between(freqs,
                        (psds_mean - psds_std).mean(axis=0),
                        (psds_mean + psds_std).mean(axis=0),
                        alpha=0.3)
        plt.title(f"PSD (mean ± std) - {label}")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Power")
        plt.show()
