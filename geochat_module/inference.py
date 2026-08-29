import torch
import requests
from PIL import Image
from io import BytesIO

# These imports require the GeoChat module to be installed
# pip install -e . (from inside the GeoChat repository)
from geochat.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from geochat.conversation import conv_templates, SeparatorStyle
from geochat.model.builder import load_pretrained_model
from geochat.utils import disable_torch_init
from geochat.mm_utils import tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria

class GeoChatInference:
    def __init__(self, model_path="MBZUAI/geochat-7B", load_8bit=False, load_4bit=False, device="cuda"):
        """
        Initializes the GeoChat inference module.
        Requires a GPU with at least 16GB VRAM for standard precision, or 8GB VRAM for 8-bit precision.
        """
        self.model_path = model_path
        self.device = device
        disable_torch_init()

        print(f"Loading model from {model_path}...")
        model_name = get_model_name_from_path(model_path)
        
        # Load tokenizer, model, and image processor
        self.tokenizer, self.model, self.image_processor, self.context_len = load_pretrained_model(
            model_path, None, model_name, load_8bit=load_8bit, load_4bit=load_4bit, device=device
        )
        self.model = self.model.to(device)
        self.conv_mode = "geochat_v1"

    def load_image(self, image_source):
        if image_source.startswith("http://") or image_source.startswith("https://"):
            response = requests.get(image_source)
            image = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            image = Image.open(image_source).convert("RGB")
        return image

    def generate(self, image_source, query, temperature=0.2, max_new_tokens=512):
        """
        Runs inference for a given image and text query.
        """
        image = self.load_image(image_source)
        
        # Preprocess image
        image_tensor = self.image_processor.preprocess(image, return_tensors='pt')['pixel_values'].half().to(self.device)

        # Prepare conversation template
        conv = conv_templates[self.conv_mode].copy()
        
        # Format the prompt
        if self.model.config.mm_use_im_start_end:
            inp = DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN + DEFAULT_IM_END_TOKEN + '\n' + query
        else:
            inp = DEFAULT_IMAGE_TOKEN + '\n' + query
            
        conv.append_message(conv.roles[0], inp)
        conv.append_message(conv.roles[1], None)
        prompt = conv.get_prompt()

        # Tokenize inputs
        input_ids = tokenizer_image_token(prompt, self.tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).to(self.device)
        
        # Set stopping criteria
        stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
        keywords = [stop_str]
        stopping_criteria = KeywordsStoppingCriteria(keywords, self.tokenizer, input_ids)

        # Generate response
        with torch.inference_mode():
            output_ids = self.model.generate(
                input_ids,
                images=image_tensor,
                do_sample=True,
                temperature=temperature,
                max_new_tokens=max_new_tokens,
                use_cache=True,
                stopping_criteria=[stopping_criteria]
            )

        # Decode output
        input_token_len = input_ids.shape[1]
        n_diff_input_output = (input_ids != output_ids[:, :input_token_len]).sum().item()
        if n_diff_input_output > 0:
            print(f'[Warning] {n_diff_input_output} output_ids are not the same as the input_ids')
        
        outputs = self.tokenizer.batch_decode(output_ids[:, input_token_len:], skip_special_tokens=True)[0]
        outputs = outputs.strip()
        
        if outputs.endswith(stop_str):
            outputs = outputs[:-len(stop_str)]
            
        return outputs.strip()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str, required=True, help="Path or URL to the remote sensing image")
    parser.add_argument("--query", type=str, default="Describe this image in detail.", help="Query text")
    parser.add_argument("--load-8bit", action="store_true", help="Load model in 8-bit mode (useful for 8GB VRAM Colab GPUs)")
    args = parser.parse_args()

    print("Initializing GeoChat-7B...")
    geochat = GeoChatInference(load_8bit=args.load_8bit)
    
    print(f"Running inference on image: {args.image}")
    answer = geochat.generate(args.image, args.query)
    
    print("-" * 50)
    print(f"[Query]: {args.query}")
    print(f"[Output]: {answer}")
    print("-" * 50)
