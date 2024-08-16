# HuntPastebin

HuntPastebin is a command-line tool designed to search for leaked information on the web using the psbdmp.ws API. It can search for domains, emails, or perform a general search.

## Installation

1. **Clone the repository:**
    ```shell
    git clone https://github.com/pr0d33p/huntPastebin.git
    ```

2. **Navigate to the project directory:**
    ```shell
    cd huntPastebin
    ```

3. **Install the required dependencies:**
    ```shell
    pip install -r requirements.txt
    ```

## Usage

### Search for Domains

To search for information related to a domain, use:
```shell
python huntPastebin.py -d domain.com
```

### Search for Emails

To search for information related to an email, use:
```shell
python huntPastebin.py -e foo@bar.com
```

### General Search

To perform a general search, use:
```shell
python huntPastebin.py -g search_term
```

## Advanced Options

- **Number of Threads (`-t`):** Control how many threads the tool uses for searching. Default is 10. Example:
    ```shell
    python huntPastebin.py -d domain.com -t 20
    ```

- **Rate Limit (`-r`):** Set a delay between requests to avoid hitting API rate limits. Default is 0 (no delay). Example:
    ```shell
    python huntPastebin.py -d domain.com -r 2
    ```

## Output

The tool saves the results in text files within a directory named according to the search type. Each file contains the content of the search result. It also provides a simple progress update as it works.

## Example

For a domain search with a custom number of threads and rate limit:
```shell
python huntPastebin.py -d domain.com -t 20 -r 1
```

This command searches for `domain.com` using 20 threads and waits 1 second between requests.
