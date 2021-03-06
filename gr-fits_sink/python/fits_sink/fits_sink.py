prfefi#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 Luciano Barosi.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SINK CVS grava n_samples medidas por vez em csv file.
# Tempo nas linhas, frequencias nas colunas.
from astropy.io import fits
from astropy.table import Table
from datetime import datetime
from gnuradio import gr
import numpy as np
import pathlib
import threading
import time

class fits_sink(gr.sync_block):
    """
    This block is controlled by the string variable save_toggle: if save_toggle = "True" (a string, not boolean), the data is written to a new .csv file every new integration time. The minimum integration time for the block to work is 0.1 s.
    """
    def __init__(self, vec_length, samp_rate, freq, prefix, n_samples, mode, csv, fit):
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
        self.csv = csv
        self.fit = fit

    def work(self, input_items, output_items):

        in0_buffer = input_items[0]
        self.START = self.set_TIME()
        for in0 in in0_buffer:
        # <+signal processing here+>
            self.data[self.nint,:] = np.round(in0, decimals=4)
            self.nint = self.nint + 1
            if self.nint == self.n_samples:
                END = self.set_TIME()
                if self.csv:
                    saving = threading.Thread(target=fits_sink.save_csv, args=(self.prefix,  self.mode, self.START, self.data), daemon=True)
                    saving.start()
                if self.fit:
                    saving = threading.Thread(target=fits_sink.save_FITS, args=(self.prefix, self.mode, self.START, END, self.nint, self.frequencies, self.data))
                    saving.start()
                self.data = np.empty((self.n_samples, self.vec_length))
                self.nint = 0
        return len(input_items[0])

    def stop(self):
        END = self.set_TIME()
        if self.csv:
            saving = threading.Thread(target=fits_sink.save_csv, args=(self.prefix,  self.mode, self.START, self.data), daemon=True)
            saving.start()
        if self.fit:
            saving = threading.Thread(target=fits_sink.save_FITS, args=(self.prefix,  self.mode, self.START, END, self.nint, self.frequencies, self.data))
            saving.start()
        self.data = np.empty((self.n_samples, self.vec_length))
        self.nint = 0
        return

    def save_csv(prefix, mode, START, data):
        DATE_START = START.strftime("%Y%m%d")
        TIME_START = START.strftime("%H%M%S")
        filename = prefix + "_" + DATE_START + "_" + TIME_START + "_" + mode + ".csv"
        np.savetxt(filename, data, delimiter = ",")
        return

    def set_TIME(self):
        NOW = datetime.now()
        return NOW

    def save_FITS(prefix, mode, START, END, nint, frequencies, data):
        DATE_START = START.strftime("%Y%m%d")
        TIME_START = START.strftime("%H%M%S")
        DATE_END = END.strftime("%Y%m%d")
        TIME_END =  END.strftime("%H%M%S")
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
        header["BUNIT"] = 'digits'
        header["CTYPE1"] = 'Time [UT]'
        header["CTYPE2"] = 'Frequency [MHz]'
        time_array = np.arange(nint)
        filename = prefix + "_" + DATE_START + "_" + TIME_START + "_" + mode + ".fit"
        primary_HDU = fits.PrimaryHDU(header = header, data = data)
        table_hdu = fits.table_to_hdu(Table([[time_array], [frequencies / 1e6]], names = ("TIME", "FREQUENCY")))
        hdul = fits.HDUList([primary_HDU, table_hdu])
        pathlib.Path(filename).parents[0].mkdir(parents=True, exist_ok=True)
        hdul.writeto(filename)
        return
