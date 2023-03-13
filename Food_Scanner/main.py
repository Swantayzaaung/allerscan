#Made by Thaw Zin Thant , Ai dev at Byte Busters team (Hub and Hack 2023 competition)

import pytesseract
import cv2
import numpy as np
import os
import openai

#instruction to run my code

#pip install openai
#pip install numpy
#pip install opecv-python

#instruction link for installing and setting pytesseract in ur window system
# https://www.projectpro.io/recipes/what-is-pytesseract-python-library-and-do-you-install-it

#to run pytessract for window users , you need to add path file of ur tessract program
# path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# varible
text = """"""
img_path = 'sampleImages/sample1.jpg' #image path for testing

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
        # text = text.replace("\n" , "")
        print(self.text)

    # output facts about allergies info
    def chatgpt(self):
        #Note: you need to you use your own Api
        openai.api_key = "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"#os.getenv("OPENAI_API_KEY")
        
        messages = [
            {"role": "system", "content": "You are a kind helpful assistant."},
        ]
        
        message = self.text
        
        if message:
            messages.append(
                {"role": "user", "content": f"Show possible Allergies of : {message}"},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )

        reply = chat.choices[0].message.content
        print(f"ChatGPT: {reply}")
        messages.append({"role": "assistant", "content": reply})

if __name__ == '__main__':
    aller = Allergy()
    aller.img_to_text(img_path) # change path 
    aller.chatgpt()
               

 
