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


def play_athan(prayer=None):
    cc_api = "catt"
    add_cmd = "add"
    volume = '40' if prayer == 'fajr' else '70'
    audio_files = [DEFAULT_ATHAN_URL]
    audio_files = PRAYER_AUDIO_FILES.get(prayer, PRAYER_AUDIO_FILES['other'])

    catt_cmd([cc_api, "volume", volume])
    catt_cmd([cc_api, "cast", audio_files[0]])
    for audio_file in audio_files[1:]:
        time.sleep(5)
        catt_cmd([cc_api, add_cmd, audio_file])
    time.sleep(120)


def is_athan_time(time, current_time):
    return (current_time.hour == time.hour and current_time.minute + 1 == time.minute)


def get_athan_times(date):
    return adhan(
        day=date,
        location=LOCATION,
        parameters=PARAMETERS,
        timezone_offset=LOCATION_OFFSET,
    )


def get_current_time():
    return datetime.datetime.now(LOCATION_TZ)


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

        if is_athan_time(fajr_time, current_time):
            play_athan("fajr")
        elif is_athan_time(dhuhr_time, current_time):
            play_athan()
        elif is_athan_time(asr_time, current_time):
            play_athan()
        elif is_athan_time(maghrib_time, current_time):
            play_athan("maghrib")
        elif is_athan_time(isha_time, current_time):
            play_athan()

        time.sleep(15)


if __name__ == "__main__":
    main()
