import re
import os


def extract_and_remove_image_link(markdown_str):
    pattern = r"!\[.*?\]\((.*?)\)"
    urls = re.findall(pattern, markdown_str)
    modified_markdown = re.sub(pattern, "", markdown_str)
    return urls[0], str(modified_markdown).strip()


def process_artifact(artifact):
    print("New matplotlib chart generated:", artifact.name)
    file = artifact.download()
    basename = os.path.basename(artifact.name)
    with open(f"./resources/outputs/{basename}", "wb") as f:
        f.write(file)


def process_response(response):
    if 'sandbox' in response:
        url, response = extract_and_remove_image_link(response)
        url = url.replace("sandbox:/home/user/artifacts/", './resources/outputs/')
        return [
            {"type": "text", "output": response},
            {"type": "image", "output": url}
        ]

    return [{"type": "text", "output": response}]


stt = """
Here is the scatter plot showing the relationship between the total number of rooms and the population.

![Total Rooms vs Population](sandbox:/home/user/artifacts/figure_20240101-015233.png)
"""

if __name__ == '__main__':
    print(process_response(stt))
