''' Module url: provide function(s) in support of getting web-based data
    into the needed information structures.

    version 2: trusts the http://forecast.weather.gov/ security certificate
    version 3: added strings and lines access
    version 4: fixed bug in converting negative integers in get_dataset()
    version 5: fixed bug in get_strings() and get_lines()
    version 6: adds image support
    version 7: adds dictionary support
    version 8: fixed bug in dictionary support for numeric words
'''
import csv

CSV_SEPARATOR = ','

# need help to get web and image data
import urllib.request, io


def get_text(link):
    ''' returns the contents of the web resource indicated by parameter link
    '''

    # version 2 change to function ###########################################
    if ((link.find('http://forecast.weather.gov/') == 0) or (link.find('https://forecast.weather.gov/') == 0)):

        # trust the website
        import os, ssl
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = ssl._create_unverified_context

    stream = urllib.request.urlopen(link)  # connect to resource stream

    content = stream.read()  # read stream to gets its contents

    text = content.decode('UTF-8')  # decode contents to get text

    return text


def get_dataset_as_rows_of_strings(link):
    ''' returns the contents of the web resource indicated by parameter
        link as a list of lists of strings
    '''

    text = get_text(link)

    # turn text into list of lines
    text = text.strip()  # strip surrounding whitespace of the text
    lines = text.split('\n')  # split text into lines

    # turn lines into a dataset
    dataset = []  # initialize dataset to be empty

    for line in lines:  # consider each row one-by-one
        # clean up the line
        line = line.strip()  # strip surrounding whitespace of the line

        # split line into a list of cells
        cells = line.split(CSV_SEPARATOR)  # split row into a list of cells

        # put cleaned up cells into new row of dataset

        row = []  # initialize row to be empty

        for cell in cells:  # consider each cell in the row one-by-one
            # clean up the cell
            cell = cell.strip()  # strip surrounding whitespace of the cell

            # add the cell to end of the row
            row.append(cell)

        # add the row to the end of the dataset
        dataset.append(row)

    # return the dataset
    return dataset


def get_dataset(link):
    ''' returns the contents of the web resource indicated by parameter link as
        a list of lists. The elements of the lists will be converted to int,
        float, or bool as appropriate
    '''

    dataset = get_dataset_as_rows_of_strings(link)  # get dataset with cells as strings

    # put cell contents into proper form
    nbr_rows = len(dataset)  # get number of rows we are dealing with

    for r in range(0, nbr_rows):  # consider each row in the dataset one-by-one

        row = dataset[r]  # processing r-th row of the dataset
        nbr_columns = len(row)  # get the number of cells we are dealing with

        for c in range(0, nbr_columns):  # consider each cell in the row one-by-one
            cell = row[c]  # processing c-th cell of the row

            if (cell.isnumeric()):  # determine if cell is a postive integer
                cell = int(cell)  # if it is, cast to int

            elif ((cell[0] == '-') and (cell[1:].isnumeric())):  # version 4 check
                # determine if cell is a negative integer
                cell = - int(cell[1:])  # if it is, cast the numeric part and negate

            elif (cell.capitalize() == 'True'):  # otherwise, determine if cell is logical true
                cell = True  # if it is, make it True

            elif (cell.capitalize() == 'False'):  # otherwise, determine if cell is logical false
                cell = False  # # if it is, make it False
            else:
                try:  # see if cell can be converted to decimal
                    cell = float(cell)  # if so, update it
                except:
                    pass
            row[c] = cell  # set c-th cell in row to its valued form

        dataset[r] = row  # set r-th row to its valued form

    # return the properly-valued dataset
    return dataset


###  Version 2 addition

def get_lines(link):
    ''' returns the lines of text stored at the web resource indicated by
        parameter link
    '''

    # get the contents of the page
    data = get_text(link)

    # strip the data of surrounding whitespace
    data = data.strip()

    # split data into lines
    lines = data.split('\n')

    # return what they asked for
    return lines


def get_strings(link):
    ''' returns the strings stored at the web resource indicated by
        parameter link
    '''

    # get the contents of the page
    data = get_text(link)

    # split data into strings
    strings = data.split()

    # return what they asked for

    return strings


def get_dictionary(link):
    ''' return the contents of the page indicated by parameter link as
        a dictionary
    '''
    dataset = get_dataset_as_rows_of_strings(link)  # version 8

    # initialize the dictionary
    dictionary = {}

    # accumulate the dictionary entries from the sheet
    for entry in dataset:
        key, value = entry
        dictionary[key] = value

    # return what they asked for
    return dictionary


from PIL import Image

# needed for web support
import urllib.request, io


# process image acquistion and display

def get_web_image(link):
    ''' Return image at web resource indicated by link
    '''

    # get access to module Image
    from PIL import Image
    ''' Returns a pil image of the image named by link '''

    # get a connection to the web resource name by link
    stream = urllib.request.urlopen(link)

    # get the conents of the web resource
    data = stream.read()

    # convert the data to bytes
    pixels = io.BytesIO(data)

    # get the image represented by the bytes
    image = Image.open(pixels)

    # convert the image to RGB format
    image = image.convert('RGB')

    # hand back the image
    return image


def get_selfie(id):
    ''' Returns a selfie of the indicated CS 1112 id
    '''

    REPOSITORY = 'http://www.cs.virginia.edu/~cs1112/people/'

    link = REPOSITORY + id + '/selfie.jpg'

    return get_web_image(link)


def get_image(source):
    ''' Returns a image from online or local source or an existing Image
    '''
    try:
        if (str(type(source)) == "<class 'PIL.Image.Image'>"):
            # check to if source is an existing Image
            image = source
        elif ('http://' == source[0: 7].lower()):
            # look at the initial characters of source to see if its on the web
            image = get_web_image(source)
        elif ('https://' == source[0: 8].lower()):
            # look at the initial characters of source to see if its on the web
            image = get_web_image(source)
        else:
            # initial characters indicate the image is a local file
            image = Image.open(source)
    except:
        image = None

    return image.copy()


def open_and_convert_csv(file_name):
    with open(file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        dataset = []
        for row in readCSV:
            dataset.append(row)
        nbr_rows = len(dataset)  # get number of rows we are dealing with

        for r in range(0, nbr_rows):  # consider each row in the dataset one-by-one

            row = dataset[r]  # processing r-th row of the dataset
            nbr_columns = len(row)  # get the number of cells we are dealing with

            for c in range(0, nbr_columns):  # consider each cell in the row one-by-one
                cell = row[c]  # processing c-th cell of the row

                if (cell.isnumeric()):  # determine if cell is a postive integer
                    cell = int(cell)  # if it is, cast to int

                elif ((cell[0] == '-') and (cell[1:].isnumeric())):  # version 4 check
                    # determine if cell is a negative integer
                    cell = - int(cell[1:])  # if it is, cast the numeric part and negate

                elif (cell.capitalize() == 'True'):  # otherwise, determine if cell is logical true
                    cell = True  # if it is, make it True

                elif (cell.capitalize() == 'False'):  # otherwise, determine if cell is logical false
                    cell = False  # # if it is, make it False
                else:
                    try:  # see if cell can be converted to decimal
                        cell = float(cell)  # if so, update it
                    except:
                        pass
                row[c] = cell  # set c-th cell in row to its valued form

            dataset[r] = row  # set r-th row to its valued form

        # return the properly-valued dataset
        return dataset
def list_to_csv(list_var,file_name):
    with open(file_name, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows([list_var])
    csvFile.close()

def dataset_to_csv(list_var,file_name):
    with open(file_name, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(list_var)
    csvFile.close()