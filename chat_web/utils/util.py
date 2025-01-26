import torch
from PIL import Image 

max_value = 10.0

class Resize:
    def __init__(self, size):
        self.size = size

    def __call__(self, image):
        w, h = image.size
        if max(h, w) == self.size:
            return image

        scale = self.size * 1.0 / max(w, h)
        new_w = int(w * scale + 0.5)
        new_h = int(h * scale + 0.5)
        return image.resize((new_w, new_h), Image.Resampling.BILINEAR)


class Pad:
    def __init__(self, size):
        self.size = size

    def __call__(self, image):
        h, w = image.shape[-2:]
        assert self.size >= h and self.size >= w
        pad = (0, self.size - w, 0, self.size - h)
        image = torch.nn.functional.pad(image, pad, value=0)
        return image
