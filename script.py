import time
import requests
import magic
from rich.console import Console
from rich.table import Table

URLS = [
    "https://samplefile.com/samples/download/image/png/png_sample_file_10MB.png",
    "https://devlab.itlibra.com/files/images/png/png-10mb.png",
]


class DownloadTester:
    def __init__(self, urls, iterations=10):
        self.urls = urls
        self.iterations = iterations
        self.console = Console()
        self.session = requests.Session()

    def get_valid_image_url(self):
        for url in self.urls:
            try:
                self.console.print(f"🌐 [yellow]Checking URL[/yellow]: {url}")

                response = self.session.get(url, timeout=10)
                response.raise_for_status()

                content_type = response.headers.get("Content-Type", "unknown")
                mime_type = magic.from_buffer(response.content, mime=True)

                if "image" not in mime_type:
                    self.console.print(
                        f"[red]❌ Not an image[/red] | "
                        f"Server type: {content_type} | "
                        f"Actual type: {mime_type}"
                    )
                    continue

                return url

            except requests.RequestException:
                self.console.print(f"[red]❌ Invalid URL:[/red] {url}")

        raise RuntimeError("No valid image URLs found")

    def download(self, url):
        request_durations = []
        response_sizes = []

        self.console.print(f"\n⚡ Downloading an image...")

        for attempt in range(self.iterations):
            start = time.perf_counter()

            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            elapsed = time.perf_counter() - start
            size = len(response.content) / (1024 * 1024)

            request_durations.append(elapsed)
            response_sizes.append(size)

            self.console.print(
                f"[#FFA500]#{attempt+1}[/] " f"{elapsed:.3f}s " f"{size:.2f} MB"
            )

        return request_durations, response_sizes

    def show_report(self, url, request_durations, response_sizes):
        total_duration = sum(request_durations)
        total_size = sum(response_sizes)

        average_request_time = total_duration / len(request_durations)
        download_speed = total_size / total_duration

        table = Table(title="Internet Speed Test")

        table.add_column("Metric")
        table.add_column("Value")

        table.add_row("URL", url)
        table.add_row("Average Request time", f"{average_request_time:.3f}s")
        table.add_row("Download", f"{total_size:.2f} MB")
        table.add_row("Speed", f"{download_speed:.2f} MB/s")

        self.console.print(table)

    def run(self):
        url = self.get_valid_image_url()
        request_durations, response_sizes = self.download(url)
        self.show_report(url, request_durations, response_sizes)


if __name__ == "__main__":
    DownloadTester(URLS).run()
