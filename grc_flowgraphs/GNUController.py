# -*- coding: utf-8 -*-
"""
Controlador de flowgraph do GNURADIO baseado no módulo importado, com adição de gerenciamento de linha de comando com argparse e tempo de execução.

PACKAGE: Radiotelecope
AUTHOR: Luciano Barosi
DATE: 24.04.2022
"""
import argparse
import signal
import time
from PFB_Spectrometer import PFB_Spectrometer as PFB


def main(top_block_cls=PFB, options=None):
    parser = argparse.ArgumentParser(description="GNURADIO flowgraph controller."
        )
    parser.add_argument("--rtlsdr", type=str, dest="rtl_string", help="RTL command string", default="rtl=0")
    parser.add_argument("--name", type=str, dest="name", help="Caminho e nome do arquivo.", default="_")
    parser.add_argument("--mode", type=str, dest="mode", help="Modo de obsrvação.", default="59")
    parser.add_argument("--vec_length", type=int, dest="vec_length", help="tamanho FFT", default=4096)
    parser.add_argument("--samp_rate", type=int, dest="samp_rate", help="Frequência de amostragem", default=2048e6)
    parser.add_argument("--gain", type=int, dest="gain", help="Ganho.", default=50)
    parser.add_argument("--freq", type=int, dest="freq", help="Frequência central", default=1420e6)
    parser.add_argument("--n_integration", type=int, dest="n_integration", help="Número de Integrações", default=100)
    parser.add_argument("--n_samples", type=int, dest="n_samples", help="Número de amostras por arquivo", default=100)
    parser.add_argument("--csv", help="grava formato csv", dest="csv", action="store_true", default=False)
    parser.add_argument("--FIT", help="grava formato FITs", dest="fit", action="store_true", default=False)
    parser.add_argument("--duration", type=str, dest="duration", help="Duração da medição.", default=60)


    args = parser.parse_args()
    PFB.rtl_string = args.rtl_string
    PFB.name = args.name
    PFB.mode = args.mode
    PFB.vec_length = args.vec_length
    PFB.samp_rate = args.samp_rate
    PFB.gain = args.gain
    PFB.freq = args.freq
    PFB.n_integration = args.n_integration
    PFB.n_samples = args.n_samples
    PFB.csv = args.csv
    PFB.fit = args.fit

    duration = args.duration

    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    time.sleep(duration)
    tb.stop()
    tb.wait()

if __name__ == '__main__':
    main()
