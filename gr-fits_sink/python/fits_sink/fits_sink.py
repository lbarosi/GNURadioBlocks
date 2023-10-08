#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 Luciano Barosi.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SINK CVS grava n_samples medidas por vez em csv file.
# Tempo nas linhas, frequencias nas colunas.
from astropy.time import Time
from astropy.io import fits
from astropy.table import Table
from datetime import datetime
from gnuradio import gr
import logging
import numpy as np
import pathlib
import threading
import time
import pytz

# Preparando log ----------------------
logger = logging.getLogger(__name__)
# -------------------------------------

# -------------------------------------
class fits_sink(gr.sync_block):
    """
    Class fits_sink.

    This block is controlled by the string variable save_toggle: if save_toggle = "True" (a string, not boolean), the data is written to a new .csv file every new integration time. The minimum integration time for the block to work is 0.1 s.
    """

    def __init__(self, vec_length, samp_rate, freq, prefix, n_samples, mode, fit, timezone=pytz.timezone('America/Recife'), lat=-7.2117, lon=-35.9081, heigth=553, alt=84, az=0):
        gr.sync_block.__init__(self,
            name="fits_sink",
            in_sig=[(np.float32, int(vec_length))],
            out_sig=None)

        self.vec_length = int(vec_length)
        self.samp_rate = samp_rate
        self.freq = freq
        self.prefix = prefix
        self.frequencies = np.linspace(freq - samp_rate/2, freq + samp_rate/2, int(vec_length))
        self.n_samples = n_samples
        self.data = np.empty((self.n_samples, self.vec_length))
        self.nint = 0
        self.mode = mode
        self.fit = fit
        self.timevector = np.empty(self.n_samples)
        self.START = self.set_TIME()
        self.time_start = time.perf_counter()
        self.timezone = timezone
        self.lat = lat
        self.lon = lon
        self.heigth = heigth
        self.alt = alt
        self.az = az


    def work(self, input_items, output_items):

        in0_buffer = input_items[0]

        for in0 in in0_buffer:
        # <+signal processing here+>
            self.data[self.nint,:] = np.round(in0, decimals=4)
            self.timevector[self.nint] = time.perf_counter_ns() - self.time_start
            self.nint = self.nint + 1
            if self.nint == self.n_samples:
                END = self.set_TIME()
                if self.fit is True:
                    saving = threading.Thread(target=fits_sink.save_FITS, args=(self.prefix, self.mode, self.START, END, self.nint, self.frequencies, self.data, self.timevector))
                    saving.start()
                self.data = np.empty((self.n_samples, self.vec_length))
                self.timevector = np.empty(self.n_samples)
                self.nint = 0
                self.time_start = time.perf_counter_ns()
                self.START = self.set_TIME()
        return len(input_items[0])

    def stop(self):
        END = self.set_TIME()
        if self.fit is True:
            saving = threading.Thread(target=fits_sink.save_FITS, args=(self.prefix,  self.mode, self.START, END, self.nint, self.frequencies, self.data, self.timevector))
            saving.start()
        self.data = np.empty((self.n_samples, self.vec_length))
        self.nint = 0
        return

    def set_TIME(self):
        NOW = Time.now()
        return NOW

    def save_FITS(prefix, mode, START, END, nint, frequencies, data, timevector):
        START_ = START
        END_ = END
        START = timezone.localize(START.to_datetime())
        END = timezone.localize(END.to_datetime())
        DATE_START = START.strftime("%Y%m%d")
        TIME_START = START.strftime("%H%M%S.%f")
        DATE_END = END.strftime("%Y%m%d")
        TIME_END =  END.strftime("%H%M%S.%f")
        time_size = nint
        freq_size = frequencies.size
        header = fits.Header()
        header["SIMPLE"] = "T"
        header["BITPIX"] = "16"
        header["NAXIS"] = 2
        header["NAXIS1"] = time_size
        header["NAXIS2"] = freq_size
        header["EXTEND"] = "T"
        header["COMMENT"] = "FITS (Flexible Image Transport System) format defined in Astronomy and"
        header["COMMENT"] = "Astrophysics Supplement Series v44#p363, v44#p371, v73#p359, v73#p365."
        header["COMMENT"] = "Contact the NASA Science Office of Standards and Technology for the   "
        header["COMMENT"] = "FITS Definition document #100 and other FITS information.             "
        header["DATE"] = DATE_START
        header["CONTENT"] = "Radio flux density - " + str(prefix)
        header["ORIGIN"] = "PB"
        header["TELESCOP"] = str(prefix)
        header["INSTRUME"] = str(prefix)
        header["DATE-OBS"] = DATE_START
        header["TIME-OBS"] = TIME_START
        header["DATE-END"] = DATE_END
        header["TIME-END"] = TIME_END
        header["BZERO"] = 0.
        header["BSCALE"] = 1.
        header["BUNIT"] = 'dB (ADU)'
        header["CTYPE1"] = 'Time [JD]'
        header["CTYPE2"] = 'Frequency [MHz]'
        header["MINFREQ"] = frequencies.min()
        header["MAXFREQ"] = frequencies.max()
        header["JULSTART"] = START_.tai.jd
        header["JULEND"] = END_.tai.jd
        header["OBS_LAT"] = self.lat
        header["OBS_LON"] = self.lon
        header["OBS_ALT"] = self.heigth
        header["OBS_Alt"] = self.Alt
        header["OBS_Az"] = self.Az
        DATE_START_name = START.strftime("%Y%m%d")
        TIME_START_name = START.strftime("%H%M%S")
        filename = prefix + "_" + str(DATE_START_name) + "_" + str(TIME_START_name) + "_" + str(mode) + ".fit"
        primary_HDU = fits.PrimaryHDU(header = header, data = data[0:nint, :])
        time_array = (START_ + (timevector[0:nint]) * (1e-9 u.s)).tai.jd
        table_hdu = fits.table_to_hdu(Table([[time_array], [frequencies / 1e6]], names = ("TIME", "FREQUENCY")))
        hdul = fits.HDUList([primary_HDU, table_hdu])
        pathlib.Path(filename).parents[0].mkdir(parents=True, exist_ok=True)
        hdul.writeto(filename)
        print("Arquivo {} salvo com sucesso.".format(filename))
        return
