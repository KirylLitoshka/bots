from catalogues.patrona.bot_bruna.bot import bruna_bot
from catalogues.patrona.bot_daniel.bot import daniel_bot
from catalogues.patrona.bot_denis.bot import denis_bot
from catalogues.patrona.bot_james.bot import james_bot
from catalogues.patrona.bot_minho.bot import minho_bot
from catalogues.patrona.bot_rena.bot import rena_bot
from catalogues.patrona.bot_mother.bot import patrona_mother_bot

from catalogues.readdly.bot_josh.bot import josh_bot
from catalogues.readdly.bot_krystal.bot import krystal_bot
from catalogues.readdly.bot_lina.bot import lina_bot
from catalogues.readdly.bot_reina.bot import reina_bot
from catalogues.readdly.bot_mother_readdly.bot import readdly_mother_bot

from catalogues.diagnosis.bot import diagnosis_bot
from catalogues.policy.bot import policy_bot

DISPATCHERS = {
    "bruna": bruna_bot,
    "daniel": daniel_bot,
    "denis": denis_bot,
    "james": james_bot,
    "minho": minho_bot,
    "rena": rena_bot,
    "patrona": patrona_mother_bot,
    "josh": josh_bot,
    "krystal": krystal_bot,
    "lina": lina_bot,
    "reina": reina_bot,
    "readdly": readdly_mother_bot,
    "diagnosis": diagnosis_bot,
    "policy": policy_bot
}
