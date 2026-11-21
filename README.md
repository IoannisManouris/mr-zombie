# Mr Zombie

A Discord bot for random animal pictures, facts, memes, and server statistics.

## Purpose and audience

Mr Zombie gives Discord members a handful of one-command diversions and gives moderators a quick picture of the server's membership and channels.

## How it works

The bot registers five slash commands. Four call external services and return a fact or media URL. The server summary reads Discord's member cache, counts people and bots separately, and reports channels, roles, boosts and the verification level.

## Quick start

From the repository root, use Python 3.12 in a virtual environment. The following commands use a POSIX shell. In PowerShell, activate the environment with `.venv\Scripts\Activate.ps1` and use `Copy-Item` in place of `cp`.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env

```

## Configuration

Set `DISCORD_TOKEN` in `.env`. Add an `IMGUR_CLIENT_ID` to enable `/meme`. Enable the Server Members intent so the member totals are available. Invite the application with the bot and application commands scopes and grant View Channel, Send Messages and Embed Links in the test channel.

## Deployment and commands

Start the bot with `python mrzombie.py` after filling in its configuration. A deployment needs one running Python process with the same configuration as the local run. An existing process environment takes precedence over `.env`.

Try `/dog` or `/cat` for a picture, `/fact` for a random fact and `/meme` for an Imgur result. Run `/server_info` inside a server to see membership and channel totals.

## Testing and troubleshooting

Run `python -m py_compile mrzombie.py` for a syntax check. CI installs the dependencies and checks command registration offline. To check the Discord connection and provider responses, use the commands above in a test server.

If only memes fail, check the Imgur client ID and quota. If member totals look incomplete, check the Server Members intent. Animal and fact results depend on the external providers being available.

## Project history and release status

The original folder has a creation timestamp of May 25, 2024. The surviving `mrzombie.py` file was created June 2 and last modified June 8, 2024 (UTC filesystem timestamps). The first public release date is unknown.

This repository preserves the source as a historical project. No versioned release is recorded.

## Support and security

Open a repository issue for a reproducible bug. For credentials or vulnerabilities, use the private reporting route in [SECURITY.md](SECURITY.md). The [license notice](LICENSE) records the project's reuse terms.
