#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Spectrometer
# Author: LUCIANO BAROSI
# Copyright: MIT
# GNU Radio version: 3.10.2.0

from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import fits_sink
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import numpy as np
import osmosdr
import time
#import rtlstring



class PFB_Spectrometer(gr.top_block):

    def __init__(self, vec_length=4096, samp_rate=2.048e6,
                 rtl_string=None, name=None, n_samples=4096,
                 n_integration=100, mode="59", gain=50, freq=1040e6, fit=True,
                 csv=False):
        gr.top_block.__init__(self, "Spectrometer", catch_exceptions=True)
        ##################################################
        # Variables
        ##################################################
        self.vec_length = vec_length
        self.sinc_sample_locations = sinc_sample_locations = np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/vec_length)
        self.sinc = sinc = np.sinc(sinc_sample_locations/np.pi)
        self.samp_rate = samp_rate
        self.rtl_string = rtl_string
        self.name = name
        self.n_samples = n_samples
        self.n_integration = n_integration
        self.mode = mode
        self.gain = gain
        self.freq = freq
        self.fit = fit
        self.custom_window = custom_window = sinc*np.hamming(4*vec_length)
        self.csv = csv

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + rtl_string
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(100e6, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.fits_sink_fits_sink_0 = fits_sink.fits_sink( vec_length, samp_rate, freq, name, n_samples, mode, csv, fit)
        self.fft_vxx_0 = fft.fft_vcc(vec_length, True, window.blackmanharris(vec_length), True, 1)
        self.blocks_stream_to_vector_0_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_multiply_const_vxx_0_0_0_0 = blocks.multiply_const_vcc(custom_window[0:vec_length])
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_vcc(custom_window[1*vec_length:2*vec_length])
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc(custom_window[2*vec_length:3*vec_length])
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc(custom_window[-vec_length:])
        self.blocks_integrate_xx_0_0_0 = blocks.integrate_ff(n_integration, vec_length)
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, 3*vec_length)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, 2*vec_length)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_correctiq_0 = blocks.correctiq()
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(vec_length)
        self.blocks_add_xx_0 = blocks.add_vcc(vec_length)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0_0_0, 0))
        self.connect((self.blocks_correctiq_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_correctiq_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.blocks_correctiq_0, 0), (self.blocks_delay_0_0_0, 0))
        self.connect((self.blocks_correctiq_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_stream_to_vector_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0, 0), (self.blocks_stream_to_vector_0_0_0_0, 0))
        self.connect((self.blocks_integrate_xx_0_0_0, 0), (self.fits_sink_fits_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0, 0), (self.blocks_add_xx_0, 3))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_correctiq_0, 0))


    def get_vec_length(self):
        return self.vec_length

    def set_vec_length(self, vec_length):
        self.vec_length = vec_length
        self.set_custom_window(self.sinc*np.hamming(4*self.vec_length))
        self.set_sinc_sample_locations(np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/self.vec_length))
        self.blocks_delay_0.set_dly(self.vec_length)
        self.blocks_delay_0_0.set_dly(2*self.vec_length)
        self.blocks_delay_0_0_0.set_dly(3*self.vec_length)
        self.blocks_multiply_const_vxx_0.set_k(self.custom_window[-self.vec_length:])
        self.blocks_multiply_const_vxx_0_0.set_k(self.custom_window[2*self.vec_length:3*self.vec_length])
        self.blocks_multiply_const_vxx_0_0_0.set_k(self.custom_window[1*self.vec_length:2*self.vec_length])
        self.blocks_multiply_const_vxx_0_0_0_0.set_k(self.custom_window[0:self.vec_length])

    def get_sinc_sample_locations(self):
        return self.sinc_sample_locations

    def set_sinc_sample_locations(self, sinc_sample_locations):
        self.sinc_sample_locations = sinc_sample_locations
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_sinc(self):
        return self.sinc

    def set_sinc(self, sinc):
        self.sinc = sinc
        self.set_custom_window(self.sinc*np.hamming(4*self.vec_length))
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_rtl_string(self):
        return self.rtl_string

    def set_rtl_string(self, rtl_string):
        self.rtl_string = rtl_string

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_n_samples(self):
        return self.n_samples

    def set_n_samples(self, n_samples):
        self.n_samples = n_samples

    def get_n_integration(self):
        return self.n_integration

    def set_n_integration(self, n_integration):
        self.n_integration = n_integration

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_fit(self):
        return self.fit

    def set_fit(self, fit):
        self.fit = fit

    def get_custom_window(self):
        return self.custom_window

    def set_custom_window(self, custom_window):
        self.custom_window = custom_window
        self.blocks_multiply_const_vxx_0.set_k(self.custom_window[-self.vec_length:])
        self.blocks_multiply_const_vxx_0_0.set_k(self.custom_window[2*self.vec_length:3*self.vec_length])
        self.blocks_multiply_const_vxx_0_0_0.set_k(self.custom_window[1*self.vec_length:2*self.vec_length])
        self.blocks_multiply_const_vxx_0_0_0_0.set_k(self.custom_window[0:self.vec_length])

    def get_csv(self):
        return self.csv

    def set_csv(self, csv):
        self.csv = csv




def main(top_block_cls=PFB_Spectrometer, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
