import subprocess
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.client.EventListener import EventListener

def days_between(d1, d2):
    cmd = ['bash', '-c', f'd1=$(date -d "{d1}" +%s); d2=$(date -d "{d2}" +%s); echo $(( (d2 - d1) / 86400 ))']
    result = subprocess.check_output(cmd).decode('utf-8').strip()
    return result

class DaysBetweenDatesExtension(EventListener):

    def on_event(self, event, extension):
        if isinstance(event, KeywordQueryEvent):
            query = event.get_argument()
            if not query:
                return RenderResultListAction([
                    ExtensionResultItem(icon='images/calendar-days-solid.svg', name='Enter two dates separated by a comma', on_enter=None)
                ])

            date1, date2 = [date.strip() for date in query.split(',')]
            result = days_between(date1, date2)
            return RenderResultListAction([
                ExtensionResultItem(icon='images/calendar-days-solid.svg', name=f'Days between {date1} and {date2}: {result}', on_enter=None)
            ])

if __name__ == '__main__':
    DaysBetweenDatesExtension().run()
