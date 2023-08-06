from octoai.client import Client
from octoai.types import Image
from config import OCTO_API_KEY
from PIL import Image

import chainlit as cl
import base64
import io
import json

client = Client(token=OCTO_API_KEY)  

client = Client() # token can be set in Client instantiation if not an env variable

public_endpoint = "https://stable-diffusion-xl-demo-kk0powt97tmb.octoai.cloud"
private_endpoint = "https://stable-diffusion-xl-demo-05v073pgec1v.octoai.cloud"

stable_diffusion_url = private_endpoint + "/predict"
sd_health_check = private_endpoint + "/healthcheck"


def get_image_name():
    image_count = cl.user_session.get("image_count")
    if image_count is None:
        image_count = 0
    else:
        image_count += 1

    cl.user_session.set("image_count", image_count)

    return f"image-{image_count}"


def decode_image(base64_image):
    """
    Decodes the base64 image data to bytes.

    Args:
        base64_image (str): Base64 encoded image data.

    Returns:
        bytes: Decoded image data in bytes.
    """
    image_data = base64.b64decode(base64_image.encode())
    return image_data


def _generate_image(prompt: str):

    # These are the inputs we'll send to the endpoint.
    inputs = {
                # The prompt input is required, while the rest are optional.
            "prompt": prompt,
            # What we don't want to see
            "negative_prompt": "bad anatomy, bad proportions, blurry, cloned face, cropped, deformed, dehydrated, disfigured, duplicate, error, extra arms, extra fingers, extra legs, extra limbs, fused fingers, gross proportions, jpeg artifacts, long neck, low quality, lowres, malformed limbs, missing arms, missing legs, morbid, mutated hands, mutation, mutilated, out of frame, poorly drawn face, poorly drawn hands, signature, text, too many fingers, ugly, username, watermark, worst quality,deformed, glitch, noise, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, sloppy, duplicate, mutated, black and white",
            # Classifier free guidance, 1 to 20
            "guidance_scale": 7.5,
            # Number of denoising steps, 1 to 500
            "num_inference_steps": 40,
            # Algorithm used for denoising.  Also accepts PNDM, KLMS, DDIM, etc.
            # Please view the QuickStart templates page for stable diffusion for more information.
            "scheduler": "DPMSolverMultistep"
    }

    if client.health_check(sd_health_check) == 200:

        outputs = client.infer(endpoint_url=stable_diffusion_url, inputs=inputs)

        print(f"Generation completed successfly in {outputs.get('prediction_time_ms')} millisecs...")

        # save outpust json to file
        with open('outputs.json', 'w') as f:
            json.dump(outputs, f)


        # The output image is a base64 encoded string.
        # This can easily be passed to other models for inference as well.
        sd_image_base64 = outputs.get('completion').get('image_0')

        if sd_image_base64 is None:
            print("No image generated. Please try again.")
            return None, None

        image = decode_image(sd_image_base64)

        # print(f"\n\nTYPE OF IMAGE: {type(image)}")

        name = get_image_name()
        cl.user_session.set(name, image)
        cl.user_session.set("generated_image", name)
        print(f"Generated image: {name}")
        
        return name, image
    else:
        print("Model is not ready yet. Please try again later.") 
        return None, None   

       

def generate_image(prompt: str):
    image_name, image = _generate_image(prompt)
    return f"Here is {image_name}.", image
