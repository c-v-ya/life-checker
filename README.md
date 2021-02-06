# Life Checker

Checks if server is alive via `Head` request.

## Prerequisites

Update `config.yaml` and `targets.txt` to your needs.

Make sure your logstash instances are up and running, and able to receive json via `http` input.

Example `logstash.conf` input config:

```
input {
  http {
    port => 5044
  }
}
```

## Usage

### Shell

```shell
python main.py
```

Then check your log collector for results.

### Docker

First build an image with `docker build . -t checker`.

Run `docker run --rm --name checker -v $(pwd)/config.yaml:/app/config.yaml -v $(pwd)/targets.txt:/app/targets.txt checker`