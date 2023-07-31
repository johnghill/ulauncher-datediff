from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
import subprocess
import logging

logger = logging.getLogger(__name__)

def days_between(d1, d2):
    cmd = ['bash', '-c', f'd1=$(date -d "{d1}" +%s); d2=$(date -d "{d2}" +%s); echo $(( (d2 - d1) / 86400 ))']
    result = subprocess.check_output(cmd).decode('utf-8').strip()
    return result

class DaysBetweenDatesExtension(Extension):

    def __init__(self):
        super(DaysBetweenDatesExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument()
        if not query:
            return RenderResultListAction([
                ExtensionResultItem(icon='images/calendar-days-solid.svg', name='Enter two comma-separated dates (YYYY-MM-DD)', on_enter=HideWindowAction())
            ])

        date1, date2 = [date.strip() for date in query.split(',')]
        result = days_between(date1, date2)
        return RenderResultListAction([
            ExtensionResultItem(icon='images/calendar-days-solid.svg', name=f'Days between {date1} and {date2}: {result}', on_enter=HideWindowAction())
        ])

if __name__ == '__main__':
    DaysBetweenDatesExtension().run()
