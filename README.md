# equisound
Open source software allows you to check if there is a match between music or sounds.
> Python 3.x module

## Getting started
To get started, the mandatory requirement for audio files, the presence of the .wav format, and two audio files must be converted into one format and one compression algorithm.
For example: wav 16 bit signed
```
python audioanalysis.py {example} {input} {scatter percentage} {accuracy}
```
* Parameters
  * _example and input_ - path to file or name file
  * _scatter percentage_ - float value from 0 to 100
  * _accuracy_ - float value from 0 to 100

__Attention! More accuracy, longer the calculation!__
## dependencies
```
pip install wave
pip install numpy
pip install matplotlib
```

Algorithm is not perfect. Have fun.
