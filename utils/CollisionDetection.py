class CollisionDetection:

    @staticmethod
    def collision(dynamic_object, static_object):
        static_object_x, static_object_y = static_object.position["x"], static_object.position["y"]

        if dynamic_object.position['x'] + dynamic_object.width > static_object.position['x'] and \
                dynamic_object.position['x'] < static_object.position[
            'x'] + static_object.width:
            if (static_object.position['y'] < dynamic_object.position['y'] < static_object.position[
                'y'] + static_object.height) or (
                    static_object.position['y'] < dynamic_object.position['y'] + dynamic_object.height <
                    static_object.position['y'] + static_object.height):
                return True
        return False

    @staticmethod
    def position_tank_relatively_to_moving_direction(tank, sprite):
        # if tank.current_image_angle == 0:
        #     tank.position['y'] = sprite.height + sprite.position['y']
        # elif tank.current_image_angle == 180:
        #     tank.position['y'] = sprite.position['y'] - tank.height
        # elif tank.current_image_angle == 270:
        #     tank.position['x'] = sprite.position['x'] - tank.width
        # elif tank.current_image_angle == 90:
        #     tank.position['x'] = sprite.position['x'] + sprite.width
        if tank.current_image_angle == 0 and tank.position['y'] > sprite.position['y'] + (sprite.height / 2):
            tank.position['y'] = sprite.height + sprite.position['y']
        if tank.current_image_angle == 180 and tank.position['y'] < sprite.position['y'] + (sprite.height / 2):
            tank.position['y'] = sprite.position['y'] - tank.height
        if tank.current_image_angle == 270 and tank.position['x'] < sprite.position['x'] + (sprite.width / 2):
            tank.position['x'] = sprite.position['x'] - tank.width
        if tank.current_image_angle == 90 and tank.position['x'] > sprite.position['x'] + (sprite.width / 2):
            tank.position['x'] = sprite.position['x'] + sprite.width
