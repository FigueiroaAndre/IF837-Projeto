import ticket

server = ticket.Server()
eid = server.createElection('5',['bla','7'])
elec = server.getElection(eid)
print(elec)
print(server.configureElection(eid,duration=600,maxVotes=900))
elec = server.getElection(eid)
print(elec)