# First time running Docker

```
mkdir out-docker
sudo chown -R 10001 out-docker
docker compose run --entrypoint "python main.py -i logs/access-small.log -o out-docker/output-docker.json --mfip --lfip --eps --bytes" --build log-analyzer
```