# Sonido estéreo y ficheros WAVE

## Mark Bonete Ventura

## El formato WAVE

El formato WAVE es uno de los más extendidos para el almacenamiento y transmisión
de señales de audio. En el fondo, se trata de un tipo particular de fichero
[RIFF](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format) (*Resource
Interchange File Format*), utilizado no sólo para señales de audio sino también para señales de
otros tipos, como las imágenes estáticas o en movimiento, o secuencias MIDI (aunque, en el caso
del MIDI, con pequeñas diferencias que los hacen incompatibles).

La base de los ficheros RIFF es el uso de *cachos* (*chunks*, en inglés). Cada cacho,
o subcacho, está encabezado por una cadena de cuatro caracteres ASCII, que indica el tipo del cacho,
seguido por un entero sin signo de cuatro bytes, que indica el tamaño en bytes de lo que queda de
cacho sin contar la cadena inicial y el propio tamaño. A continuación, y en función del tipo de
cacho, se colocan los datos que lo forman.

Todo fichero RIFF incluye un primer cacho que lo identifica como tal y que empieza por la cadena
`'RIFF'`. A continuación, después del tamaño del cacho y en otra cadena de cuatro caracteres,
se indica el tipo concreto de información que contiene el fichero. En el caso concreto de los
ficheros de audio WAVE, esta cadena es igual a `'WAVE'`, y el cacho debe contener dos
*subcachos*: el primero, de nombre `'fmt '`, proporciona la información de cómo está
codificada la señal. Por ejemplo, si es PCM lineal, ADPCM, etc., o si es monofónica o estéreo. El
segundo subcacho, de nombre `'data'`, incluye las muestras de la señal.

Dispone de una descripción detallada del formato WAVE en la página
[WAVE PCM soundfile format](http://soundfile.sapp.org/doc/WaveFormat/) de Soundfile.

## Audio estéreo

La mayor parte de los animales, incluidos los del género *homo sapiens sapiens* sanos y completos,
están dotados de dos órganos que actúan como transductores acústico-sensoriales (es decir, tienen dos
*oídos*). Esta duplicidad orgánica permite al bicho, entre otras cosas, determinar la dirección de
origen del sonido. En el caso de la señal de música, además, la duplicidad proporciona una sensación
de *amplitud espacial*, de realismo y de confort acústico.

En un principio, los equipos de reproducción de audio no tenían en cuenta estos efectos y sólo permitían
almacenar y reproducir una única señal para los dos oídos. Es el llamado *sonido monofónico* o
*monoaural*. Una alternativa al sonido monofónico es el *estereofónico* o, simplemente, *estéreo*. En
él, se usan dos señales independientes, destinadas a ser reproducidas a ambos lados del oyente: los
llamados *canal izquierdo* (**L**) y *derecho* (**R**).

Aunque los primeros experimentos con sonido estereofónico datan de finales del siglo XIX, los primeros
equipos y grabaciones de este tipo no se popularizaron hasta los años 1950 y 1960. En aquel tiempo, la
gestión de los dos canales era muy rudimentaria. Por ejemplo, los instrumentos se repartían entre los
dos canales, con unos sonando exclusivamente a la izquierda y el resto a la derecha. Es el caso de las
primeras grabaciones en estéreo de los Beatles: las versiones en alemán de los singles *She loves you*
y *I want to hold your hand*. Así, en esta última (de la que dispone de un fichero en Atenea con sus
primeros treinta segundos, [Komm, gib mir deine Hand](wav/komm.wav)), la mayor parte de los instrumentos
suenan por el canal derecho, mientras que las voces y las características palmas lo hacen por el izquierdo.

Un problema habitual en los primeros años del sonido estereofónico, y aún vigente hoy en día, es que no
todos los equipos son capaces de reproducir los dos canales por separado. La solución comúnmente
adoptada consiste en no almacenar cada canal por separado, sino en la forma semisuma, $(L+R)/2$, y
semidiferencia, $(L-R)/2$, y de tal modo que los equipos monofónicos sólo accedan a la primera de ellas.
De este modo, estos equipos pueden reproducir una señal completa, formada por la suma de los dos
canales, y los estereofónicos pueden reconstruir los dos canales estéreo.

Por ejemplo, en la radio FM estéreo, la señal, de ancho de banda 15 kHz, se transmite del modo siguiente:

- En banda base, $0\le f\le 15$ kHz, se transmite la suma de los dos canales, $L+R$. Esta es la señal
  que son capaces de reproducir los equipos monofónicos.

- La señal diferencia, $L-R$, se transmite modulada en amplitud con una frecuencia de portadora
  $f_m = 38$ kHz.

  - Por tanto, ocupa la banda $23 \mathrm{kHz}\le f\le 53 \mathrm{kHz}$, que sólo es accedida por los
    equipos estéreo, y, en el caso de colarse en un reproductor monofónico, ocupa la banda no audible.

- También se emite una sinusoide de $19 \mathrm{kHz}$, denominada *señal piloto*, que se usa para
  demodular síncronamente la señal diferencia.

- Finalmente, la señal de audio estéreo puede acompañarse de otras señales de señalización y servicio en
  frecuencias entre $55.35 \mathrm{kHz}$ y $94 \mathrm{kHz}$.

En los discos fonográficos, la semisuma de las señales está grabada del mismo modo que se haría en una
grabación monofónica, es decir, en la profundidad del surco; mientras que la semidiferencia se graba en el
desplazamiento a izquierda y derecha de la aguja. El resultado es que un reproductor mono, que sólo atiende
a la profundidad del surco, reproduce casi correctamente la señal monofónica, mientras que un reproductor
estéreo es capaz de separar los dos canales. Es posible que algo de la información de la semisuma se cuele
en el reproductor mono, pero, como su amplitud es muy pequeña, se manifestará como un ruido muy débil,
apenas perceptible.

En general, todos estos sistemas se basan en garantizar que el reproductor mono recibe correctamente la
semisuma de canales y que, si algo de la semidiferencia se cuela en la reproducción, sea en forma de un
ruido inaudible.

## Tareas a realizar

Escriba el fichero `estereo.py` que incluirá las funciones que permitirán el manejo de los canales de una
señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos.

### Manejo de los canales de una señal estéreo

En un fichero WAVE estéreo con señales de 16 bits, cada muestra de cada canal se codifica con un entero de
dos bytes. La señal se almacena en el *cacho* `'data'` alternando, para cada muestra de $x[n]$, el valor
del canal izquierdo y el derecho:

<img src="img/est%C3%A9reo.png" width="380px">

#### Función `estereo2mono(ficEste, ficMono, canal=2)`

La función lee el fichero `ficEste`, que debe contener una señal estéreo, y escribe el fichero `ficMono`,
con una señal monofónica. El tipo concreto de señal que se almacenará en `ficMono` depende del argumento
`canal`:

- `canal=0`: Se almacena el canal izquierdo $L$.
- `canal=1`: Se almacena el canal derecho $R$.
- `canal=2`: Se almacena la semisuma $(L+R)/2$. Ha de ser la opción por defecto.
- `canal=3`: Se almacena la semidiferencia $(L-R)/2$.

#### Función `mono2estereo(ficIzq, ficDer, ficEste)`

Lee los ficheros `ficIzq` y `ficDer`, que contienen las señales monofónicas correspondientes a los canales
izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
`ficEste`.

### Codificación estéreo usando los bits menos significativos

En la línea de los sistemas usados para codificar la información estéreo en señales de radio FM o en los
surcos de los discos fonográficos, podemos usar enteros de 32 bits para almacenar los dos canales de 16 bits:

- En los 16 bits más significativos se almacena la semisuma de los dos canales.

- En los 16 bits menos significativos se almacena la semidiferencia.

Los sistemas monofónicos sólo son capaces de manejar la señal de 32 bits. Esta señal es prácticamente
idéntica a la señal semisuma, ya que la semisuma ocupa los 16 bits más significativos. La señal
semidiferencia aparece como un ruido añadido a la señal, pero, como su amplitud es $2^{16}$ veces más
pequeña, será prácticamente inaudible (la relación señal a ruido es del orden de 90 dB).

Los sistemas estéreo son capaces de aislar las dos partes de la señal y, con ellas, reconstruir los dos
canales izquierdo y derecho.

<img src="img/est%C3%A9reo_cod.png" width="510px">

#### Función `codEstereo(ficEste, ficCod)`

Lee el fichero `ficEste`, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
monofónicos como por sistemas estéreo preparados para ello.

#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero `ficCod` con una señal monofónica de 32 bits en la que los 16 bits más significativos
contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
semidiferencia, y escribe el fichero `ficEste` con los dos canales por separado en el formato de los
ficheros WAVE estéreo.

### Entrega

#### Fichero `estereo.py`

- El fichero debe incluir una cadena de documentación que incluirá el nombre del alumno y una descripción
  del contenido del fichero.

- Es muy recomendable escribir, además, sendas funciones que *empaqueten* y *desempaqueten* las cabeceras
  de los ficheros WAVE a partir de los datos contenidos en ellas.

- Aparte de `struct`, no se puede importar o usar ningún módulo externo.

- Se deben evitar los bucles. Se valorará el uso, cuando sea necesario, de *comprensiones*.

- Los ficheros se deben abrir y cerrar usando gestores de contexto.

- Las funciones deberán comprobar que los ficheros de entrada tienen el formato correcto y, en caso
  contrario, elevar la excepción correspondiente.

- Los ficheros resultantes deben ser reproducibles correctamente usando cualquier reproductor estándar;
  por ejemplo, el Windows Media Player o similar. Es probable, muy probable, que tenga que modificar los
  datos de las cabeceras de los ficheros para conseguirlo.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el uso de los estándares
  marcados por PEP-ocho.

#### Comprobación del funcionamiento

Es responsabilidad del alumno comprobar que las distintas funciones realizan su cometido de manera correcta.
Para ello, se recomienda usar la canción [Komm, gib mir deine Hand](wav/komm.wav), suminstrada al efecto.
De todos modos, recuerde que, aunque sea en alemán, se trata de los Beatles, así que procure no destrozar
innecesariamente la canción.

#### Código desarrollado

Inserte a continuación el código de los métodos desarrollados en esta tarea, usando los comandos necesarios
para que se realice el realce sintáctico en Python del mismo (no vale insertar una imagen o una captura de
pantalla, debe hacerse en formato *markdown*).

### Código de empaquetado y desempaquetado de cabeceras

##### Código de `read_wave()`
```p
def read_wave(filename: str) -> dict | dict:
    """
    Reads a WAVE file and returns two dictionaries with the file sub-chunks.

    Args:
        filename: name of the file to read
    Returns:
        - Header dictionary with the following keys:
            - ChunkID
            - ChunkSize
            - Format
            - Subchunk1ID
            - SubChunk1Size
            - AudioFormat
            - NumChannels
            - SampleRate
            - ByteRate
            - BlockAlign
            - BitsPerSample
        - Data dictionary with the following keys
            - SubChunk2ID
            - SubChunk2Size
            - data
    """
    header = {}
    data = {}
    with open(filename , "rb") as f:
        # RIFF chunk descriptor
        format = "<4sI4s"
        buffer = f.read(st.calcsize(format))
        header["ChunkID"], header["ChunkSize"], header["Format"] = st.unpack(format, buffer)
        
        position = st.calcsize(format)
        f.seek(position)

        # Check file format    
        if header["Format"] != b"WAVE":
            raise ValueError(f"File '{filename}' is not a WAVE file")

        # fmt subchunk
        format = "<4sI2H2I2H"
        buffer = f.read(st.calcsize(format))
        (
            header["SubChunk1ID"],
            header["SubChunk1Size"],
            header["AudioFormat"],
            header["NumChannels"],
            header["SampleRate"],
            header["ByteRate"],
            header["BlockAlign"],
            header["BitsPerSample"]
        ) = st.unpack(format, buffer)
        
        position += st.calcsize(format)
        f.seek(position)

        # data subchunk
        format = "<4sI"
        buffer = f.read(st.calcsize(format))
        data["SubChunk2ID"], data["SubChunk2Size"] = st.unpack(format, buffer)
        
        position += st.calcsize(format)
        f.seek(position)

        # data
        if header["BitsPerSample"] == 8:
            format = "<b"
        elif header["BitsPerSample"] == 16:
            format = "<h"
        elif header["BitsPerSample"] == 32:
            format = "<i"
        else:
            raise ValueError(f"Bits per sample must be 8, 16 or 32. File '{filename}' has {header['BitsPerSample']} instead.")
        
        buffer = f.read()
        data["data"] = [int(sample[0]) for sample in st.iter_unpack(format, buffer)]

    return header, data
```

##### Código de `write_wave()`
```p
def write_wave(filename: str, header: dict, data: dict):
    """
    Writes a WAVE file with the given header and data dictionaries.
    """
    if header["Format"] != b"WAVE":
        raise ValueError(f"File {filename} is not a WAVE file")
        
    with open(filename, "wb") as f:
        # RIFF chunk descriptor
        format = "<4sI4s"
        buffer = st.pack(format, header["ChunkID"], header["ChunkSize"], header["Format"])
        f.write(buffer)

        # fmt subchunk
        format = "<4sI2H2I2H"
        buffer = st.pack(
            format,
            header["SubChunk1ID"],
            header["SubChunk1Size"],
            header["AudioFormat"],
            header["NumChannels"],
            header["SampleRate"],
            header["ByteRate"],
            header["BlockAlign"],
            header["BitsPerSample"]
        )
        f.write(buffer)

        # data subchunk
        format = "<4sI"
        buffer = st.pack(format, data["SubChunk2ID"], data["SubChunk2Size"])
        f.write(buffer)

        # data
        if header["BitsPerSample"] == 8:
            format = f"<{len(data['data'])}b"
        elif header["BitsPerSample"] == 16:
            format = f"<{len(data['data'])}h"
        elif header["BitsPerSample"] == 32:
            format = f"<{len(data['data'])}i"
        else:
            raise ValueError(f"Bits per sample must be 8, 16 or 32. File '{filename}' has {header['BitsPerSample']} instead.")
        
        buffer = st.pack(format, *data["data"])
        f.write(buffer)
```

##### Código de `estereo2mono()`
```p
def estereo2mono(ficEste, ficMono, canal=2):
    """
    Converts an estereo audio file into a mono audio file.

    Args:
        ficEste: estereo audio file
        ficMono: mono audio file
        canal: channel to convert
            - 0: left channel
            - 1: right channel
            - 2: mean of both channels
            - 3: difference of both channels
    
    Raises:
        ValueError: if the file is not estereo or the channel is not between 0 and 3
    """
    header, data = read_wave(ficEste)
    if header["NumChannels"] != 2:
        raise ValueError(f"File '{ficEste}' is not an estereo file")
    
    # Mono header
    header["NumChannels"] = 1
    header["ByteRate"] = header["SampleRate"] * header["NumChannels"] * header["BitsPerSample"]//8
    header["BlockAlign"] = header["NumChannels"] * header["BitsPerSample"]//8

    # Define data to be saved
    left_channel, right_channel = data["data"][::2], data["data"][1::2]
    mono_data = {
        "SubChunk2ID": b"data",
        "SubChunk2Size": 0,
        "data": []
    }

    if canal == 0:
        mono_data["data"] = left_channel
    elif canal == 1:
        mono_data["data"] = right_channel
    elif canal == 2:
        mono_data["data"] = [(left_sample + right_sample) // 2 for left_sample, right_sample in zip(left_channel, right_channel)]
    elif canal == 3:
        mono_data["data"] = [(left_sample - right_sample) // 2 for left_sample, right_sample in zip(left_channel, right_channel)]
    else:
        raise ValueError(f"Channel must be a number between 0 and 3, both included.")
    
    mono_data["SubChunk2Size"] = len(mono_data["data"]) * header["NumChannels"] * header["BitsPerSample"]//8

    write_wave(ficMono, header, mono_data)
```

##### Código de `mono2estereo()`
```p
def mono2estereo(ficIzq: str, ficDer: str, ficEste: str):
   """
    Converts two mono audio files into an estereo audio file.

    Args:
        ficIzq: left channel audio file
        ficDer: right channel audio file
        ficEste: estereo audio file
    Raises:
        ValueError: if the files are not mono
    """
    left_header, left_data = read_wave(ficIzq)    
    if left_header["NumChannels"] != 1:
        raise ValueError(f"File '{ficIzq}' is not a mono file")
    
    right_header, right_data = read_wave(ficDer)
    if right_header["NumChannels"] != 1:
        raise ValueError(f"File '{ficDer}' is not a mono file")
    
    # Estereo header
    header = left_header
    header["NumChannels"] = 2
    header["ByteRate"] = header["SampleRate"] * header["NumChannels"] * header["BitsPerSample"]//8
    header["BlockAlign"] = header["NumChannels"] * header["BitsPerSample"]//8

    # Define data to be saved
    data = {
        "SubChunk2ID": b"data",
        "SubChunk2Size": 0,
        "data": []
    }
    data["data"] = left_data["data"] + right_data["data"]
    data["data"][::2] = left_data["data"]
    data["data"][1::2] = right_data["data"]

    data["SubChunk2Size"] = len(left_data["data"]) * header["NumChannels"] * header["BitsPerSample"]//8

    write_wave(ficEste, header, data)
```

##### Código de `codEstereo()`
```p
def codEstereo(ficEste: str, ficCod: str):
    """
    Codifies an estereo audio file into a mono audio file. The codification is done by:
    - Calculating the semi-sum and semi-difference of the left and right channels.
    - Converting the semi-sum and semi-difference into 16-bit samples.
    - Adding the semi-sum and semi-difference samples to obtain the codified sample of 32 bits.

    Args:
        ficEste: estereo audio file
        ficCod: codified audio file
    Raises:
        ValueError: if the file is not estereo
    """
    header, data = read_wave(ficEste)
    if header["NumChannels"] != 2:
        raise ValueError(f"File '{ficEste}' is not an estereo file")
    
    # Codified file header
    header["NumChannels"] = 1
    header["BitsPerSample"] = 32
    header["ByteRate"] = header["SampleRate"] * header["NumChannels"] * header["BitsPerSample"]//8
    header["BlockAlign"] = header["NumChannels"] * header["BitsPerSample"]//8

    # Define data to be saved
    left_channel, right_channel = data["data"][::2], data["data"][1::2]
    cod_data = {
        "SubChunk2ID": b"data",
        "SubChunk2Size": 0,
        "data": []
    }

    semi_sum_bytes = [int.to_bytes(((left_sample + right_sample) // 2), length=2, byteorder="little", signed=True) for left_sample, right_sample in zip(left_channel, right_channel)]
    semi_diff_bytes = [int.to_bytes(((left_sample - right_sample) // 2), length=2,byteorder="little", signed=True) for left_sample, right_sample in zip(left_channel, right_channel)]
    cod_data["data"] = [int.from_bytes((sum_sample + diff_sample), byteorder="little", signed=True) for sum_sample, diff_sample in zip(semi_sum_bytes, semi_diff_bytes)]
    cod_data["SubChunk2Size"] = len(cod_data["data"]) * header["NumChannels"] * header["BitsPerSample"]//8

    write_wave(ficCod, header, cod_data)
```

##### Código de `decEstereo()`
```p
def decEstereo(ficCod: str, ficEste: str):
    """
    Decodifies a mono audio file into an estereo audio file. The decodification is done by:
    - Extracting the semi-sum and semi-difference of the codified sample.
    - Converting the semi-sum and semi-difference into 16-bit samples.
    - Calculating the left and right channels from the semi-sum and semi-difference samples.
    
    Args:
        ficCod: codified audio file
        ficEste: estereo audio file
        
    Raises:
        ValueError: if the file is not 32-bit or mono
    """
    header, cod_data = read_wave(ficCod)
    if header["NumChannels"] != 1:
        raise ValueError(f"File '{ficCod}' is not a mono file")
    if header["BitsPerSample"] != 32:
        raise ValueError(f"File '{ficCod}' is not a 32-bit file")
    
    # Decodified file header
    header["NumChannels"] = 2
    header["BitsPerSample"] = 16
    header["ByteRate"] = header["SampleRate"] * header["NumChannels"] * header["BitsPerSample"]//8
    header["BlockAlign"] = header["NumChannels"] * header["BitsPerSample"]//8

    # Define data to be saved
    data = {
        "SubChunk2ID": b"data",
        "SubChunk2Size": 0,
        "data": []
    }

    semi_sum = [int.from_bytes(int.to_bytes((sample>>16) & 0xFFFF, 2, "little"), "little", signed=True) for sample in cod_data["data"]]
    semi_diff =[int.from_bytes(int.to_bytes(sample & 0xFFFF, 2, "little"), "little", signed=True) for sample in cod_data["data"]]
    left_channel = [(sum_sample + diff_sample) for sum_sample, diff_sample in zip(semi_sum, semi_diff)]
    right_channel = [(sum_sample - diff_sample) for sum_sample, diff_sample in zip(semi_sum, semi_diff)]
    
    data["data"] = left_channel + right_channel
    data["data"][::2] = left_channel
    data["data"][1::2] = right_channel

    data["SubChunk2Size"] = len(data["data"]) * header["NumChannels"] * header["BitsPerSample"]//8

    write_wave(ficEste, header, data)
```
#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
