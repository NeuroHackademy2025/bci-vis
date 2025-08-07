import yaml
from src.bcivis.manager.core import DatasetManager


config_path = "D:/Niv/bci_vis/bci-vis/src/bcivis/config/motor_imagery_ds003810.yaml"
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

manager = DatasetManager(config=config)
manager.load_all()
manager.preprocess_all()


# Sanity check
for i, loader in enumerate(manager.loaders):
    print(f"\n✅ Loader {i+1}")
    print(f"Subject: {loader.subject} | Run: {loader.run}")
    print("Raw info:", loader.raw.info)
    print("Event IDs:", loader.event_id)
    print("Events shape:", loader.events.shape if loader.events is not None else None)
    print("Epochs shape:", manager.get_all_epochs()[i].get_data().shape)
