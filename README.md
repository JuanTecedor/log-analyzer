```
head access.log > access-small.log
grep "10.105.21.199" logs/access.log | wc -l
```

# How to build package

https://packaging.python.org/en/latest/tutorials/packaging-projects/

# How to run with docker compose

Example with all the arguments:

```
docker compose run --entrypoint "python main.py -i logs/access-small.log -o output-docker.json --mfip --lfip --eps --bytes" --build log-analyzer
```
