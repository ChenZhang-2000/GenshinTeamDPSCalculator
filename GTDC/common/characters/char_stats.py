import os

import yaml
import torch

file_name = os.path.join(os.path.dirname(__file__), f'stats')

with open(rf"{file_name}\_base_value.yaml", 'r', encoding="utf-8") as stream:
    base_value = yaml.safe_load(stream)

with open(rf"{file_name}\_level_multiplier.yaml", 'r', encoding="utf-8") as stream:
    level_multiplier = yaml.safe_load(stream)

with open(rf"{file_name}\_max_ascension_values.yaml", 'r', encoding="utf-8") as stream:
    max_ascension_value = yaml.safe_load(stream)

ascension_value_multiplier = [0, 38/182, 65/182, 101/182, 128/182, 155/182, 1]
ascension_bonus_multiplier = [0, 0, 1, 2, 2, 3, 4]

base_attributes = torch.tensor([0, 0, 0,
                                0, 0, 0,
                                0, 0, 0,

                                0, 5, 50, 0, 100, 0,

                                0, 10,
                                0, 10,
                                0, 10,
                                0, 10,
                                0, 10,
                                0, 10,
                                0, 10,
                                0, 10,

                                0, 0.])

bonus_attributes_multiplier = {
    4: torch.tensor([0, 0, 6,
                     0, 0, 7.5,
                     0, 0, 6,

                     24, 0, 0, 0, 6.7, 0,

                     6, 0,
                     6, 0,
                     6, 0,
                     6, 0,
                     6, 0,
                     6, 0,
                     6, 0,
                     7.5, 0,

                     0, 0]),
    5: torch.tensor([0, 0, 7.2,
                     0, 0, 0,
                     0, 0, 0,

                     28.8, 4.8, 9.6, 5.5, 8, 0,

                     7.2, 0,
                     7.2, 0,
                     7.2, 0,
                     7.2, 0,
                     7.2, 0,
                     7.2, 0,
                     7.2, 0,
                     0, 0,

                     0, 0])
}














