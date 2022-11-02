# plof -> plotext command line tool

- [x] -xlim and -ylim limits
- [] -empty for a plain graph
- [] -json for json input. Use 'jq' syntax
- [] -csv for csv input.
- [x] -host / -port for network
- [] -pipe for stdin (will block on buffering though)
- [x] -refresh rate of refresh for graph
- [] -title for title of graph

## Overview

Plof allows you to pipe and read data from many sources, parse and aggregate on it, and then plot or display the metrics in the way you want. Plof makes no attempt at being platform specific. It is completely extendable through the use of other command line tools or custom scripts (including additional python). For convience sake, there are some built in tools for some data sources and parsing logic as well.

### Why not just use bash?

Bash can do the same thing. Stich together some complex pipes and download a bunch of tools and your done! Well! To that I say: I've added additional features where bash is lacking including centralization (everything in one tool without a million dependencies), an advanced buffering and aggregation layer that regular UNIX pipes do not allow for, easy terminal GUI's for graphing and display, and easy to read and understand yaml configurations instead of command line arguments. Is it revolutionary? No. Is it really convient? Yes.

Basically, this tool is meant to simplify reading from devices and their metrics and create a universal tool that many teams (Software, Field Service, Site Reliability, DevOps, whatever you want to call yourself) can use. This builds trust amoung teams so that all teams will have the same experience and the same data to observe.

### Why in Python?

This is a valuable question. Python is slow-ish. It's not type safe. It can get messy. BUT! It's fricken easy. A lot of thought went into this tool before any code was written in order to ensure some standard coding practices, semi-typed usage, lots of documentation, and logically layed out code that just makes sense. I can do a lot in a few lines of code with the native Python libs that I simply cannot do with other programming languages. I like Rust, sometimes Java, I know C, some basic C++, too much Javascript, and a few others... BUT! This language is just too comprehensive to not make it the obvious choice.



## How it works (PPP)

```
[Pipe] -> [Parse] -> [Plot]
```

The [Pipe] will recieve data continously on a polling interval or as a push message. It will never fail or hang up unless no data is coming through. This is the only required step! If no other steps are provided, then this will just print to standard output.

The [Parse] will format the data into whatever you want, but in addition, allow the user to buffer and aggregate on parsed metrics if so desired.

The [Plot] will then take the formatted data and display it to the user in the format of a graph, table, or raw.

## What can you do with it?

In keeping with the "terminal only" mentality, I like to pair it with `tmux` and `tmuxp` profiles. This allows me to quickly setup a profile that I can share with my team to monitor different devices directly in the terminal. 

## Examples

### Load from a file. No command line arguments to remember!

```
plof ~/.plof/monitor-sensor-metrics.yml
```

But, there is some help avaliable if you want it

```
plof --help
```

### MQTT JSON data to a line graph

```
pipe:
    type: mqtt
    config:
        url: mqtt://127.0.0.1:1883
        topic: sensor/1/metrics
parse:
    type: json
    config:
        expression: .data[0].temperature
        datatype: float
        buffer: 5
        aggregate: avg
plot:
    type: line
    refresh: 5s
```

### HTTP get yaml data and display in a table

```
pipe:
    type: http
    config:
        url: http://sensor.com/1/metrics
        poll: 5s
parse:
    type: yaml
    config:
        expression: .data
        datatype: csv
plot:
    type: table
    refresh: 5s
```

### Listen to a serial port for total bitrate in a bar graph

```
pipe:
    type: serial
    config:
        file: "/dev/USB01"
        baudrate: 9600
parse: 
    type: raw
    config:
        buffer: 5s
        aggregate: total
plot:
    type: bar
    title: "Total Bitrate (5s) on /dev/USB01"
    refresh: 5s
```

### Pipe data from journalctl command, parse errors with grep, find total lines, and graph as a line

```
pipe:
    type: exec
    config:
        command: journalctl -f -u systemd-service
parse:
    type: exec
    config:
        command: "grep error"
        deliminator: "\n"
        buffer: 5s
        aggregate: total
plot:
    type: line
    refresh: 5s
```

### Pipe data into gnuplot (has to be installed seperately)

```
pipe:
  type: sin
  config:
    poll: 500ms
    amplitude: 100
parse:
  - type: cast
    config:
      cast: float
  - type: rolling_average
    config:
      window: 10
plot:
  type: gnuplot
  config:
    refresh: 5s
```

### Apply multiple parse commands

```
pipe:
    type: exec
    config:
        command: journalctl -f -u systemd-service
parse:
    - type: split
    config:
        deliminator: "\n"
    - type: cast
    config:
        cast: json
    - type: pointer
    config:
        pointer: "/data/sensor"
    - type: rolling_average
    config:
        window: 10
plot:
    type: line
    refresh: 5s
```

## Other

```
gstdbuf -oL python3 gen.py -random -mult 5 -sleep 0.01 | ncat --keep-open --listen -p 4000

# tcp
gstdbuf -oL python3 gen.py -sin -mult 5 | ncat --keep-open --listen -p 4000

# udp
gstdbuf -oL python3 gen.py -sin -mult 5 | ncat -u --listen -p 4000 
```

```
plof -ylim="-1,1" -type raw -refresh 5 -timeout 1 -buffer 100 -host 127.0.0.1 -port 4000

gstdbuf -oL python3 gen.py -random -mult 5 | plof -ylim="-5,5" -type raw -refresh 1 -timeout 1 -buffer 100 -pipe
```

