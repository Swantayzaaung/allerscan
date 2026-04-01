#Made by Thaw Zin Thant , Ai dev at Byte Busters team (Hub and Hack 2023 competition)

import pytesseract
import cv2
import numpy as np
import os
import openai
from dotenv import load_dotenv

load_dotenv()

path_to_tesseract = os.getenv("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = path_to_tesseract

text = """"""

class Allergy():
    
    # blurring image (thresholding)
    def apply_threshold(self , img , argument):
        
        switcher = {
            "GaussianBlur": cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
            "bilateralFilter": cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
            "medianBlur": cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
            "GaussianBlurAdaptive": cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
            "bilateralFilterAdaptive": cv2.adaptiveThreshold(cv2.bilateralFilter(img, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
            "medianBlurAdaptive": cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        }
        return switcher.get(argument, "Invalid method")

    def img_to_text(self , img_path: str):

        #language configuration
        config = ('-l eng --oem 1 --psm 3')

        img = cv2.imread(img_path)

        # Rescaling the image
        img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

        # Converting image to gray-scale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Applying dilation and erosion to remove the noise
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)

        self.text = pytesseract.image_to_string(img, config=config)

    def chatgpt(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY is not set. Add it in your .env file.")
        
        messages = [
            {"role": "system", "content": "You are a kind helpful assistant."},
        ]
        
        message = self.text
        
        if message:
            messages.append(
                {"role": "user", "content": f"If it contains the word Ingredients, use at least 5 explanations to show possible Allergies of : {message}"},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )

        reply = chat.choices[0].message.content
        return reply