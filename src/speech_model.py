# import speech_commands as sp
# from ubinascii import a2b_base64, b2a_base64

# data = a2b_base64('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')
# sp.init(data)
# labels = ["lumus", "nox", "[OTHER]"]
# feature = bytearray(732)


def predict(audio):
    return ("lumus", 100)
    # return ("[OTHER]", 100)
    # result = sp.predict(audio, 0, 0)
    # return (labels[result // 1000], result % 1000)


def snapshot():
    global feature
    # sp.export_mfcc(feature)


def save(label):
    with open('samples.txt', 'ab') as f:
        f.write(b'{"label": "')
        f.write(label.encode())
        f.write(b'", "mfcc": "')
        # f.write(b2a_base64(feature)[:-1])
        f.write(b'"},\n')
