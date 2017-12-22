def write_to_file(name, data, encoding):
    text_file = open(name, "w")
    if enconding == 'utf-8':
        text_file.write(data.encode('utf-8'))
    elif encoding == 'string':
        text_file.write(str(data))
    text_file.close()
