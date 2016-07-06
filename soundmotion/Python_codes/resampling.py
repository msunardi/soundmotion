#--- Resampling

def resample(data, samplerate):
	#new_data = []
	#for n in range(0, len(data), samplerate):
	#	new_data.append(data[n])
	new_data = [data[n] for n in range(0, len(data), samplerate)]
	return new_data


# === TEST
"""a = range(2, 50)
new_a = resample(a, 4)

print "a = ", a, " length = ", len(a)
print "new_a = ", new_a, "length = ", len(new_a)
"""
