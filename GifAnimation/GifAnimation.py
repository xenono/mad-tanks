import pygame


class GifAnimation:
    def __init__(self, folder_with_frames, first_frame_number, last_frame_number, screen):
        self.screen = screen
        self.folder_with_frames = folder_with_frames
        self.first_frame_number = first_frame_number
        self.last_frame_number = last_frame_number
        self.frames = []
        self.frame_counter = 0
        self.is_finished = False
        self.switch_image_delay = 0

    def load_frames(self):
        # Load all frames
        step = 1 if self.first_frame_number < self.last_frame_number else -1
        for frame in range(self.first_frame_number, self.last_frame_number + step, step):
            path = "assets/{}/0{:02d}.png".format(self.folder_with_frames, frame)
            self.frames.append(pygame.image.load(path))

    def play(self):
        self.screen.blit(self.frames[self.frame_counter], (100, 100))
        self.switch_image_delay += 1

    def update(self):
        if self.frame_counter == len(self.frames):
            self.is_finished = True

        if not self.is_finished:
            self.play()
            if self.switch_image_delay % 20 == 0:
                self.frame_counter += 1

