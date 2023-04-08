import food_scanner as fs 

class Ai(): 
    def __init__(self,img_path,api_key):
        self.api_key = api_key
        self.img_path = img_path

    def run(self):
        text = fs.text_recognition(self.img_path)
        response = fs.chatgpt(text,self.api_key)

        print(response)

if __name__ == "__main__":
    ai = Ai("sample_image_path",
            "API_KEY")
    ai.run()
