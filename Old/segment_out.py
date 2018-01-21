def search(IJout, _split="[DEBUG]", tag="loc = ["):
    sections = IJout.split(_split)
    for section in sections:
        if tag in section:
            return section

if __name__=='__main__':
    imagej_out = input()
    locations = search(imagej_out)
