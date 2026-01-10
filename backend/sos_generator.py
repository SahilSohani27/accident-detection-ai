# sos_generator.py

import os
import base64
from openai import OpenAI

class SOSGenerator:
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        """
        Initializes SOS Generator with OpenAI client.
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def generate_sos(self, accident_info: dict, best_frame_path: str):
        """
        Generate SOS message using ChatGPT based on accident info and best frame.
        
        Args:
            accident_info (dict): Info dict from accident detector.
            best_frame_path (str): Path to best frame image.
        
        Returns:
            str: SOS message text.
        """

        # Encode image as base64 for OpenAI vision input
        image_base64 = None
        if best_frame_path and os.path.exists(best_frame_path):
            with open(best_frame_path, "rb") as img_file:
                image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        # Build prompt
        prompt = (
            f"Accident detected in the video uploaded to an ai accident detection system. "
            f"The frame with the highest confidence is attached for your analysis. "
            f"The system is {accident_info.get('confidence'):.2f} confident. "
            f"Generate a short SOS alert message suitable for immediately notifying emergency response teams. "
            f"The message should be clear, urgent, and professional whilst explaining the severity of the accident"
            f"Also mention only if you think there is going to be a fire hazard because of the vehicle collision and if a fire truck is needed"
            f"If there is no mention of location, do not enter any location in the message."
            f"Do not any dummy text in the message, only interpret what you get from the frames and try to mention the details you can interpret."
        )

        # Prepare input for OpenAI (text + image if available)
        content = [{"type": "text", "text": prompt}]
        if image_base64:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                }
            })

        # Send request
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": content}],
            max_tokens=150
        )

        sos_message = response.choices[0].message.content
        return sos_message


# # Example usage:
# if __name__ == "__main__":
#     accident_info = {
#         "coordinates": [100, 200, 300, 400],
#         "confidence": 0.92,
#         "frame_idx": 120
#     }
#     sos = SOSGenerator().generate_sos(accident_info, "sample_best_frame.jpg")
#     print("Generated SOS Message:\n", sos)
