import os

process = os.popen('sudo clockdiff -o 127.0.0.1')
output = process.read()
print(output)
process.close()
