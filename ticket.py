from uuid import uuid4
from copy import deepcopy
import socket
import _thread
import time


ELECTION_NOT_STARTED = 0
ELECTION_STARTED = 1
ELECTION_FINISHED = 2
TIME_MINUTE = 60
TIME_HOUR = 3600
TIME_DAY = 86400

class Server:
  def __init__(self):
    self.__elections = {}
    self.__electionsUsers = []
    self.__users = []

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

    electionID = str(uuid4())
    election = {
      'name': name,
      'candidates': candidates,
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
    Returns the list of elections

    Returns:
    list: List of elections
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

