import time
from helpers.win32_helpers import Win32Helpers

import mss
from PIL import Image
import pytesseract

class FlowerBot():
    def __init__(self):
        self.elden_ring_window = Win32Helpers.get_window('ELDEN RING™')

    def check_window(self):
        activeWindow = Win32Helpers.get_active_window()
        return activeWindow == self.elden_ring_window

    def teleport(self):
        Win32Helpers.pressAndHold('g')
        time.sleep(0.5)
        Win32Helpers.release('g')

        Win32Helpers.pressAndHold('s')
        time.sleep(0.1)
        Win32Helpers.release('s')

        Win32Helpers.pressAndHold('w')
        time.sleep(0.1)
        Win32Helpers.release('w')

        Win32Helpers.pressAndHold('enter')
        time.sleep(0.1)
        Win32Helpers.release('enter')
        time.sleep(0.5)
        Win32Helpers.pressAndHold('enter')
        time.sleep(0.1)
        Win32Helpers.release('enter')
        time.sleep(6)  # location loading
        print("loc loaded")

    def correct_position(self):
        time.sleep(1) # just to make extra sure location is loaded

        # turn 90 degrees
        Win32Helpers.pressAndHold('l')
        time.sleep(0.5)
        Win32Helpers.release('l')

        # run to the fire
        Win32Helpers.pressAndHold('w')
        time.sleep(0.8)
        Win32Helpers.release('w')

        time.sleep(0.2)

        # 90 degree turn again
        Win32Helpers.pressAndHold('l')
        time.sleep(0.4)
        Win32Helpers.release('l')

        # step forward
        Win32Helpers.pressAndHold('s')
        time.sleep(0.3)
        Win32Helpers.release('s')


    def take_screenshot(self):
        with mss.mss() as sct:
            # Define the region to capture (left, top, width, height)
            # where messages about collecting items are displayed
            region = {"left": 1050, "top": 650, "width": 300, "height": 60}

            # Capture the specified region
            screenshot = sct.grab(region)

            # Save the screenshot to a file
            mss.tools.to_png(screenshot.rgb, screenshot.size, output="collect_prompt.png")

        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        img = Image.open('collect_prompt.png')

        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(img)

        # Check if any text is detected
        if text:
            return True
        else:
            print("text was not extracted")
            return False

    def main(self):
        print("Waiting 5 seconds before starting...")
        time.sleep(5)
        print("starting")
        self.teleport()
        self.correct_position()
        while self.check_window():
            # run to the flower
            Win32Helpers.pressAndHold('s')
            time.sleep(1.5)
            Win32Helpers.release('s')

            # collect the flower
            Win32Helpers.pressAndHold('e')
            time.sleep(0.1)
            Win32Helpers.release('e')

            success = False
            for i in range(5):
                success = self.take_screenshot()
                if success: break
                time.sleep(0.05)
            if not success:
                self.teleport()
                self.correct_position()
            else:
                # run to the fire
                Win32Helpers.pressAndHold('w')
                time.sleep(1.5)
                Win32Helpers.release('w')

                # sit down
                Win32Helpers.pressAndHold('e')
                time.sleep(0.1)
                Win32Helpers.release('e')

                time.sleep(3.5) # sit at the fire
                Win32Helpers.click_mouse(400, 200)
                time.sleep(2)


        print("Stopped session because we're no longer in the right window")
        return


bot = FlowerBot()
bot.main()