from urllib.request import urlopen
import pprint

end_page_offset = 6
start_page_offset = 3
tag_ids = [
    '563',  # Seattle
    '561',  # East Side
    "560",  # North
    "547"  # Tacoma & Olympia
]

def find_all_play_in_page(offset):
    url = 'https://nwtheatre.org/calendar/action~agenda/request_format~json/tag_ids~563/'
    if offset != 0:
        url = f'https://nwtheatre.org/calendar/action~agenda/page_offset~{offset}/tag_ids~563/request_format~json/'

    page = urlopen(url)
    html = page.read().decode("utf-8")
    # find plays
    start_index = html.find('<div class="ai1ec-agenda-view">') + len('<div class="ai1ec-agenda-view">')
    end_index = html.find('<div class="ai1ec-pull-left">')
    all_plays = html[start_index:end_index]
    # split each play
    plays = all_plays.split('<span class="ai1ec-event-title">')
    play_names = {}
    for play in plays:
        # find play name - hacky way, fix me
        index = play.find("@")
        if index > 0:
            play_name = play[:index - 1].strip()
            # find producer company - hacky way, fix me
            produce_index = play.find("</span>")
            # find time
            time_start_index = play.find('<div class="ai1ec-event-time">') + len('<div class="ai1ec-event-time">')
            time_tmp = play[time_start_index:]
            time_end_index = time_tmp.find('</div>')
            time = time_tmp[:time_end_index].strip()
            #
            if produce_index > 0:
                produce = play[index:produce_index - 1].strip()
                play_names[play_name] = produce
            elif play_name not in play_names:
                play_names[play_name] = 'unknown'

    return play_names


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    all_plays = {}
    for offset in range(start_page_offset, end_page_offset):
        plays_in_current_offset = find_all_play_in_page(offset)
        all_plays = {**all_plays, **plays_in_current_offset}
    pprint.pprint(all_plays)
    print('finished')
