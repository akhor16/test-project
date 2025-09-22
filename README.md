# Algorithm Processor

A Flask web application that processes text files containing lists, applies a custom algorithm, and integrates with an LLM for sorting results.

## Features

- Upload TXT files with list data in format `[a,b,c]`
- Process data through the "unset" algorithm
- Store the 5 most recent results on disk
- Send results to LLM (OpenAI) for sorting
- Simple, responsive web interface
- Docker containerization ready

## Algorithm

The application implements the "unset" algorithm that:
1. Finds runs of consecutive identical symbols
2. Identifies the maximum run length
3. Returns sorted unique symbols from runs with maximum length

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Visit `http://localhost:5000`

**Note:** No API keys are required! The LLM functionality uses a built-in sorting algorithm with LLM-like response formatting.

## Docker

1. Build the image:
```bash
docker build -t algorithm-processor .
```

2. Run the container:
```bash
docker run -p 5000:5000 algorithm-processor
```

## Deployment to Railway

1. Push your code to GitHub
2. Connect your GitHub repository to Railway
3. Railway will automatically build and deploy using the Dockerfile

## Environment Variables

- `PORT`: Port number (default: 5000)

## File Format

Upload TXT files with each line containing a list in the format:
```
[a]
[a,b]
[a,a,b]
[a,a,b,b]
[a,b,b,a]
[a,a,z,z,z,a,a]
[r,r,r,a,a,g,g,g,r,r,r]
```

## API Endpoints

- `GET /`: Main application page
- `POST /upload`: Upload and process TXT file
- `POST /llm`: Send most recent result to LLM
- `GET /history`: Retrieve stored results

## Testing

The application can be tested with the provided example data. Expected outputs:
- `[a]` → `[]`
- `[a,a]` → `[a]`
- `[a,b]` → `[]`
- `[a,a,b,b]` → `[a,b]`
- `[a,b,b,a]` → `[b]`
- `[a,a,z,z,z,a,a]` → `[z]`
- `[r,r,r,a,a,g,g,g,r,r,r]` → `[g,r]`
