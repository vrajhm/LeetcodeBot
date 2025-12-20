# LeetCode Discord Bot

A Discord bot that delivers daily LeetCode coding challenges with customizable difficulty levels.

## Features

- **Daily Challenges**: Automatically post LeetCode problems or request them on-demand
- **Difficulty Control**: Specify easy, medium, or hard problems, or let the bot randomize
- **Problem Details**: Bot provides problem descriptions and links for solving

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your Discord bot token:
    ```
    DISCORD_TOKEN=your_token_here
    ```
4. Run the bot: `python bot.py`

## Usage

- `/challenge` - Request a random difficulty challenge
- `/challenge difficulty:easy|medium|hard` - Request a specific difficulty
- `/daily` - Enable daily challenges (configurable schedule)

## Requirements

- Python 3.8+
- Discord.py
- LeetCode API integration
