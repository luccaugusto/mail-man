import stow
from datetime import datetime

from mltu.configs import BaseModelConfigs

class ModelConfigs(BaseModelConfigs):
    def __init__(self):
        super().__init__()
        self.model_path = stow.join('Model/', datetime.strftime(datetime.now(), "%Y%m%d%H%M"))
        self.vocab = ''
        self.height = 80
        self.width = 215
        self.max_text_length = 0
        self.batch_size = 64
        self.learning_rate = 1e-2
        self.train_epochs = 1000
        self.train_workers = 20