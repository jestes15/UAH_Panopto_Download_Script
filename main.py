import requests
import re
import wget
import sys
import os


# Create this bar_progress method which is invoked automatically from wget
def bar_progress(current, total, width=80):
    progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
    # Don't use print() as it will print in new line every time.
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


def download_rss_file(rss_link: str, output_file: str):
    response = requests.get(rss_link)
    open(output_file, "wb").write(response.content)


def get_mp4_urls(input_file: str, pattern_guid, pattern_url):
    downloads = []
    with open(input_file) as file:
        for line in file.readlines():
            match = re.search(pattern_guid, line)
            if match:
                new_line = match.group()
                url_final = re.search(pattern_url, new_line)
                downloads.append(url_final.group())

    return downloads


def download_videos(download_array, title):
    video_number = 1
    os.mkdir(title)
    for url_val in download_array:
        wget.download(url_val, f"./{title}/{title}_{video_number}.mp4", bar=bar_progress)
        video_number += 1
        print()


if __name__ == "__main__":
    urls = []
    url_file_name = []
    video_file_name = []

    for url in range(1, len(sys.argv) - 1, 3):
        urls.append(sys.argv[url])
        url_file_name.append(sys.argv[url + 1])
        video_file_name.append(sys.argv[url + 2])

    for i in range(0, len(urls)):
        download_rss_file(urls[i], url_file_name[i])
        download = get_mp4_urls(url_file_name[i],
                                r"<guid>https:\/\/[A-Za-z0-9.\/-]{0,}<\/guid>",
                                r"https:\/\/[A-Za-z0-9.\/-]{0,}")
        download_videos(download, video_file_name[i])
