import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Emoji mapping for difficulty
DIFFICULTY_EMOJIS = {
    "EASY": "🟢",
    "MEDIUM": "🟡",
    "HARD": "🔴"
}


def get_random_problem(difficulty="MEDIUM"):
    difficulty = difficulty.upper()
    
    query = """
    query problemsetQuestionListV2($limit: Int, $skip: Int) {
      problemsetQuestionListV2(limit: $limit, skip: $skip) {
        questions {
          title
          titleSlug
          difficulty
          topicTags {
            name
          }
        }
      }
    }
    """
    variables = {"limit": 100, "skip": 0}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://leetcode.com/problemset/all/"
    }

    try:
        response = requests.post(
            "https://leetcode.com/graphql",
            json={"query": query, "variables": variables},
            headers=headers,
            timeout=10
        )
        if response.status_code != 200:
            return f"⚠️ LeetCode error {response.status_code}"

        data = response.json()
        if "data" not in data:
            return f"⚠️ API error: {data}"

        all_problems = data["data"]["problemsetQuestionListV2"]["questions"]

        # Filter by difficulty
        filtered = [p for p in all_problems if p["difficulty"] == difficulty]
        if not filtered:
            return f"⚠️ No {difficulty.title()} problems found."

        problem = random.choice(filtered)

        # Format topics nicely
        topics = ", ".join([t["name"] for t in problem.get("topicTags", [])]) or "None"


        # Compose embed-like message
        message = (
            f"{DIFFICULTY_EMOJIS.get(problem['difficulty'], '')} **Daily LeetCode Challenge!** {DIFFICULTY_EMOJIS.get(problem['difficulty'], '')}\n\n"
            f"**Problem:** {problem['title']}\n"
            f"**Difficulty:** {problem['difficulty'].title()}\n"
            f"**Topics:** {topics}\n\n"
            f"🔗 Solve here: https://leetcode.com/problems/{problem['titleSlug']}/\n"
        )

        return message

    except requests.exceptions.RequestException as e:
        return f"⚠️ Network error: {e}"


@bot.command()
async def daily(ctx, difficulty: str = "hard"):
    """Send a random LeetCode problem with optional difficulty"""
    difficulty = difficulty.lower()
    if difficulty not in ["easy", "medium", "hard"]:
        await ctx.send("⚠️ Difficulty must be 'easy', 'medium', or 'hard'.")
        return

    message = get_random_problem(difficulty)
    await ctx.send(message)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')


bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
