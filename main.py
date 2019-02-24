"""
Ulauncher Extension for opening popular documentation sites.
"""

import json
import logging
import os
# pylint: disable=import-error
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

LOGGING = logging.getLogger(__name__)


class OpenDocsExtension(Extension):
    """ Main Extension Class  """

    def __init__(self):
        """ Initializes the extension """
        super(OpenDocsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

    def get_doc_icon(self, doc_name):
        """ Returns the documentation icon with fallback for the default one if does not exists """
        icon = 'images/docs/%s.png' % doc_name
        icon_abs_path = os.path.join(os.path.dirname(__file__), icon)
        if os.path.isfile(icon_abs_path):
            return icon

        return 'images/icon.png'


class KeywordQueryEventListener(EventListener):
    """ Listener that handles the user input """

    # pylint: disable=unused-argument,no-self-use
    def on_event(self, event, extension):
        """ Handles the event """

        with open('data/docs.json') as f_data:
            docs = json.load(f_data)

        query = event.get_argument() or ""

        if query:
            docs = [x for x in docs if query.lower() in x['name'].lower()]

        docs = sorted(docs, key=lambda k: k['name'])
        items = []

        for doc in docs[:8]:

            icon = extension.get_doc_icon(doc['key'])

            items.append(ExtensionResultItem(
                icon=icon,
                name=doc['name'],
                on_enter=OpenUrlAction(doc['url']),
                on_alt_enter=CopyToClipboardAction(doc['url'])
            ))

        return RenderResultListAction(items)


if __name__ == '__main__':
    OpenDocsExtension().run()
