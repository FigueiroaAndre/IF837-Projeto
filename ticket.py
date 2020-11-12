from uuid import uuid4
from copy import deepcopy
from random import randrange #TODO: Remove when cryptography implementation be ready
import socket
import _thread
import time


ELECTION_NOT_STARTED = 0
ELECTION_STARTED = 1
ELECTION_FINISHED = 2
TIME_MINUTE = 60
TIME_HOUR = 3600
TIME_DAY = 86400

class SecurityClass:
  def keyGenerator(self):
    """
    Generate a random key for encrypt and decrypt data

    Returns:
    str: A random key
    """
    #TODO: Update when the cryptography implementation be ready
    key = 1 + randrange(9)
    return key

  def encrypt(self, plaintext, key):
    """
    Encrypt a message

    Parameters:
    plaintext (str): Message to be encrypted
    key (str): Key for encrypt the message

    Returns:
    str: Encrypted message
    """
    ciphertext = ''
    for char in plaintext:
      cipherchar = chr(ord(char) + key)
      ciphertext = ciphertext + cipherchar
    return ciphertext

  def decrypt(self, ciphertext, key):
    """
    Decrypt a ciphertext

    Parameters:
    ciphertext (str): Ciphertext to be decrypted
    key (str): Key for decrypt the message

    Returns:
    str: Encrypted message
    """
    plaintext = ''
    for char in ciphertext:
      plainchar = chr(ord(char) - key)
      plaintext = plaintext + plainchar
    return plaintext


class Server(SecurityClass):
  def __init__(self):
    self.__elections = {}
    self.__electionsUsersLink = []
    self.__users = {}

  def createElection(self, name, candidates, duration=TIME_MINUTE, maxVotes=None):
    """
    Create an election and returns it's ID

    Parameters:
    name  (str): Name of the election
    candidates (list of str): The list of candidates
    duration (int): Duration of the election in seconds, defaults to 1 minute
    maxVotes (int): Max number of votes, defaults to None (unlimited)

    Returns:
    str: ID of the created Election
    """
    if type(name) is not str:
      raise TypeError('Arg name must be a string')
    if type(candidates) is not list:
      raise TypeError('Arg candidates must be a list')
    if len(candidates) < 2:
      raise Exception('An election must have at least 2 candidates')
    if not isinstance(duration,int):
      raise TypeError('Arg duration must be an int')
    if not (maxVotes is None or isinstance(maxVotes,int)):
      raise TypeError('Arg maxVotes must be int or None')
    for candidate in candidates:
      if type(candidate) is not str:
        raise TypeError('All elements of candidates list must be a string')
      if len(candidate) == 0:
        raise Exception('Candidate cannot be an empty string')

    candidateSet = set(candidates)
    if (len(candidates) != len(candidateSet)):
      raise Exception('There cannot be a duplicated candidate')

    votes = {}
    for candidate in candidates:
      votes[candidate] = 0

    electionID = str(uuid4())
    election = {
      'name': name,
      'candidates': candidates,
      'votes': votes,
      'total': 0,
      'status': ELECTION_NOT_STARTED,
      'published': False,
      'config': {
        'duration': duration,
        'maxVotes': maxVotes
      }
    }
    self.__elections[electionID] = election
    return electionID


  def getElections(self):
    """
    Returns an object with info of elections

    Returns:
    Dict: Dictionary of Elections
    """
    elections = deepcopy(self.__elections)
    return elections


  def electionExists(self, electionID):
    """
    Return if election exists or not

    Parameters:
    electionID (str): Election ID
    """
    if type(electionID) is not str:
      raise TypeError('Arg electionID must be a string')

    try:
      self.__elections[electionID]
      return True
    except:
      return False


  def getElection(self, electionID):
    """
    Returns the election of specified id

    Parameters:
    electionID (str): Election ID

    Returns:
    obj: Election with specified id
    """
    if self.electionExists(electionID):
      selectedElection = deepcopy(self.__elections[electionID])
      return selectedElection
    else:
      raise Exception('Election not found')


  def configureElection(self, electionID, duration=None, maxVotes=None):
    """
    Configure duration and or maxVotes of an election, the election must not have started

    Parameters:
    electionID (str): Election ID
    duration (int): Duration of the election in seconds, defaults to None (unchanged)
    maxVotes (int): Max number of votes, defaults to None (unlimited)
    """
    if not (duration is None or isinstance(duration,int)):
      raise TypeError('Arg duration must be None or int')
    if not (maxVotes is None or isinstance(maxVotes,int)):
      raise TypeError('Arg maxVotes must be None or int')

    if self.electionExists(electionID):
      selectedElection = self.__elections[electionID]
      if selectedElection['status'] != ELECTION_NOT_STARTED:
        raise Exception('Election must not have started')
      if duration is not None:
        selectedElection['config']['duration'] = duration
      selectedElection['config']['maxVotes'] = maxVotes
    else:
      raise Exception('Election not found')


  def deleteElection(self, electionID):
    """
    Delete an Election that have not started or that have already finished

    Parameters:
    electionID (str): Election ID
    """
    electionData = self.getElection(electionID)
    if electionData['status'] == ELECTION_STARTED:
      raise Exception('Cannot delete an active election')
    else:
      del self.__elections[electionID]


  def startElection(self, electionID):
    """
    Start an unstarted election

    Parameters:
    electionID (str): Election ID
    """
    # if self.electionExists(electionID)
    electionData = self.getElection(electionID)

    if electionData['status'] == ELECTION_NOT_STARTED:
      self.__elections[electionID]['status'] = ELECTION_STARTED
    elif electionData['status'] == ELECTION_STARTED:
      raise Exception('It is not possible to start an election that have already been started')
    elif electionData['status'] == ELECTION_FINISHED:
      raise Exception('It is not possible to start a finished election')


  def getUsers(self):
    """
    Returns an object with info of users

    Returns:
    Dict: Dictionary of users
    """
    users = deepcopy(self.__users)
    return users


  def userExists(self, userID):
    """
    Return if user exists or not

    Parameters:
    userID (str): user ID
    """
    if type(userID) is not str:
      raise TypeError('Arg userID must be a string')

    try:
      self.__users[userID]
      return True
    except:
      return False


  def getUser(self, userID):
    """
    Returns the user of specified id

    Parameters:
    userID (str): user ID

    Returns:
    obj: user with specified id
    """
    if self.userExists(userID):
      selecteduser = deepcopy(self.__users[userID])
      return selecteduser
    else:
      raise Exception('User not found')


  def registerUser(self, name, customID=None):
    """
    Register an user into the system

    Parameters:
    name (str): Name of the user
    customID (str): uses an customID from the application to represents the userID, defaults to None (the protocol creates a uniqueID)

    Returns:
    str: ID of the registered User
    """
    if type(name) is not str:
      raise TypeError('Arg name must be a string')
    if not (type(customID) is str or customID is None):
      raise TypeError('Arg customID must be string or None')

    userID = ''
    if customID is None:
      userID = str(uuid4())
    else:
      userID = customID
      if self.userExists(customID):
        raise Exception(f'An user with id {customID} already Exists')

    user = {
      'name': name
    }
    self.__users[userID] = user
    return userID


  def getElectors(self, electionID):
    """
    Returns the electors of a specified election

    Parameters:
    electionID (str): Election ID

    Returns:
    list: list of userID subscribed to the specified election
    """
    if self.electionExists(electionID):
      userList = []
      for electionUserLink in self.__electionsUsersLink:
        if electionUserLink['election'] == electionID:
          userList.append(electionUserLink['user'])
      return userList
    else:
      raise Exception('Election not found')


  def subscribe(self, userID, electionID):
    """
    Subscribe an user into an election

    Parameters:
    userID (str): ID of the user
    electionID (str): ID of the election
    """
    if self.electionExists(electionID) and self.userExists(userID):
      if userID in self.getElectors(electionID):
        raise Exception('This user has already subscribed in this election')
      election = self.getElection(electionID)
      if election['status'] != ELECTION_NOT_STARTED:
        raise Exception('An user can only subscribe into an election that have not started.')

      electionUserLink = {
        'election': electionID,
        'user': userID,
        'ticket': self.generateTicket(),
        'voted': False
      }
      self.__electionsUsersLink.append(electionUserLink)
      #TODO: Complete me

  def generateTicket(self):
    """
    Generate a new Ticket

    Returns:
    str: Ticket
    """
    #TODO: Update when cryptography be ready
    randomKey = self.keyGenerator()
    randomValue = str(uuid4())
    ticket = self.encrypt(randomValue, randomKey)
    return ticket
