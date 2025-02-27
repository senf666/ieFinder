
# .ie finder

.ie finder is a python based application that finds and logs `.ie` domain names by checking certificate transparency logs in near real-time.

<img  alt="image"  src="screenshot.png">


## Features

- Logs `.ie` domain names to text files.
- Generates logs in multiple formats: `.txt`, `.csv`.
- Provides verbose output for all tlds (top level domains) passing through using --verbose flag.
- Displays hyperlinks to the found `.ie` domains.

## Requirements

- Python 3.x

# Installation

```bash
$ python3  -m  venv  .venv
$ source  .venv/bin/activate
$ pip  install  -r  requirements.txt
```

  

# Usage
```bash
$$ python3 ieFinder.py

    _         _____  _             _             
   (_)  ___  |  ___|(_) _ __    __| |  ___  _ __ 
   | | / _ \ | |_   | || '_ \  / _` | / _ \| '__|
 _ | ||  __/ |  _|  | || | | || (_| ||  __/| |   
(_)|_| \___| |_|    |_||_| |_| \__,_| \___||_|   
                                                 
 The .ie domain name finder | Github

[2025-02-27 00:04:05] old.idpd.ecoserve.ie
[2025-02-27 00:04:09] www.icecompanyinc.ie
[2025-02-27 00:05:06] qjcmekguojdoy8w.mail.yt.m3dia.ie
[2025-02-27 00:05:11] quantumfulfilment.ie
[2025-02-27 00:05:11] *.tiltinsurance.ie
[2025-02-27 00:05:12] help.apexit.ie
[2025-02-27 00:05:14] draft.kmk.ie
[2025-02-27 00:05:39] *.ruby-consulting.ie
[2025-02-27 00:06:13] driveinc.ie
[2025-02-27 00:06:23] www.autoconfig.avalon-house.ie
[2025-02-27 00:06:36] www.autoconfig.avalon-house.ie
[2025-02-27 00:06:37] *.ruby-consulting.ie
...
```

# Output
.ie Finder produces 4 log files:
```

├── log.txt       contains a log of what happened.
├── certstream.txt certstream log.
├── domains.txt   contains .ie domain names.
└── www.txt       contains .ie domain names without subdomains, just www.domainName.ie
```

# Attribution
.ie Finder is heavily based on CertSniff by A-poc https://github.com/A-poc/certSniff



