import yaml

def load_config(config_path = 'config/config.yaml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# testing
if __name__ == "__main__":
    cfg = load_config()
    print("Master file path: ", cfg['master_file'])
    print("Deduplication?", cfg['deduplication']['enabled'])