from latest import Latest

if __name__ == "__main__":
    l = Latest("youtube")
    dwn = l.latest_version()
    l.download(dwn)