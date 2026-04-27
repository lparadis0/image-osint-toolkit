# Image OSINT Toolkit

Practical Python toolkit developed during the 42 Firenze Cybersecurity Piscine, focused on image collection, EXIF metadata analysis and OSINT workflows.

## Included Tools

### spider.py
Downloads images from websites using recursive crawling, custom depth levels and user-defined save paths.

### scorpion.py
Analyzes image files and extracts EXIF metadata, file properties and technical information.

### requirements.txt
Project dependencies for setup and execution.

## Skills Demonstrated

- Python scripting
- Web scraping
- Command-line tool development
- File handling automation
- Metadata analysis
- Security-oriented workflows
- Practical problem solving

## Technologies

- Python 3
- requests
- BeautifulSoup4
- Pillow

## Example Use Cases

- Collect images from websites for analysis
- Inspect metadata from image files
- Support basic OSINT investigations

## Usage

```bash
pip install -r requirements.txt
python3 spider.py -r -l 2 -p ./images https://example.com
python3 scorpion.py image1.jpg image2.png
