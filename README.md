# Web scraper 🔍

## Description

This project is a web scraper designed to extract data from websites. It can be customized to scrape various types of data and save it in different formats.

## Features

- Extracts data from web pages
<!-- - Supports multiple data formats (CSV, JSON, etc.)
- Customizable scraping rules
- Error handling and logging -->

## Installation

### Using Docker

1. Clone the repository:

```bash
git clone https://git.wmi.amu.edu.pl/s500042/webscraper
```

2. Navigate to the project directory:

```bash
cd webscraper
```

3. Build the Docker image and run it using script:
   - On Linux, ?Mac <!-- I haven't tested it yet -->

```bash
./start.sh
```

- Windows 🤡

```bash
python start.py
```

This one will work just fine on Linux, but on Mac, you'll have to use

```bash
python3 start.py
```

### Without Docker

1. Clone the repository:

```bash
git clone https://github.com/yourusername/webscraper.git
```

2. Navigate to the project directory:

```bash
cd webscraper/app
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

If you're on Arch Linux, you'll need to create a virtual environment.
Here's is a [Step by step guide](#) that will help you create it.

## Usage

1. Configure the scraper by editing the `config.json` file.
2. Run the scraper:

```bash
python scraper.py
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
