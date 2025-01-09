from openai import OpenAI 

class getResponse : 
    def __init__(self, 
                 api_key
                 ):
        self.api_key = api_key

    def auth(self) : 
        client = OpenAI(api_key=self.api_key)
        return client 
    
    def get_response(self, message) : 
        client = self.auth() 

        response = client.chat.completions.create(model = "gpt-4o-mini", 
                                                  messages = message, 
                                                  temperature = 0
        )

        return response.choices[0].message.content


