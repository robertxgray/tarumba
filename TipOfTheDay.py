# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         TipOfTheDay.py
# Purpose:      Random tip of the day generator.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: TipOfTheDay.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals

import random

messages = (
_(u'You can help Tarumba to be available in more languajes. Please contact with us.'),
_(u'If you have multivolume zip files, you can join them by selecting Tools->Join multivolume zip'),
_(u'Open your files faster with right click on the file system.'),
_(u'Corrupted files? Tarumba will help you to test and fix them in an easy way.'),
_(u'Did you know that the generic volumes created with Tarumba can also be joined with the cat command?'),
_(u'You can change the default compression level, but do it wisely. The most powerfull levels will also be slower.'),
_(u'Remember that Tarumba\'s favourite compression formats are tar.bz2 and tar.gz. The first has an higher rate and the second is faster.'),
_(u'You can use drag an drop between Tarumba and your favourite file manager, as well as many other programs.'),
_(u'Tarumba\'s tools to encrypt/decrypt and split/join, can be used with any file, not just compressed ones.'),
_(u'Did you know you can use Tarumba to rename the contents of a compressed file? If you rename a folder, the path for the files inside it will be updated as well.'),
_(u'Are your files top secret? Tarumba will encrypt then. Tarumba\'s compression is compatible with standart security tools like openssl.'),
_(u'If you need a fast preview of a file just double click on it. To select a program in particular use the option "Open with...".'),
_(u'Do you want to use Tarumba but an X server is not available? No problem! type "tarumba -h" for more details.'),
_(u'You can easily integrate Tarumba with your shell scripts or with other programs. Type "tarumba -h" for more details.')
)

def message():
    "Returns a random tip of the day"
    global messages
    baseMessage = _(u'Welcome to Tarumba %s') % Globals.VERSION + '\n'
    numMessages = len(messages)
    randomMess = random.randint(0,numMessages-1)
    return baseMessage + messages[randomMess]
