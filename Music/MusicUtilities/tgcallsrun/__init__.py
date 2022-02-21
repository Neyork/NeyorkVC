from os import listdir, mkdir
from pyrogram import Client
from Music import config
from Music.MusicUtilities.tgcallsrun.queues import (clear, get, is_empty, put, task_done)
from Music.MusicUtilities.tgcallsrun.downloader import download
from Music.MusicUtilities.tgcallsrun.convert import convert
from Music.MusicUtilities.tgcallsrun.music import db_mem
from Music.MusicUtilities.tgcallsrun.music import pytgcalls as call_py
smexy = 1
