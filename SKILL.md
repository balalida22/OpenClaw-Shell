## Skill: File System Management

- List files: `ls -la <path>`
- Find files by name: `find <path> -name "<pattern>"`
- Find files by content: `grep -r "<text>" <path>`
- Create directories: `mkdir -p <path>`
- Copy files: `cp -r <src> <dst>`
- Move/rename: `mv <src> <dst>`
- Delete safely: `rm -r <path>`
- Check disk usage: `du -sh <path>` or `df -h`
- Check file type: `file <path>`

---

## Skill: Reading & Editing Files

- Print file contents: `cat <file>`
- Print with line numbers: `cat -n <file>`
- View large files page by page: `less <file>`
- Print first/last N lines: `head -n <N> <file>` / `tail -n <N> <file>`
- Search within a file: `grep -n "<pattern>" <file>`
- Replace text in file: `sed -i 's/<old>/<new>/g' <file>`
- Count lines/words: `wc -l <file>` / `wc -w <file>`
- Compare two files: `diff <file1> <file2>`

---

## Skill: Package Management

- Update package list: `sudo apt update`
- Upgrade all packages: `sudo apt upgrade -y`
- Install a package: `sudo apt install -y <package>`
- Remove a package: `sudo apt remove -y <package>`
- Search for a package: `apt search <package>`
- Check if installed: `dpkg -l | grep <package>`
- Install Python packages: `pip install <package>` or `pip3 install <package>`

---

## Skill: Process Management

- List running processes: `ps aux`
- Search for a process: `ps aux | grep <name>`
- Kill a process by name: `pkill <name>`
- Kill a process by PID: `kill -9 <pid>`
- Monitor system resources: `top` or `htop`
- Check CPU/memory usage: `free -h` and `vmstat`
- Run a command in background: `<command> &`
- Check background jobs: `jobs`

---

## Skill: Networking

- Check IP address: `ip addr show`
- Check open ports: `ss -tulnp`
- Test connectivity: `ping -c 4 <host>`
- Download a file: `wget <url>` or `curl -O <url>`
- Fetch URL content: `curl -s <url>`
- Check DNS resolution: `nslookup <domain>`
- Trace network route: `traceroute <host>`
- Check active connections: `netstat -antp`

---

## Skill: Python Development

- Run a script: `python3 <script.py>`
- Create a virtual environment: `python3 -m venv <env>`
- Activate virtual environment: `source <env>/bin/activate`
- Install from requirements: `pip install -r requirements.txt`
- List installed packages: `pip list`
- Check Python version: `python3 --version`
- Run a quick expression: `python3 -c "<expression>"`

---

## Skill: Git

- Clone a repo: `git clone <url>`
- Check status: `git status`
- Stage changes: `git add .`
- Commit: `git commit -m "<message>"`
- Push: `git push`
- Pull latest: `git pull`
- Check log: `git log --oneline -10`
- Create branch: `git checkout -b <branch>`
- Switch branch: `git checkout <branch>`

---

## Skill: Compression & Archives

- Create tar.gz: `tar -czf <archive.tar.gz> <folder>`
- Extract tar.gz: `tar -xzf <archive.tar.gz>`
- Create zip: `zip -r <archive.zip> <folder>`
- Extract zip: `unzip <archive.zip>`
- List archive contents: `tar -tzf <archive.tar.gz>`

---

## Skill: System Information

- OS info: `lsb_release -a`
- Kernel version: `uname -r`
- CPU info: `lscpu`
- Memory info: `free -h`
- Disk info: `lsblk`
- Uptime: `uptime`
- Current user: `whoami`
- Environment variables: `env`
- Check a specific variable: `echo $<VAR>`

---

## Skill: Video Downloading with yt-dlp

- Download a video (best quality): `yt-dlp <url>`
- Download audio only (mp3): `yt-dlp -x --audio-format mp3 <url>`
- Download audio only (best quality): `yt-dlp -x --audio-quality 0 <url>`
- Download to a specific folder: `yt-dlp -o "<path>/%(title)s.%(ext)s" <url>`
- Download specific resolution: `yt-dlp -f "bestvideo[height<=1080]+bestaudio" <url>`
- List available formats: `yt-dlp -F <url>`
- Download a specific format by ID: `yt-dlp -f <format_id> <url>`
- Download a playlist: `yt-dlp -o "%(playlist_index)s-%(title)s.%(ext)s" <playlist_url>`
- Download playlist range: `yt-dlp --playlist-start 1 --playlist-end 5 <playlist_url>`
- Download with subtitles: `yt-dlp --write-subs --sub-lang en <url>`
- Embed subtitles into video: `yt-dlp --embed-subs <url>`
- Download thumbnail: `yt-dlp --write-thumbnail <url>`
- Embed thumbnail into file: `yt-dlp --embed-thumbnail <url>`
- Limit download speed: `yt-dlp --rate-limit 1M <url>`
- Resume interrupted download: `yt-dlp -c <url>`
- Show video metadata without downloading: `yt-dlp --dump-json <url>`
- Update yt-dlp to latest version: `yt-dlp -U`
- Install yt-dlp if not present: `pip install yt-dlp`