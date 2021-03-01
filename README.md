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

Note that if you run this script with `targets.txt` without modifying - it will consume around 1.5Gb RAM.
And if a subnet is even wider than x.x.0.0/16 - the consumption will increase even more.

### Shell

```shell
python main.py
```

Then check your log collector for results.

### Docker

First build an image with `docker build . -t checker`.

Run `docker run --rm --name checker -v $(pwd)/config.yaml:/app/config.yaml -v $(pwd)/targets.txt:/app/targets.txt checker`