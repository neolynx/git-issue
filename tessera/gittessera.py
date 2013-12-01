# -*- coding: utf-8 -*-

import os
import stat

from gittle import Gittle
from tessera import Tessera
from colorful import colorful


class GitTessera(object):
    SORTING = {
        "date": lambda t1, t2: t1.mtime < t2.mtime,
        "status": lambda t1, t2: cmp(t1.status.lower(), t2.status.lower()),
        "title": lambda t1, t2: cmp(t1.title.lower(), t2.title.lower()),
        "hash": lambda t1, t2: cmp(t1.tessera_hash.lower(), t2.tessera_hash.lower())
    }

    def __init__(self):
        self.gitdir = "."
        self.git = Gittle(self.gitdir)
        self.tesserae = "%s/.tesserae" % self.gitdir

    def ls(self, args=[]):
        if not os.path.exists(self.tesserae):
            return False

        try:
            idx = args.index("--sort")
            sortfunc = GitTessera.SORTING[args[idx + 1]]
        except ValueError:
            sortfunc = GitTessera.SORTING["date"]
        except IndexError:
            colorful.out.bold_red("Please specify aa sort algorithm. Available: %s" % (", ".join(GitTessera.SORTING.keys())))
            return []
        except KeyError:
            colorful.out.bold_red("No sort algorithm for '%s' available" % args[idx + 1])
            return []

        contents = [self.tesserae + "/" + x for x in os.listdir(self.tesserae) if stat.S_ISDIR(os.lstat(self.tesserae + "/" + x).st_mode)]
        tesserae = []
        for tessera_path in contents:
            tesserae.append(Tessera(tessera_path))
        tesserae = sorted(tesserae, cmp=sortfunc)
        return tesserae
