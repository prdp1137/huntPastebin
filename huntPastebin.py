import argparse
import aiohttp
import asyncio
import os
from tqdm.asyncio import tqdm

class APIDownError(Exception):
    pass

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 502:
                raise APIDownError("API is down. Please try again later.")
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientResponseError as e:
        raise e

async def fetch_and_save_content(url, file_path, session, semaphore, rate_limit):
    async with semaphore:
        try:
            content_data = await fetch(session, url)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content_data.get('content', ''))  # Write content or empty string if missing
            return file_path
        except APIDownError:
            raise
        except Exception as e:
            print(f"Failed to fetch content from {url}. Skipping. Error: {e}")
        await asyncio.sleep(rate_limit)

async def scrape(url, dir_name, session, semaphore, rate_limit):
    print("Searching pastebin...")
    try:
        data = await fetch(session, url)
    except APIDownError:
        print("Stopping all tasks due to API downtime.")
        raise
    except Exception as e:
        print(f"Error during search: {e}")
        return

    ids = [entry['id'] for entry in data]
    if not ids:
        print(f"No data found for {url}. No files to save.")
        return

    os.makedirs(dir_name, exist_ok=True)

    tasks = [
        fetch_and_save_content(
            f"https://psbdmp.ws/api/v3/dump/{id}",
            os.path.join(dir_name, f"{id}.txt"),
            session,
            semaphore,
            rate_limit
        ) for id in ids
    ]

    try:
        # Progress bar setup
        for task in tqdm.as_completed(tasks, total=len(tasks), desc="Downloading files", unit="file"):
            await task
        # Optional: Remove directory if no files were saved
        if not any(os.path.isfile(os.path.join(dir_name, f"{id}.txt")) for id in ids):
            os.rmdir(dir_name)
    except APIDownError:
        print("Stopping all tasks due to API downtime.")
    except Exception as e:
        print(f"Error during task execution: {e}")
    else:
        print(f"Task completed. Content saved in '{dir_name}' directory.")

async def main(args):
    semaphore = asyncio.Semaphore(args.threads)  # Limit number of concurrent requests
    async with aiohttp.ClientSession() as session:
        rate_limit = args.rate_limit
        try:
            if args.general:
                await scrape(
                    f"https://psbdmp.ws/api/search/{args.general}",
                    os.path.join("general", args.general),
                    session,
                    semaphore,
                    rate_limit
                )
            elif args.email:
                await scrape(
                    f"https://psbdmp.ws/api/search/email/{args.email}",
                    os.path.join("email", args.email),
                    session,
                    semaphore,
                    rate_limit
                )
            elif args.domain:
                await scrape(
                    f"https://psbdmp.ws/api/search/domain/{args.domain}",
                    os.path.join("domain", args.domain),
                    session,
                    semaphore,
                    rate_limit
                )
        except APIDownError:
            print("API is down. Exiting.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for domains, emails, or perform a general search.")
    parser.add_argument('-g', dest='general', metavar='TERM', help='Perform a general search')
    parser.add_argument('-e', dest='email', metavar='EMAIL', help='Search for emails')
    parser.add_argument('-d', dest='domain', metavar='DOMAIN', help='Search for domains')
    parser.add_argument('-t', dest='threads', type=int, default=10, help='Number of threads (default: 10)')
    parser.add_argument('-r', dest='rate_limit', type=float, default=0, help='Rate limit in seconds between requests (default: 0)')
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        exit(0)

    asyncio.run(main(args))
