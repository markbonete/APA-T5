"""
Nombre y apellidos: Mark Bonete Ventura
En este archivo se encuentran las funciones necesarias para trabajar con archivos de audio del tipo WAVE.
Las funciones implementadas son:

- read_wave: Lee un archivo de audio WAVE y devuelve dos diccionarios, uno con el header y otro con los datos.
- write_wave: Escribe un archivo de audio WAVE con los datos y el header dados en formato de diccionario.
- estereo2mono: Convierte un archivo de audio estereo en mono. Se puede elegir el canal a convertir.
- mono2estereo: Convierte dos archivos de audio mono en uno estereo.
- codEstereo: Codifica un archivo de audio estereo.
- decEstereo: Decodifica un archivo de audio estereo.

"""
import struct as st

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