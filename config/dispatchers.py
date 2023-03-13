from catalogues.patrona.bot_bruna.bot import bruna_bot
from catalogues.patrona.bot_daniel.bot import daniel_bot
from catalogues.patrona.bot_denis.bot import denis_bot
from catalogues.patrona.bot_james.bot import james_bot
from catalogues.patrona.bot_minho.bot import minho_bot
from catalogues.patrona.bot_rena.bot import rena_bot
from catalogues.patrona.bot_mother.bot import patrona_mother_bot

DISPATCHERS = {
    "bruna": bruna_bot,
    "daniel": daniel_bot,
    "denis": denis_bot,
    "james": james_bot,
    "minho": minho_bot,
    "rena": rena_bot,
    "patrona": patrona_mother_bot
}
