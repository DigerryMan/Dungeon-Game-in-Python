class ShakingAnimation():
    def __init__(self, boss):
        self.boss = boss
        self.shake_time_x_left = 5
        self.x_change = 1
        self.shake_time_y_left = 5
        self.y_change = 1

    def shaking_animation_x(self, with_laser=False):
        self.shake_time_x_left -= 1
        if self.shake_time_x_left <= 0:
            self.boss.rect.centerx += 5 * self.x_change
            if with_laser and self.boss.laser is not None:
                self.boss.laser.rect.centerx += 5 * self.x_change
            
            self.x_change *= -1
            self.shake_time_x_left = 3

    def shaking_animation_y(self):
        self.shake_time_y_left -= 1
        if self.shake_time_y_left <= 0:
            self.boss.rect.centery += 2 * self.y_change
            self.y_change *= -1
            self.shake_time_y_left = 7
    
    def shake_animation_x_and_y(self):
        self.shaking_animation_x()
        self.shaking_animation_y()