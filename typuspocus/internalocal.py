import locale
import gettext
import os

locale_dir = os.path.join(os.path.dirname(__file__), "locale")

def getLanguage():
    '''Returns the language to be used by the system.

    Si encuentra el lenguaje del sistema dentro de lo
    traducido, lo devuelve, sino None.
    '''
    try:
        loc = locale.setlocale(locale.LC_ALL, "")
    except:
        return None
    loc = loc[:2]
    traducidos = os.listdir(locale_dir)
    if loc in traducidos:
        return loc
    return

gettext.install('core', locale_dir, unicode=True)
idioma = getLanguage()
if idioma is not None:
    mo = os.path.join(locale_dir, '%s/LC_MESSAGES/core.mo' % idioma)
    if not os.access(mo, os.F_OK):
        raise IOError, "The l10n directory (for language %r) exists but not the core.mo file" % idioma
    gettext.translation('core', locale_dir, languages=[idioma]).install()

y = _
def x(s):
    translated = y(s)
    if translated.__class__ is unicode:
        return translated
    return unicode(translated, "utf8")
__builtins__["_"] = x

