import certifi

cafile = certifi.where()
with open("Additionals/certificate.pem", "rb") as infile:
    customca = infile.read()

with open(cafile, "ab") as outfile:
    outfile.write(customca)

print("cert successful added to python!")
