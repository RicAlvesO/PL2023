import re

# Parse header of csv file
def parse_header(header):

    # Split header
    fields = re.split(r',', header.strip())
    max=len(fields)
    i=0

    # Parse each field
    while i <max:

        # If field is a list with min and max values get min from i+1
        if re.findall(r'\{', fields[i]) and not re.findall(r'\}', fields[i]):
            fields[i] = fields[i] + ',' + fields[i+1]
            fields[i+1]=''
        
        #clear /n
        fields[i] = fields[i].strip()
        obj=[]

        # If field is a list
        if re.findall(r'\{', fields[i]):

            # Get name of field
            obj.append(re.split(r'\{', fields[i])[0])
            
            rest = re.split(r'\{', fields[i])[1]
            
            # If list has max values get min and max else get only min
            if re.findall(r',', rest):
                obj.append(int(re.split(r'\,', rest)[0]))
                obj.append(int(re.split(r'\}',re.split(r',', rest)[1])[0]))
            else:
                obj.append(int(re.split(r'\}', rest)[0]))
            
            # If list has a complex field get it
            rest = re.split(r'\}', rest)[1]
            if re.findall(r'::', rest):
                obj.append(re.split(r'::', rest)[1])

            # Replace field with list
            fields[i] = obj
        else:

            # If field is simple put it in a list
            fields[i] = [fields[i]]
        i+=1

    # Remove empty fields
    fields = [x for x in fields if x != ['']]
    
    return fields

# Parse line according to header
def parse_line(line, fields):

    # Split line
    linef = re.split(r',', line.strip())

    # Parse Integers
    for x in range(len(linef)):
        if re.match('\d+',linef[x]):
            linef[x]=int(linef[x])
    dic={}
    at=0

    # Create dictionary with values
    for i in fields:

        # If simple field
        if len(i)==1:
            dic[i[0]]=linef[at]
            at+=1

        # If list
        else:

            # Get min and max values of list elements
            min=i[1]
            if len(i)==3 and re.match(r'\d+', str(i[2])):
                max=i[2]
                expr=None
            elif len(i)==3:
                expr=i[2]
                max=min
            elif len(i)==4:
                max=i[2]
                expr=i[3]
            else:
                max=min
                expr=None
            nat=0
            arr=[]

            # Get lists of values between min and max
            while nat < max:
                if nat<min:
                    arr.append(linef[at])
                else:
                    if linef[at] != '':
                        arr.append(linef[at])
                at+=1
                nat+=1

            # Calculate value if its a complex fields
            if expr:
                dic[i[0]]=calc(expr,arr)
            else:
                dic[i[0]]=arr
    return dic

# Calculate value of complex fields
def calc(expr, arr):
    if expr == 'sum':
        return sum(arr)
    elif expr == 'avg':
        return sum(arr)/len(arr)
    elif expr == 'min':
        return min(arr)
    elif expr == 'max':
        return max(arr)
    elif expr == 'count':
        return len(arr)
    else:
        return arr

# Parse csv file
def parse_file(file):
    with open(file, 'r') as f:

        # Get header and parse it
        header = f.readline()
        fields = parse_header(header)
        jdic=[]

        # Parse each line
        for line in f:
            jdic.append(parse_line(line, fields))
    
    # Return dictionary
    return jdic

# If file is run as a script
if __name__ == '__main__':

    # Import libraries
    import sys
    import json

    # Check if file is given
    if len(sys.argv) < 2:
        print('Usage: csv2json.py <csvfile>')
        sys.exit(1)
    
    # Parse csv file to json
    file = sys.argv[1]
    jdic = parse_file(file)

    # Write to json file
    newf=re.sub(r'\.csv$', '.json', file)
    with open(newf, 'w') as f:
        f.write(json.dumps(jdic, indent=4, ensure_ascii=False))