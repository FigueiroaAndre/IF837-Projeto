import pytest
import ticket

ERROR_MESSAGE_INDEX = 0

def test_stateMachine_ServerHappyPath():
  stateMachine = ticket.ProtocolStateMachineHandler('server')
  try:
    stateMachine.changeState(ticket.STATE_SERVER_WAIT_RECV_ELECTION_ID)
    stateMachine.changeState(ticket.STATE_SERVER_WAIT_RECV_VOTE)
    stateMachine.changeState(ticket.STATE_SERVER_WAIT_TCP_CLOSE)
    stateMachine.changeState(ticket.STATE_FINISHING)
  except:
    assert False, 'No error should have happenned'

def test_stateMachine_ClientHappyPath():
  stateMachine = ticket.ProtocolStateMachineHandler('client')
  try:
    stateMachine.changeState(ticket.STATE_CLIENT_SEND_ELECTION_ID)
    stateMachine.changeState(ticket.STATE_CLIENT_SEND_VOTE)
    stateMachine.changeState(ticket.STATE_FINISHING)
  except:
    assert False, 'No error should have happenned'