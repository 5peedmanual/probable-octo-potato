def write_to_file(name, data, encoding):
	try:
    	text_file = open(name, "w")
	except IOError as error:
		print("[!!] Error opening file " + str(error))
		return -1
	
    if enconding == 'utf-8':
		try:
        	text_file.write(data.encode('utf-8'))
		except IOError as error:
			print("[!!] Error writing to file " + str(error))
			return -1
			
    elif encoding == 'string':
		try:
        	text_file.write(str(data))
		except IOError as error:
			print("[!!] Error writing to file " + str(error))
			return -1
    
	text_file.close()

	
	
