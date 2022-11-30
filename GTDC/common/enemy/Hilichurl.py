from .base_enemy import register_enemy, Enemy


@register_enemy
class Hilichurl(Enemy):
    def __init__(self, level=100):
        super().__init__(level)