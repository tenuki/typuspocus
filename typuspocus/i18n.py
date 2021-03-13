"""Set up the internationalization and provide a better function to translate than underscore."""

import gettext
import os

# install the translation service
base = os.path.dirname(os.path.realpath(__file__))
locale_dir = os.path.join(base, "locale")
gettext.install('core', locale_dir)

tr = _  # NOQA: this was set by gettext
