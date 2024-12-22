import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.camera import Camera
import cv2
import numpy as np
import matplotlib.pyplot as plt

class CameraClick(BoxLayout):
    def __init__(self, **kwargs):
        super(CameraClick, self).__init__(**kwargs)

        self.orientation = 'vertical'

        self.camera = Camera(play=True)
        self.camera.resolution = (640, 480)
        self.add_widget(self.camera)

        self.capture_button = Button(text="Prendre une Photo")
        self.capture_button.bind(on_press=self.capture)
        self.add_widget(self.capture_button)

        self.image_view = Image()
        self.add_widget(self.image_view)

    def capture(self, instance):
        texture = self.camera.texture
        image_data = np.frombuffer(texture.pixels, np.uint8).reshape(texture.height, texture.width, 4)
        image = cv2.cvtColor(image_data, cv2.COLOR_RGBA2BGR)

        # Enregistrer l'image capturée
        cv2.imwrite('captured_image.png', image)

        # Afficher l'histogramme de l'image
        self.show_histogram(image)

    def show_histogram(self, image):
        # Convertir en niveaux de gris pour l'histogramme
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        plt.hist(gray_image.ravel(), 256, [0, 256])
        plt.title('Histogramme')
        plt.xlabel('Intensité des pixels')
        plt.ylabel('Nombre de pixels')

        # Enregistrer l'histogramme
        plt.savefig('histogram.png')
        plt.close()

        # Afficher l'histogramme dans l'application
        histogram_image = cv2.imread('histogram.png')
        buf1 = cv2.flip(histogram_image, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(histogram_image.shape[1], histogram_image.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.image_view.texture = image_texture

class TestCameraApp(App):
    def build(self):
        return CameraClick()

if __name__ == '__main__':
    TestCameraApp().run()