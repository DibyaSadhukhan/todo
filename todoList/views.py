import requests
import json
from django.shortcuts import render
import urllib.request
class access:
  def __init__(self):
    token=[]
    for line in urllib.request.urlopen('https://drive.google.com/uc?export=veiw&id=14hvM3Lg3bhM66ljlMxsyz6E9IL1Gz7GX'):
      token.append(line.decode('utf-8').strip()[1:-1])

    self.personal_access_token=token[0]
    self.HEADERS={'Authorization':f'Bearer {self.personal_access_token}'}
    self.workspace_gid=token[1]
    self.user_gid=token[2]

# Create your views here.
def get_user_tasks(user_gid,workspace_gid,HEADERS):
  response = requests.get(f'https://app.asana.com/api/1.0/tasks?workspace={workspace_gid}&assignee={user_gid}&opt_fields=gid,name,completed,notes,due_on,assignee', headers=HEADERS)
  return response.json()
def update_task(gid,data,HEADERS):
  response = requests.put(f"https://app.asana.com/api/1.0/tasks/{gid}", data=data, headers=HEADERS)
  if response.ok:
    return "Updated "
  else:
    return "Encountered error in "
def delete_task(gid,HEADERS):
  response = requests.delete(f"https://app.asana.com/api/1.0/tasks/{gid}", headers=HEADERS) 
  if response.ok:
    return "Deleted"
  else:
    return "error in deletion"
  
def create_task(user_gid,data,workspace_gid,HEADERS):
  response = requests.post(f"https://app.asana.com/api/1.0/tasks?workspace={workspace_gid}&assignee={user_gid}",data=data, headers=HEADERS)
  if response.ok:
    return "done"
  else:
    return "error in creation"
def Todo(request):
  ob=access()
  if request.POST.get('Delete'):
    message=delete_task(request.POST.get('Delete'),ob.HEADERS)
  elif request.POST.get('Statusinc'):
    message=update_task(request.POST.get('Statusinc'),{'completed':True},ob.HEADERS)
  elif request.POST.get('Statuscomp'):
    message=update_task(request.POST.get('Statuscomp'),{'completed':False},ob.HEADERS)
  elif request.POST.get('UserCreatingtask'):
    message=create_task(ob.user_gid,{'name':request.POST.get('add_task_name'),'due_on':request.POST.get('add_task_due'),'notes':request.POST.get('add_task_notes'),'completed':False},ob.workspace_gid,ob.HEADERS)
  elif request.POST.get('Modifyingtask'):
    message=update_task(request.POST.get('Modifyingtask'),{'name':request.POST.get('mod_task_name'),'due_on':request.POST.get('mod_task_due'),'notes':request.POST.get('mod_task_notes'),'completed':False},ob.HEADERS)
  else:
    message=""
  print(request.POST)
  print(message)
  data=get_user_tasks(ob.user_gid,ob.workspace_gid,ob.HEADERS) 
  context={'data':data.get('data'),'notification':message}
  return render(request, 'index.html',context)

