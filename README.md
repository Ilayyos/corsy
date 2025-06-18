
<h1 align="center">
  <br>
  <a href="https://github.com/s0md3v/Corsy"><img src="https://i.ibb.co/K0Z7X99/corsy.png" alt="Corsy"></a>
  <br>
  Corsy
  <br>
</h1>

<h4 align="center">CORS Misconfiguration Scanner</h4>

<p align="center">
  <a href="https://github.com/s0md3v/Corsy/releases">
    <img src="https://img.shields.io/github/release/s0md3v/Corsy.svg">
  </a>
  <a href="https://github.com/s0md3v/Corsy/issues?q=is%3Aissue+is%3Aclosed">
      <img src="https://img.shields.io/github/issues-closed-raw/s0md3v/Corsy.svg">
  </a>
</p>

### Introduction
Corsy is a lightweight program that scans for all known misconfigurations in CORS implementations.

![demo](https://i.ibb.co/Jc1HtmW/corsy.png)

### Requirements
Corsy only works with `Python 3` and has just one dependency:

- `requests`

### Installation
Install the tool with `pip` to automatically handle the dependency:

```bash
pip install .
```

This will install `corsy` and make a `corsy` command available in your PATH.

### Usage
Using Corsy is pretty simple

Run it as a command after installation:

```bash
corsy -u https://example.com
```

##### Scan URLs from a file
`corsy -i /path/urls.txt`

##### Scan URLs from stdin
`cat urls.txt | corsy`

##### Number of threads
`corsy -u https://example.com -t 20`

##### Delay between requests
`corsy -u https://example.com -d 2`

##### Request timeout
`corsy -u https://example.com --timeout 5`

##### Disable TLS verification
`corsy -u https://example.com -k`

##### Export results to JSON
`corsy -i /path/urls.txt -o /path/output.json`

##### Custom HTTP headers
`corsy -u https://example.com --headers "User-Agent: GoogleBot\nCookie: SESSION=Hacked"`

##### Skip printing tips
`-q` can be used to skip printing of `description`, `severity`, `exploitation` fields in the output.

### Tests implemented
- Pre-domain bypass
- Post-domain bypass
- Backtick bypass
- Null origin bypass
- Unescaped dot bypass
- Underscore bypass
- Invalid value
- Wild card value
- Wildcard value with credentials
- Origin reflection test
- Third party allowance test
- HTTP allowance test
