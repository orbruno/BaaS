# API Testing

This folder contains test files and scripts for testing the Branding API.

## 📁 Test Structure

```
tests/
├── data/                          # Test data files
│   ├── techcorp_interview.txt     # Text format interview
│   ├── greenleaf_interview.md     # Markdown format interview
│   ├── brightfuture_interview.txt # Another text interview
│   └── (your_pdf_files_here.pdf)  # PDF files for testing
├── test_api.py                    # API testing script
└── README.md                      # This file
```

## 🧪 Running Tests

### 1. Start your FastAPI server

```bash
# From the project root
uvicorn main:app --reload
```

### 2. Install requests for testing (if not already installed)

```bash
uv add requests --dev
```

### 3. Run the test script

```bash
# From the project root
python tests/test_api.py
```

## 📄 Creating Test PDFs

### Option 1: Convert existing text files

1. Open any of the `.txt` files in `tests/data/`
2. Copy the content
3. Paste into Google Docs, Word, or Pages
4. Export/Save as PDF
5. Save in `tests/data/` folder

### Option 2: Use online converters

1. Go to any text-to-PDF converter (like SmallPDF, ILovePDF)
2. Upload one of the text files
3. Download the PDF
4. Save in `tests/data/` folder

### Option 3: Command line (macOS/Linux)

```bash
# Convert text to PDF using pandoc (if installed)
pandoc tests/data/techcorp_interview.txt -o tests/data/techcorp_interview.pdf
```

## 🔧 Manual Testing with curl

### Test with text file

```bash
curl -X POST "http://localhost:8000/api/v1/branding/create-from-interview" \
  -H "Content-Type: multipart/form-data" \
  -F "interview_file=@tests/data/techcorp_interview.txt" \
  -F "brand_name=TechCorp Solutions"
```

### Test with PDF file

```bash
curl -X POST "http://localhost:8000/api/v1/branding/create-from-interview" \
  -H "Content-Type: multipart/form-data" \
  -F "interview_file=@tests/data/your_file.pdf" \
  -F "brand_name=Your Brand Name"
```

## 📋 Available Test Files

1. **techcorp_interview.txt** - Technology company focused on simplifying complex software
2. **greenleaf_interview.md** - Organic food company with sustainability focus
3. **brightfuture_interview.txt** - Consulting firm focused on transformation

Each file contains realistic interview content that should generate meaningful Golden Circle responses from your API.

## 🎯 Expected Response Format

```json
{
  "brand_name": "Brand Name",
  "golden_circle": {
    "why": "The purpose and belief...",
    "how": "The process and values...",
    "what": "The products and services..."
  }
}
```
