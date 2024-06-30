# captcha_tg_bot

1) `git clone git@github.com:DziumovS/captcha_tg_bot.git`
2) cd captcha_tg_bot
3) set api token and your user_id to `.env` file
4) set `correct_answer` value what you want in `main.py` (btw you can set it later via chat with bot)
5) `docker compose up -d`

### commands (for admin only):
- `/check` - to check bot status
- `/set <...>` - to set new `correct_answer` value, change '...' to your answer (for example: /set pewpew - here a new answer is 'pewpew');  
\* only one solid word can be the answer