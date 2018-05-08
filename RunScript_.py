#!/usr/bin/python3.6

# Ahmed Alotabibi
# 4/11/2018
# A class for extracting
# emails from the file content.
# Getters, file, directory logic and making json
# for each data needed in a file that is
# located inside a directory

from email.parser import Parser
import sys, os
import re
import json

maildir = "ermis-f"
json_file = "emails.json"

class Files():

    """A constructor to initialize the objects"""
    
    def __init__(self, fp):
        self.parsing = Parser().parse(fp)
        self.dirname = os.path.basename(os.path.dirname((fp.name)))
        self.filename = os.path.basename(fp.name)
        
    def _getDirname(self):
        """Get directory name"""
        return self.dirname
        
    def _getFilename(self):
        """Get file name"""
        return self.filename
    
    def _getEmail(text):
        """Get the email"""
        if not text:
            return None
        return text.strip()
    
    def _getName(text):
        """Get the name"""
        if not text:
            return None
        name =r'(.+) ?<.*>'
        match = re.match(name, text)
        return match.group(1).strip() if match\
                else text.strip()
    
    def _getMessage(self, Message):
        """Get the field of the email"""
        if not self.parsing[Message]:
            return [(None, None)]
        _first = self.parsing[Message].split(",")
        _second = self.parsing['X-' + Message].split(",")
        _listToFill = [(Files._getEmail(_first[i]),\
                    Files._getName(_second[i]))\
                   for i in range(len(_first))]
        return _listToFill
    
    def _getFrom(self):
        """ Get from in the form (From, X-From) """
        if not self.parsing['from']:
            return (None, None)
        return (self.parsing['From'],\
                Files._getName(self.parsing['X-From']))
    
    def _getDate(self):
        """Get the date """
        if not self.parsing['date']:
            return None
        return (self.parsing['Date'])

    def _getTo(self):
        """ Get to in the form [(To, X-To)] """
        to_list = self._getMessage("To")
        if to_list:
            return to_list
        else:
            return [(None, None)]
        
    def _getCc(self):
        """ Get CC in the form [(Cc, X-cc)] """
        cc = self._getMessage("Cc")
        if cc:
            return cc
        else:
            return [(None, None)]
        
    def _getBcc(self):
        """ Get Bcc in the form [(Bcc, X-bcc)] """
        bcc = self._getMessage("Bcc")
        if bcc:
            return bcc
        else:
            return [(None, None)]

def _dictWithInfo(data):
    """A dictoinary for the data to make json file"""
    """Zip to make lists for the names of people in both To & CC"""
    to, to_names = zip(*data._getTo())
    cc, cc_names = zip(*data._getCc())
    values = {
        'Foldername': data._getDirname(),
        'filename': data._getFilename(),
        'Date': data._getDate(),
        'from': data._getFrom()[0],
        'x-from': data._getFrom()[1],
        'to': to, 'x-to': to_names,
        'cc': cc, 'x-cc': cc_names}
    return values

def _generateJson(dirname, _emails, file=json_file):
    """Loop and write the data in a Json formatted"""
    email_dicts = [_dictWithInfo(email)
                   for email in _emails]
    with open(os.path.join(dirname, file), "w") as jsfile:
        json.dump(email_dicts, indent=3, fp=jsfile)

def _readEmail(email_, output, _emails):
    """Open the content and append the needed data"""
    with open(email_) as fp:
        email = Files(fp)
        _emails.append(email)
        return
    
def _WalkOverDir(dirname, output):
    """Walk over all the emails in the given directory
        and add the data to process in json format"""
    _emails = []
    for filename in os.listdir(dirname):
        email_ = os.path.join(dirname, filename)
        if not os.path.isfile(email_):
            continue
        _readEmail(email_, output, _emails)
        _generateJson(dirname, _emails)
        
def main():
    
    output = {}
    for dirname, suddirs, files in os.walk(maildir):
        print("Directory Name: " + dirname)
        _WalkOverDir(dirname, output)
        
if __name__ == "__main__":
    main()
