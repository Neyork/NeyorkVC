from os import listdir, mkdir
from pyrogram import Client
from Music import config
from Music.MusicUtilities.tgcallsrun.queues import (clear, get, is_empty, put, task_done)
from Music.MusicUtilities.tgcallsrun.downloader import download
from Music.MusicUtilities.tgcallsrun.convert import convert
from Music.Inline import (audio_markup, audio_timer_markup_start,
                          primary_markup, secondary_markup2, timer_markup)
from Music.MusicUtilities.tgcallsrun.music import smexy as ASS_ACC
smexy = 1
