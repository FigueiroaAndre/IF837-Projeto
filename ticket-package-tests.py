import pytest
import ticket
import json

package = None
TEST_ID = '111.111.111-11'
TEST_TICKET = 'TESTICKET'
TEST_CMD = 1
TEST_DATA = json.dumps({'message': 'hello world'})


def setup_function():
  global package
  package = ticket.Package(TEST_ID,TEST_TICKET,TEST_CMD,TEST_DATA)

def test_constructor_CreatePackageSpecifyingEachField():
  assert package.content['id'] == TEST_ID, 'Package ID does not match'
  assert package.content['ticket'] == TEST_TICKET, 'Package Ticket does not match'
  assert package.content['cmd'] == TEST_CMD, 'Package Cmd does not match'
  assert package.content['data'] == TEST_DATA, 'Package Data does not match'

def test_constructor_CreatePackageSpecifyingADumpedPackage():
  dumpedPackage = package.dump()
  package2 = ticket.Package(dumpedPackage=dumpedPackage)
  assert package2.content['id'] == TEST_ID, 'Package ID does not match'
  assert package2.content['ticket'] == TEST_TICKET, 'Package Ticket does not match'
  assert package2.content['cmd'] == TEST_CMD, 'Package Cmd does not match'
  assert package2.content['data'] == TEST_DATA, 'Package Data does not match'
