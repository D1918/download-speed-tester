## Download Speed Tester (Test task)

This project is a simple script that measures internet download speed.

## Task:
Write a script that measures internet speed from your computer. It should accept a URL (a large image), run 10 sequential requests to it, wait for each response, calculate average request time, total downloaded data, and print speed in MB/s.

---

## Run with Docker

### Build image

```bash
docker build -t download-speed-tester .
```

### Run container

```bash
docker run --rm download-speed-tester
```
