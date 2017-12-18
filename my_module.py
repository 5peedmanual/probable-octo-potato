def write_to_file(name, data, num):
    text_file = open(name, "w")
    if num == 1:
        text_file.write(data.encode('utf-8'))
    elif num == 2:
        text_file.write(str(data))
    text_file.close()
