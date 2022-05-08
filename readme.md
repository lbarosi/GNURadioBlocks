# GNURADIO FITS_SINK

Bloco GNURadio para gravação em formatos FITS e CSV.


```
git clone endereço
cd GNURadioBlocks/gr_fits_sink
mkdir build
cd build
cmake ../
make
sudo make install
sudo ldconfig
```

Se você usa GNURADIO em um ambiente conda ou em endereço customizado em sua máquina local você deve informar o `cmake` sobre isso, por exemplo `cmake -DCMAKE_INSTALL_PREFIX=$CONDA_PREFFIX ../ `.

Os parâmetros do módulo são:

- `vec_length`: tamanho do string de dados lido por vez.
- `samp_rate`: frequência de amostragem do sinal.
- `freq`: frequência central
- `prefix`: string que prefixa o nome dos arquivos.
- `n_samples`: número de amostras para cada arquivo.
- `mode`: string sufixo do nome do arquivo salvo
- `csv`: booleano para salvar ou não em formato CVS
- `fit`: booleano para salvar ou não em formato FITS

## Linha de comando

O programa `grc_flowgraphs/PFB_Spectrometer.py` é um flow gnuradio que usa o bloco, pode ser utulizado como exemplo para aprender suas funcionalidades.

O programa `grc_flowgraphs/GNUController.py` é um script em python que controla um flow do GNURadio, assumindo que existe um dispositivo RTLSDR escutando os comandos.

```bash
$ ./GNUController.py  --rtlsdr "rtl=0" --name "RTLSDR_teste" \
+ --mode "01" --vec_length 4096 --samp_rate 2048000 --gain 50 \
--freq 1420000000 --n_integration 100 --n_samples 1000 \
--duration 300 --csvflag --fitflag
```
