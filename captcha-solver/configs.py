import stow
from datetime import datetime

from mltu.configs import BaseModelConfigs

class ModelConfigs(BaseModelConfigs):
    def __init__(self):
        super().__init__()
        self.model_path = stow.join('Model/%Y%m%d%H%M'))
        self.vocab = '0123456789abcdefghijklmnopqrstuvwxyz'
        self.height = 80
        self.width = 215
        self.max_text_length = 6
        self.batch_size = 64
        self.learning_rate = 1e-3
        self.train_epochs = 1000
        self.train_workers = 20
