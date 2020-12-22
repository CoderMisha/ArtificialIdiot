import torch.nn as nn
import torch.nn.functional as F
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.rllib.utils.typing import ModelConfigDict
from gym.spaces import Space
import numpy as np
from PIL import Image


class NoobSaberTorchModel(TorchModelV2, nn.Module):
    def __init__(self, obs_space: Space, action_space: Space, num_outputs: int, model_config: ModelConfigDict, name: str):
        TorchModelV2.__init__(self, obs_space, action_space, num_outputs, model_config, name)
        nn.Module.__init__(self)

        self.conv1 = nn.Conv2d(3, 8, 3)
        self.conv2 = nn.Conv2d(8, 32, 3)
        self.conv3 = nn.Conv2d(32, 64, 3)
        self.fc1 = nn.Linear(64 * 37 * 47, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_outputs)

        self.model_out = None

    def forward(self, input_dict, state, seq_lens):
        x = input_dict["obs"].float().permute(0, 3, 1, 2)

        x = self.conv1(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)

        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)

        x = self.conv3(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)

        x = x.reshape(x.size(0), -1)

        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)

        self.model_out = x

        return x, state

    def value_function(self):
        return self.model_out[0]


def my_resize_frame_pixels(self, frame):
        img = Image.frombytes(
            'RGB',
            (self.video_width, self.video_height),
            bytes(frame.pixels)
        )

        resized = img.resize((self.obs_width, self.obs_height))

        resized_arr = np.array(resized)

        img.close()
        resized.close()
        return resized_arr

def my_empty_obs(self):
    return np.zeros((self.obs_height, self.obs_width, 3))
