import argparse
import requests

def scrape(url):
    print("Searching pastebin...")
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    ids = [entry['id'] for entry in data]
    urls = [f"https://pastebin.com/{id}" for id in ids]

    print("Task completed. Output URLs:")
    for url in urls:
        print(url)

    return 0

parser = argparse.ArgumentParser(description="Search for domains, emails, or perform a general search.")

parser.add_argument('-g', dest='general', metavar='TERM', help='Perform a general search')
parser.add_argument('-e', dest='email', metavar='EMAIL', help='Search for emails')
parser.add_argument('-d', dest='domain', metavar='DOMAIN', help='Search for domains')

args = parser.parse_args()

if not any(vars(args).values()):
    parser.print_help()
    exit(0)

if args.general:
    dir = f"general/{args.general}"
    url = f"https://psbdmp.ws/api/search/{args.general}"
    scrape(url)

elif args.email:
    dir = f"email/{args.email}"
    url = f"https://psbdmp.ws/api/search/email/{args.email}"
    scrape(url)

elif args.domain:
    dir = f"domain/{args.domain}"
    url = f"https://psbdmp.ws/api/search/domain/{args.domain}"
    scrape(url)
