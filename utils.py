import requests

class APIClient:
    BASE_URL = "http://127.0.0.1:8000"

    @staticmethod
    def send_request(endpoint: str, payload: dict = None) -> dict:
        """
        Sends a request to the specified endpoint of the API.
        
        Args:
            endpoint (str): The API endpoint to send the request to.
            payload (dict, optional): The JSON payload to send with the request. Defaults to None.
        
        Returns:
            dict: The response from the API.
        """
        url = f"{APIClient.BASE_URL}{endpoint}"
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    @staticmethod
    def chat(question: str) -> dict:
        """
        Sends a question to the chat endpoint of the API.
        
        Args:
            question (str): The question to be sent to the chat engine.
        
        Returns:
            dict: The response from the API.
        """
        return APIClient.send_request("/chat", {"question": question})

    @staticmethod
    def reset_chat() -> dict:
        """
        Sends a request to reset the chat history.
        
        Returns:
            dict: The response from the API confirming the reset action.
        """
        return APIClient.send_request("/reset")