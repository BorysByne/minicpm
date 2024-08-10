# MiniCPM API

## Overview

MiniCPM API is a FastAPI-based wrapper around the openbmb/MiniCPM-V-2_6 model. It provides a ChatGPT-compatible API that allows users to interact with the MiniCPM model, supporting both the quantized (int4) and full versions of the model.

**Note:** We've recorded a 95% accuracy with this model on a test dataset of PDF pages.

⚠️ **Warning:** The model requires the images to be reasonably compressed, or it may take a long time to run. Please ensure your input images are optimized for performance.

## Features

- ChatGPT-compatible API endpoint for text generation
- Support for both openbmb/MiniCPM-V-2_6-int4 (quantized) and openbmb/MiniCPM-V-2_6 (full) models
- Handling of text and image inputs
- Customizable generation parameters (temperature, max tokens, etc.)
- Error handling and input validation
- Support for system prompts

## Prerequisites

- Python 3.10 or higher
- CUDA-compatible GPU (for full model support)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/minicpm-api.git
   cd minicpm-api
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the API server:
   ```
   python app/main.py
   ```

2. When prompted, choose the model version you want to use:
   - Option 1: openbmb/MiniCPM-V-2_6-int4 (Quantized version)
   - Option 2: openbmb/MiniCPM-V-2_6 (Full version)

3. The API will be available at `http://localhost:8000`.

## API Endpoints

### POST /v1/chat/completions

Generate a chat completion using the MiniCPM model.

#### Request Body

```json
{
  "model": "MODEL_NAME",
  "temperature": 0,
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Hello, how are you?"
        }
      ]
    }
  ],
  "seed": 42,
  "response_format": {
    "type": "json_object"
  },
  "max_tokens": 4095
}
```

#### Response

```json
{
  "id": "chatcmpl-123abc",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "Hello! As an AI assistant, I don't have feelings, but I'm functioning well and ready to help you. How can I assist you today?",
        "role": "assistant"
      }
    }
  ],
  "model": "MODEL_NAME"
}
```

## Error Handling

- The API will return a 400 status code if more than one system message is provided in the request.
- Other errors will result in a 500 status code with an error message.

## Examples and Testing

For guidance on how to use the API and for testing purposes, please refer to the `example` folder in the project root. This folder contains:

- `test.ipynb`: A Jupyter notebook with usage examples and test cases.
- `test_images/`: A subfolder containing sample images for testing the image processing capabilities of the API.

We recommend reviewing these examples to understand the API's functionality and to ensure it meets your specific requirements.

## Development

### Project Structure

```
minicpm_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── chat.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── minicpm.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── chat.py
│
├── example/
│   ├── test.ipynb
│   └── test_images/
│       └── (various test images)
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## License and Usage Restrictions

This software is proprietary and is not open for contributions. 

**Important:** This proprietary software shall not be deployed for commercial applications unless a license has been granted. 

For licensing inquiries or permissions, please contact denys.budnyk@bynesoft.com.

## Acknowledgements

- [openbmb/MiniCPM](https://github.com/OpenBMB/MiniCPM) for the underlying model
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework

## Support

If you encounter any problems or have any questions, please contact our support team at borys.nadykto@bynesoft.com.