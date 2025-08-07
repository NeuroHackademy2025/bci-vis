import mne


def plot_raw(raw, config):
    vis_cfg = config.get("visualization", {})
    duration = vis_cfg.get("duration", 60.0)
    start = vis_cfg.get("start", 0.0)
    n_channels = vis_cfg.get("n_channels", 8)
    scalings = vis_cfg.get("scalings", dict(eeg=1e2))

    raw.plot(duration=duration, start=start, scalings=scalings,
             n_channels=n_channels, title="Raw EEG Signal")


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


def plot_epoch_psd(epochs, event_label, config):
    vis_cfg = config.get("visualization", {})
    fmin = vis_cfg.get("psd_fmin", 0.1)
    fmax = vis_cfg.get("psd_fmax", 45.0)
    picks = vis_cfg.get("picks", 'eeg')

    epochs[event_label].plot_psd(picks=picks, fmin=fmin, fmax=fmax)
