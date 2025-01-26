import datetime
from homeassistant.helpers.entity import Entity

def er_skudaar(aar):
    return aar % 4 == 0 and (aar % 100 != 0 or aar % 400 == 0)

def beregn_paaskedag(aar):
    a = aar % 19
    b = aar // 100
    c = aar % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    maaned = (h + l - 7 * m + 114) // 31
    dag = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(aar, maaned, dag)

def beregn_helligdage(aar):
    helligdage = {}
    helligdage["dkh_nytaarsdag"] = datetime.date(aar, 1, 1)
    helligdage["dkh_grundlovsdag"] = datetime.date(aar, 6, 5)
    helligdage["dkh_juleaften"] = datetime.date(aar, 12, 24)
    helligdage["dkh_juledag"] = datetime.date(aar, 12, 25)
    helligdage["dkh_anden_juledag"] = datetime.date(aar, 12, 26)

    paaskedag = beregn_paaskedag(aar)
    helligdage["dkh_skaertorsdag"] = paaskedag - datetime.timedelta(days=3)
    helligdage["dkh_langfredag"] = paaskedag - datetime.timedelta(days=2)
    helligdage["dkh_paaskedag"] = paaskedag
    helligdage["dkh_anden_paaskedag"] = paaskedag + datetime.timedelta(days=1)
    helligdage["dkh_store_bededag"] = paaskedag + datetime.timedelta(days=26)
    helligdage["dkh_kristi_himmelfartsdag"] = paaskedag + datetime.timedelta(days=39)
    helligdage["dkh_pinsedag"] = paaskedag + datetime.timedelta(days=49)
    helligdage["dkh_anden_pinsedag"] = paaskedag + datetime.timedelta(days=50)
    helligdage["dkh_fastelavnssoendag"] = paaskedag - datetime.timedelta(days=49)

    juleaften = datetime.date(aar, 12, 24)
    foerste_advent = juleaften - datetime.timedelta(days=juleaften.weekday() + 22)
    helligdage["dkh_1_sondag_i_advent"] = foerste_advent
    helligdage["dkh_2_sondag_i_advent"] = foerste_advent - datetime.timedelta(days=-7)
    helligdage["dkh_3_sondag_i_advent"] = foerste_advent - datetime.timedelta(days=-14)
    helligdage["dkh_4_sondag_i_advent"] = foerste_advent - datetime.timedelta(days=-21)

    return helligdage

def setup_platform(hass, config, add_entities, discovery_info=None):
    aar = datetime.datetime.now().year
    helligdage = beregn_helligdage(aar)
    sensorer = []

    for navn, dato in helligdage.items():
        sensorer.append(HelligdagsSensor(navn, dato))

    sensorer.append(SkudaarSensor(aar, er_skudaar(aar)))
    skuddags_dato = datetime.date(aar, 2, 29) if er_skudaar(aar) else None
    sensorer.append(SkuddagsSensor(skuddags_dato))

    add_entities(sensorer, True)

class HelligdagsSensor(Entity):
    def __init__(self, navn, dato):
        self._navn = navn
        self._dato = dato

    @property
    def name(self):
        return self._navn

    @property
    def state(self):
        return self._dato

    @property
    def extra_state_attributes(self):
        return {
            "venligt_navn": self._navn,
            "dato": self._dato
        }

class SkudaarSensor(Entity):
    def __init__(self, aar, er_skudaar):
        self._navn = f"dkhelligdag_skudaar_{aar}"
        self._er_skudaar = er_skudaar

    @property
    def name(self):
        return self._navn

    @property
    def state(self):
        return self._er_skudaar

    @property
    def extra_state_attributes(self):
        return {
            "venligt_navn": self._navn,
            "er_skudaar": self._er_skudaar
        }

class SkuddagsSensor(Entity):
    def __init__(self, dato):
        self._navn = "dkhelligdag_skuddagen"
        self._dato = dato

    @property
    def name(self):
        return self._navn

    @property
    def state(self):
        return self._dato

    @property
    def extra_state_attributes(self):
        return {
            "venligt_navn": self._navn,
            "dato": self._dato
        }
