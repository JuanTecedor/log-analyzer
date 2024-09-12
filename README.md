# Assumptions

1. Given several input files, the operations are performed on each file, not globally. For example: The total bytes exchanged option is computed in a per-file basis, not as a total between the two files.
2. For the log format, it is assumed that line with a negative response size are allowed (-1), but the total byte count is then computed with this events having a size of 0.
3. The application is made such that the log file is processed in one pass, and that all the log lines are not stored in memory. Instead, the file is processed in a line-by-line basis.
4. For the most and less frequent IPs, a IPv4 object has been stored as the key to a dict, with the value being the count. If space is important, we could consider storing a 32-bit int instead.
5. For the events per second stat, the approach selected was to count the number of events in a certain time point with a second precision. This is because the timestamps in the log files are not assumed to be ordered chronologically. If they were, we could accumulate just the counts of events per second as a list without needing a dictionary.

# How to build package

https://packaging.python.org/en/latest/tutorials/packaging-projects/

# How to run with docker compose

Examples:

```
docker compose run --entrypoint "python main.py --help" --build log-analyzer
```

```
docker compose run --entrypoint "python main.py -i logs/access-small.log -o output-docker.json --mfip --lfip --eps --bytes" --build log-analyzer
```
