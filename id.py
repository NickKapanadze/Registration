import uuid

print(str(uuid.uuid4().fields[-1])[:12])

print(type(uuid.uuid4().fields[-1]))
print(type(str((uuid.uuid4().fields[-1]))[:12]))
