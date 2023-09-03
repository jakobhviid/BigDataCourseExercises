from hdfs import InsecureClient

# Create an insecure client that works when HDFS has security turned off
client = InsecureClient('http://namenode:9870', user='root')

first_line = ''

# Reading a file, using a delimiter makes it return a list
with client.read('/alice-in-wonderland.txt', encoding='utf-8', delimiter='\n') as reader:
  for line in reader:
    print(line)
    first_line = line
    # Only first line is interesting for now
    break
    
# One line writing to a file
# client.write('/write2.txt', first_line, encoding='utf-8', overwrite=True)

# Multi line writing
with client.write('/write.txt', encoding='utf-8', overwrite=True) as writer:
    writer.write(first_line)
    writer.write('\n')
    writer.write(first_line)
    writer.write('\n')