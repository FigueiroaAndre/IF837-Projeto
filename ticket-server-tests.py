import pytest
import ticket
from uuid import uuid4

ERROR_MESSAGE_INDEX = 0
server = None

def setup_function():
  global server
  server = ticket.Server()

def test_createElection_NameIsNotString():
  try:
    server.createElection(name=None, candidates=['c1','c2'])
    assert False, 'createElection did not raise an TypeError'
  except TypeError as err:
    assert err.args[ERROR_MESSAGE_INDEX] == 'Arg name must be a string'

def test_createElection_CandidatesIsNotList():
  try:
    server.createElection(name='election', candidates=None)
    assert False, 'createElection did not raise an TypeError'
  except TypeError as err:
    assert err.args[ERROR_MESSAGE_INDEX] == 'Arg candidates must be a list'

def test_createElection_OnlyOneValidCandidate():
  try:
    server.createElection(name='election', candidates=['c1'])
    assert False, 'createElection did not raise an Exception'
  except Exception as err:
    assert err.args[ERROR_MESSAGE_INDEX] == 'An election must have at least 2 candidates'

def test_createElection_DuplicatedCandidates():
  try:
    server.createElection(name='election', candidates=['c1','c1'])
    assert False, 'createElection did not raise an Exception'
  except Exception as err:
    assert err.args[ERROR_MESSAGE_INDEX] == 'There cannot be a duplicated candidate'

def test_createElection_ThereIsAnNonStringCandidate():
  try:
    server.createElection(name='election', candidates=['c2','c2',3])
    assert False, 'createElection did not raise a TypeError'
  except TypeError as err:
    assert err.args[ERROR_MESSAGE_INDEX] == 'All elements of candidates list must be a string'

def test_createElection_CandidateCannotBeAnEmptyString():
  try:
    server.createElection(name='election', candidates=['c1',''])
    assert False, 'createElection did not raise an Exception'
  except Exception as err:
    assert err.args[ERROR_MESSAGE_INDEX] == 'Candidate cannot be an empty string'

def test_createElection_DurationIsNotInt():
  try:
    server.createElection(name='election', candidates=['c1','c2'],duration='str')
    assert False, 'createElection did not raise an TypeError'
  except TypeError as err:
    assert err.args[ERROR_MESSAGE_INDEX] == 'Arg duration must be an int'

def test_createElection_MaxVotesIsNotIntNorNone():
  try:
    server.createElection(name='election', candidates=['c1','c2'],maxVotes='7')
    assert False, 'createElection did not raise an TypeError'
  except TypeError as err:
    assert err.args[ERROR_MESSAGE_INDEX] == 'Arg maxVotes must be int or None'

def test_createElection_ElectionsSuccessfullyCreated():
  elections = []
  elections.append({
    'name': 'election1',
    'candidates': ['E1c1','E1c2']
  })
  elections.append({
    'name': 'election2',
    'candidates': ['E2c1','E2c2']
  })
  for election in elections:
    election['id'] = server.createElection(election['name'], election['candidates'])

  electionsFromServer = server.getElections()
  for election in elections:
    electionFromServer = electionsFromServer[election['id']]
    assert electionFromServer['name'] == election['name'], 'Name of election does not match'
    assert electionFromServer['candidates'] == election['candidates'], 'Candidates of election does not match'
    assert electionFromServer['status'] == ticket.ELECTION_NOT_STARTED, f'The default value of field "status" should be {ticket.ELECTION_NOT_STARTED}'
    assert not electionFromServer['published'], 'The default value of field "published" should be False'
    assert electionFromServer['config']['duration'] == ticket.TIME_MINUTE, f'The default value of field "config.duration" should be {ticket.TIME_MINUTE}'
    assert electionFromServer['config']['maxVotes'] is None, f'The default value of field "config.maxVotes" should be None'

def test_electionExists_ElectionDoesNotExist():
  electionID = str(uuid4)
  assert not server.electionExists(electionID), 'Returned True even thought election did not exist'

def test_electionExists_ElectionExists():
  electionID = server.createElection('election',['c1','c2'])
  assert server.electionExists(electionID), 'Returned False even thought election exists'

def test_electionExists_ElectionIDMustBeString():
  try:
    server.electionExists(1)
    assert False, 'electionExists did not raise a TypeError'
  except TypeError as err:
    assert err.args[ERROR_MESSAGE_INDEX] == 'Arg electionID must be a string'

def test_getElection_ElectionDoestNotExist():
  electionID = str(uuid4)
  try:
    server.getElection(electionID)
    assert False, 'Should raise an Exception when election does not exist'
  except Exception as err:
    assert err.args[ERROR_MESSAGE_INDEX] == 'Election not found'

def test_getElection_ElectionIDMustBeString():
  try:
    server.getElection(1)
    assert False, 'getElection did not raise a TypeError'
  except TypeError as err:
    assert err.args[ERROR_MESSAGE_INDEX] == 'Arg electionID must be a string'

def test_getElection_TriesToChangeElectionFromOutsideTheClass():
  electionID = server.createElection('election',['c1','c2'],duration=100)
  election = server.getElection(electionID)
  election['config']['duration'] = 200
  unchangedElection = server.getElection(electionID)
  assert unchangedElection['config']['duration'] != election['config']['duration'], 'Should not be possible to change election from outside the class'

def test_getElections_TriesToChangeElectionsFromOutsideTheClass():
  server.createElection('election1',['E1c1','E1c2'],duration=100)
  server.createElection('election2',['E2c1','E2c2'],duration=100)
  elections = server.getElections()
  for electionID in elections:
    elections[electionID]['config']['duration'] = 200
  unchangedElections = server.getElections()
  assert unchangedElections != elections, 'Should not be possible to change elections from outside the class'

def test_configureElection_ModifiesConfigurationOfUnstartedElection():
  electionID = server.createElection('election',['c1','c2'])
  server.configureElection(electionID, ticket.TIME_DAY, 500)
  election = server.getElection(electionID)
  assert election['config']['duration'] == ticket.TIME_DAY, 'Election field "config.duration" does not match the configured value'
  assert election['config']['maxVotes'] == 500, 'Election field "config.maxVotes" does not match the configured value'

