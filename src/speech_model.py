import speech_commands as sp
from ubinascii import a2b_base64, b2a_base64

data = a2b_base64('AwgJAQr+1f+9/Kzx2/zulvL46NomvhHQ8/7txOi3tvbO9Zbl1Q3jvwHIpSIm/uvq/wQB2yrlB+zqv+Pj5wrnNTD3GiX6J8nuwP3qEuWz8NPV1t22G9cc4P3pEri9yK/zouOf6dQD8N8x5dcWOgfZEztAIt4bzBHaBNTy/Ofx+g8UE+5B9QzFHLjdwfvz7wfR9s/43wS5AezJBw3s58jB16nVvTz6DenXF/PXMBkT6thBJgTALQPtBvzdBiEA5fQqJAADKvj2ww3B66kX+wvuxM3DAusAzvz3DfgTy9XLBiWz2NwWAvUvyAHv6voRDNbIMSIGCyYl/AYSAgsSDu8IHwv9ACP7Fdr7tOa+Eh7x09XYr/jkNA4f4PnVNun20vkJyNjY+/L0RhkzIeUfExwB4DcL2xMwLQvy6/kOJhu74CPgKi8aICWuvtLw2Bws9t/qDM4Q6vDzIRvo4yzyHssE8eHH7gm+CUkQ8RryBP0W9N1FC7MYJRL97Q/6FgsKsuLl6gsmHg0m7PC/+eMRGwTi5BHRLxPLBgf//Mw84RDc5d/8ELYMvv9B/+sj7vfu+93iIkHuAQ4eAOMe+/Er+toE4ALvJSAjG/PBwvTe/UAU7RXj1TkA4a0+F7X4NOMNoiTt/uTCI/QMRgztAOn2/NHe89xB5/TvKdMV7BUHDCgL+fX86zUPMh3E89zg4QMsMtnT4rhM8e3KKA3iyGD4+8b8GvXv1Dzu+DUF1fr+9g+j3ef1K9/s7QnuIQBGEuT65jnkzwomEO/jyrrwK6LNuvrnHhAkKt/x59a9xz7vzsMlPN/iEDLlIwerx/kSzdAZ9SAdytT/7d7r1uT2S/rzDjYoC/nR6wcQ0MfT8yXHxNEV5gsbRPD6zfbpu7ke17vmHTa+5REuAgPhKsDG3ZXR9fv0D8zJ2QTk8cPN1Eza9RLlC+371yPm3cnx/8woG8b2FuYa/gsWzq308eHfLue+IxM5xdgOJwYH1hPn8du5uPzkE/nPydvn9B/ZsbwwAQwTASAP6tUH9tmy7uHEExzL6xXbJhgz9Qrj+QYA5SznsvEoHf7i7h07B+QNzOLh2trz4APkpdzXAcce3bu6KQUBKh4P88X/+NXxvgLc0A0T2PEhAhAWGOYtyQIT6NQx9sfXN/UYzQUZFBPRCADg0ffM6sII9PP88hbSJNsBxTAQsPAyBd6u8Abn5tP+BPcGKOb3BS/8Cjj07dYEFSb0G/QPsyQGFOr9KPkcvhTq89rw8hGx9frt7gb1uDnWG75HBNrlGC3r6vYW8QXp2d4H/QDS3hwAFer8BPnI/BUhxBUBN8L2/Az04CYH9dT5Cf0JDvUTqQEL1wbr+9cluyzZIO7c5Po3AgSxGf3TCwjv49wNzPUF/TLU/xMW0dL5KgsW4Bjf8wTr5dAVBOftLv3x8hz5HeAWIeLXGunEGsVM6Q3uzMgANPD/swT/1d3v39jW2eLZzRT96OIJFM0C6w77DMby0tXw3dLY+fnlvBcQ19/jABL49fPprAvJHRDEMfH+6cy3xgEE/scRxN8oRBkc5Fc1UfIPGvzp3R3ROAw1KsIhQk7uDgZD6wUq5yNJTQIaTAvG7BDvKzTdPNgrDh4H6Q4z+9P+sbwIL80cGikPTNQ7Dy4TGCL+1fQ4MBLgRjPqGTon5Pc8TRTvAQcf/S0YFWAs8ggGCegN9xTjHyITJuIs8wQH/uTUEALzEBZK9FD1ACoeBRrwCe7cLTMoFi5I7AM0HvIIJUUcANfzEPQ++Rk2CQAF9Bnm7B4+1v0tOUf7AuPwCN3X1wHh7iYlOvk1AvwGGPgUBwz/ASMSI+r/Be3pTiTr5PUqEP7q4irVNw0PDhr6GhAe9v8kBOPHIjEN9u4EzgYHxwcM/w4CMCoRUvv7BhkC/QAR8w4PB//pJgTz2yEV8ALzSREBAgMe6Q79IDMyCPYfJOT9JeTg1wwMMdD4Igj25uYd7efm/wIZJjnk/Prp1+r59uwJHTTq3NgLAMUMD/oOHQEd2PwfMbPpCeghLvYVARPrCxAN7a/+9hfM5/ERDeAbI+fP/wnyMgMHBh4R9eoY7BMSz/ov+M/zFB/Q+iQJLfz7DBTYKQfd0CMJFgjnNx8A8eAO7hHjE/E36eoB/BzeDP4q0fvr6hobOBQALAP6GN47FJ8CKj/iwxT+tiDwLQj6ESL+2RwCrfYj9QkD6TUA7wbnCAwk0DDmK9z7IQgh2zAQTOQP6BosL0w0QkTm3g4GETW6ICUX0fEYC7wPLEbw/wIrMKsjBr70OuEeCdsvH/z1/zEjA+ZZ3wXf5UtBJu3uHSzTBBWfz18=')
sp.init(data)
labels = ["lumus","nox","[OTHER]"]
feature = bytearray(732)

def predict(audio):
    result = sp.predict(audio, 0, 0)
    return (labels[result // 1000], result % 1000)

def snapshot():
    global feature
    sp.export_mfcc(feature)

def save(label):
    with open('samples.txt', 'ab') as f:
        f.write(b'{"label": "')
        f.write(label.encode())
        f.write(b'", "mfcc": "')
        f.write(b2a_base64(feature)[:-1])
        f.write(b'"},\n')
