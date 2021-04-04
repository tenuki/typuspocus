"""A simple storage for saving hi scores."""

import json
import os
import time
from operator import itemgetter

HISCORE_FILENAME = os.path.expanduser(
    "~/.local/share/typuspocus/hiscores")


class _HiScore:
    """Keep a persisted and sorted list of hiscores.

    The highest score is first. In case of tie, the older wins.
    """

    def __init__(self):
        self._hiscores = self._load()

    def _load(self):
        try:
            with open(HISCORE_FILENAME, "rt", encoding="utf8") as fh:
                return json.load(fh)
        except (IOError, ValueError):
            # file not found or broken, no problem
            print("WARNING: couldn't load hi scores file from", repr(HISCORE_FILENAME))
            return []

    def _save(self):
        dirname = os.path.dirname(HISCORE_FILENAME)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        try:
            with open(HISCORE_FILENAME, "wt", encoding="utf8") as fh:
                json.dump(self._hiscores, fh)
        except IOError:
            print("ERROR: couldn't save hi scores to", repr(HISCORE_FILENAME))

    def add(self, score, name):
        """Add a score to the list, leaving it properly ordered, and save."""
        self._hiscores.append(dict(score=score, name=name, tstamp=time.time()))

        # take advante of stable ordering
        self._hiscores.sort(key=itemgetter('tstamp'))
        self._hiscores.sort(key=itemgetter('score'), reverse=True)

        self._save()

    def list(self):
        """Return the hi scores.

        A copy, so we're sure the exterior doesn't mess with the data.
        """
        return self._hiscores.copy()


hiscore = _HiScore()

if __name__ == '__main__':
    # don't mess with real hiscores
    HISCORE_FILENAME = "/tmp/hiscore.test"

    hiscore.add(34, "Juan")
    time.sleep(.1)
    hiscore.add(38, "Mariela")
    time.sleep(.1)
    hiscore.add(38, "Carla")
    for idx, score in enumerate(hiscore.list()):
        print("{}: {}".format(idx, score))
