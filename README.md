# plof -> plotext command line tool

[x] -xlim and -ylim limits
[] -empty for a plain graph
[] -json for json input. Use 'jq' syntax
[] -csv for csv input.
[x] -host / -port for network
[] -pipe for stdin (will block on buffering though)
[x] -refresh rate of refresh for graph
[] -title for title of graph


```
gstdbuf -oL python3 gen.py -random -mult 5 -sleep 0.01 | ncat --keep-open --listen -p 4000


# tcp
gstdbuf -oL python3 gen.py -sin -mult 5 | ncat --keep-open --listen -p 4000

# udp
gstdbuf -oL python3 gen.py -sin -mult 5 | ncat -u --listen -p 4000 
```

```
plof -ylim="-1,1" -type raw -refresh 5 -timeout 1 -buffer 100 -host 127.0.0.1 -port 4000

gstdbuf -oL python3 gen.py -sin -mult 5 | plof -ylim="-1,1" -type raw -refresh 5 -timeout 1 -buffer 100 -pipe
```
