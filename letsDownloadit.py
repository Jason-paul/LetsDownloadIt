# Muhammad Momin
# Jason Paul
import downloadfile as d
def letsDownloadIt():
    # ask for the user if they want to see the history.
    # if yes then show the history from the sqlite. 
    url = input('Enter the URL of youtube Video: ').replace(' ','')
    if url == '':
        url='None'
    choice = input('To download video press \'v\'\tTo download audio press \'a\'\tTo see history press \'h\': ')

    d.__main__(url,choice)


letsDownloadIt()