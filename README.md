# save-link

A simple tool to save links to the server. 
The bot will save the link to the [slash](https://github.com/yourselfhosted/slash).
If the link is rss feed, it will save the feed to the [miniflux](https://github.com/miniflux/v2)

## Installation

### Manual

```bash
python -m venv venv # create a virtual environment
source venv/bin/activate # activate the virtual environment
pip install -r requirements.txt # install the dependencies
mv config-example.py config.py
python bot.py
```

### Docker

```bash
docker compose up -d
```

## TODO

- [x] Set visibility of the link
- [ ] Add rss feed to miniflux
- [ ] Show unread articles from miniflux
