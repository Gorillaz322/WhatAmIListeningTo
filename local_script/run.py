import os
import sys
import time
import json
import logging
from datetime import datetime, timedelta

import requests
import gi
gi.require_version('Playerctl', '1.0')
from gi.repository import Playerctl, GLib

data_to_send = None

logger = logging.getLogger('spotify-history')
console_logging = logging.StreamHandler()
formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
console_logging.setFormatter(formatter)
logger.addHandler(console_logging)
logger.setLevel(logging.INFO)


def on_track_change(pl):
    global data_to_send

    if data_to_send is not None and \
            datetime.now() - data_to_send['start_time'] > timedelta(seconds=10):
        # don't send data if playback duration less
        # than 10 seconds without excluding time of pause

        # TODO: user identification
        playback_data = dict(
            track_id=data_to_send['track_id'],
            duration=((datetime.now() - data_to_send['start_time']) -
                      data_to_send['paused_time']).seconds,
            start_time=str(data_to_send['start_time']),
            end_time=str(datetime.now())
        )

        api_url = os.environ.get('API_URL')

        if api_url is None:
            logger.error('API_URL is not specified in environment variables. Terminating...')
            sys.exit(0)

        requests.post(api_url, json=json.dumps(playback_data))

        logger.info("Data sent")

    logger.info("Playing song - {song} - {title}".format(
        song=pl.get_artist(),
        title=pl.get_title()
    ))

    data_to_send = dict(
        start_time=datetime.now(),
        paused_time=timedelta(seconds=0),
        track_id=pl.props.metadata['mpris:trackid'].split(':')[2]
    )

pause_start_time = None


def on_pause(pl):
    global pause_start_time
    pause_start_time = datetime.now()
    logger.info("Song paused")


previous_song = None


def on_play(pl):
    global pause_start_time
    global data_to_send

    if pause_start_time is not None:
        data_to_send['paused_time'] += (datetime.now() - pause_start_time)
        logger.info("Continue playback")
        pause_start_time = None

    global previous_song

    if previous_song != pl.get_title():
        previous_song = pl.get_title()
        on_track_change(pl)


# wait for spotify to launch
# if spotify not launched after 1 minute exit script
counter = 0
player = None
while counter < 13:
    player = Playerctl.Player()
    try:
        player.on('play', on_play)
        player.on('pause', on_pause)
        break
    except GLib.Error:
        logger.warning('Spotify was not found | Trying again in 10 seconds')
        counter += 1
        time.sleep(5)

if player is None:
    logger.error("Spotify not found after 1 minute. Terminating...")
    sys.exit(0)

# init startup song
on_track_change(player)

if __name__ == '__main__':
    logger.info('Running main loop')
    try:
        GLib.MainLoop().run()
    except KeyboardInterrupt:
        logger.info("Loop stopped")