import datetime
import time
from adhan import adhan
from adhan.methods import ISNA, ASR_STANDARD
import pytz
import subprocess
from retry import retry

# Update the following constants with the user's location and preferred audio files for accurate prayer times and personalized adhan and tadhkir audio.
DEFAULT_ATHAN_URL = r'https://www.youtube.com/watch?v=Fmp8f2ugZm4'
FAJR_ATHAN_URL = r'https://www.youtube.com/watch?v=iaWZ_3D6vOQ'
MORNING_TADHKIR_URL = r'https://www.youtube.com/watch?v=UdX3NPy4RM8'
SURAT_AL_BAQARAH_URL = r'https://www.youtube.com/watch?v=QhbORaXfUy0'
EVENING_TADHKIR_URL = r'https://www.youtube.com/watch?v=TGtdZmxsM5Q'
LOCATION = (30.266666, -97.73333)
LOCATION_TZ = pytz.timezone('US/Central')
LOCATION_OFFSET = -6
PARAMETERS = {**ISNA, **ASR_STANDARD}
PRAYER_AUDIO_FILES = {
    'fajr': [FAJR_ATHAN_URL, MORNING_TADHKIR_URL, SURAT_AL_BAQARAH_URL],
    'maghrib': [DEFAULT_ATHAN_URL, EVENING_TADHKIR_URL],
    'other': [DEFAULT_ATHAN_URL]
}


@retry(exceptions=Exception, tries=3, delay=2)
def catt_cmd(cmd):
    subprocess.run(cmd)


def get_audio_files(prayer):
    return DEFAULT_ATHAN_URL if not prayer else PRAYER_AUDIO_FILES[prayer]


def play_athan(prayer=None):
    cc_api = "catt"
    add_cmd = "add"
    volume = '40' if prayer == 'fajr' else '70'
    audio_files = get_audio_files(prayer)
    catt_cmd([cc_api, "stop"])
    catt_cmd([cc_api, "clear"])
    catt_cmd([cc_api, "volume", volume])
    catt_cmd([cc_api, "cast", audio_files[0]])
    for audio_file in audio_files[1:]:
        time.sleep(5)
        catt_cmd([cc_api, add_cmd, audio_file])
    time.sleep(120)


def is_athan_time(prayer_time, current_time):
    return (current_time.hour == prayer_time.hour and current_time.minute + 1 == prayer_time.minute)


def get_athan_times(date):
    return adhan(
        day=date,
        location=LOCATION,
        parameters=PARAMETERS,
        timezone_offset=LOCATION_OFFSET,
    )


def get_current_time():
    return datetime.datetime.now(LOCATION_TZ)


def check_athan_time(prayer, prayer_time, current_time):
    formatted_prayer_time = prayer_time.strftime('%I:%M %p')
    formatted_current_time = current_time.strftime('%I:%M %p')
    if is_athan_time(prayer_time, current_time):
        print(
            f'It is Athan time for {prayer.capitalize()} at {formatted_prayer_time}')
        print(f'{prayer.capitalize()} time: {formatted_prayer_time}')
        print(f'Current time: {formatted_current_time}')
        print('--------------------------------------------------------------------')
        play_athan(prayer) if prayer in {'fajr', 'maghrib'} else play_athan()


def main():
    while True:
        current_date = datetime.date.today()
        athan_times = get_athan_times(current_date)
        current_time = get_current_time()

        fajr_time = athan_times['fajr']
        dhuhr_time = athan_times['zuhr']
        asr_time = athan_times['asr']
        maghrib_time = athan_times['maghrib']
        isha_time = athan_times['isha']

        check_athan_time("fajr", fajr_time, current_time)
        check_athan_time("dhuhr", dhuhr_time, current_time)
        check_athan_time("asr", asr_time, current_time)
        check_athan_time("maghrib", maghrib_time, current_time)
        check_athan_time("isha", isha_time, current_time)
        time.sleep(15)


if __name__ == "__main__":
    main()
