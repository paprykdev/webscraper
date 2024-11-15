# Web scraper 🔍

## Description

This project is a web scraper designed to extract data from websites.

## Features

☑️ Extracts data from web pages

## Usage

### With Docker

1. Clone the repository:

```bash
git clone https://git.wmi.amu.edu.pl/s500042/webscraper
```

2. Navigate to the project directory:

```bash
cd webscraper
```

3. Build the Docker image and run it using `start.py` script:

```bash
python scripts/start.py
```

On Mac, you'll have to use

```bash
python3 scripts/start.py
```

4. Check `/app/dist/data.json` file to see the extracted data.

### Without Docker

1. Clone the repository:

```bash
git clone https://git.wmi.amu.edu.pl/s500042/webscraper
```

2. Install the required dependencies:

```bash
pip install -r app/requirements.txt
```

If you're on Arch Linux, you'll need to create a virtual environment.
Here's is a [Step by step guide](#) that will help you create it.

3. Run `run_with_no_docker.py` script:

```bash
python scripts/run_with_no_docker.py
```

On Mac you'll, need to use:

```bash
python3 scripts/run_with_no_docker.py
```

4. Check `/app/dist/data.json` file to see the extracted data.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
