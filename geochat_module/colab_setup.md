# GeoChat-7B Google Colab Setup & Test Guide

Since GeoChat-7B requires a GPU and is too large for an 8GB Mac, you should test the inference using Google Colab.

### Hardware Requirements
- **GPU**: A T4 GPU on Google Colab is sufficient (provides 16GB of VRAM).
- **RAM**: ~12-16GB of System RAM.
- Note: Loading the model in 8-bit precision (`--load-8bit`) can significantly reduce VRAM usage if you are facing OOM (Out Of Memory) issues.

### Step-by-Step Instructions

1. **Open Google Colab**
   Go to [Google Colab](https://colab.research.google.com/) and create a new notebook.
   Navigate to **Runtime > Change runtime type** and select **T4 GPU**.

2. **Clone the Official Repository & Setup Environment**
   Run the following commands in the first cell of your notebook to clone the official GeoChat repository and install dependencies:

   ```bash
   # Clone the official repository
   !git clone https://github.com/mbzuai-oryx/GeoChat.git
   %cd GeoChat

   # Install the GeoChat package
   !pip install -e .

   # Install missing requirements if any
   !pip install accelerate
   ```

3. **Upload the Inference Script**
   Upload the `inference.py` script provided in `geochat_module/inference.py` to the `/content/GeoChat/` folder in Colab.

4. **Run the Inference Test**
   In a new cell, run the script against an example remote sensing image. You can use any image URL.

   ```bash
   !python inference.py \
       --image "https://raw.githubusercontent.com/mbzuai-oryx/GeoChat/main/images/demo/1.jpg" \
       --query "Describe this remote sensing image in detail." \
       --load-8bit
   ```

### Example Expected Output

When the script successfully runs, it should output:

```text
Loading model from MBZUAI/geochat-7B...
Loading checkpoint shards: 100%|██████████| 2/2 [00:45<00:00,  0.04s/it]
Initializing GeoChat-7B...
Running inference on image: https://raw.githubusercontent.com/mbzuai-oryx/GeoChat/main/images/demo/1.jpg
--------------------------------------------------
[Query]: Describe this remote sensing image in detail.
[Output]: The image displays a large residential area characterized by densely packed houses and narrow streets. The homes appear mostly identical and are tightly arranged in blocks... [etc]
--------------------------------------------------
```

### Next Steps for SatQuery AI
Once you verify that this standalone inference works, we can proceed to:
1. Wrap this `inference.py` in a FastAPI endpoint.
2. Build the backend services and logic around it.
3. Keep the frontend separate so it can query this GPU-hosted endpoint via REST API.
