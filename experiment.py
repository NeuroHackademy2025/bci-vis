from src.bcivis.io.loader import MatDataLoader
path = "D:/Niv/bci_vis/data/A01E.mat"
config_path = "D:/Niv/bci_vis/bci-vis/src/bcivis/config/mi_bnci_2014.yaml"

loader = MatDataLoader(path, config=config_path)
loader.load()

raw = loader.get_raw()
raw.plot()
labels = loader.get('labels') or loader.get('y')
trial_starts = loader.get('tria0l') or loader.get('onsets')

raw.plot()  