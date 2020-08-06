This function depends on [pyacoustid](https://github.com/beetbox/pyacoustid) and [audioread](https://github.com/beetbox/audioread).

The function now assumes that audio files are copied to appfs so audio files are local to the guest VM.

Function request should be like:

{'audio': audio name}

Function response is like:

{'duration': audio duration, 'fingerprint': fingerprint}
