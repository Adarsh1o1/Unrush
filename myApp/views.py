from django.shortcuts import render,get_object_or_404,redirect
from django.http import response,HttpResponse,Http404,HttpResponseForbidden
from django.template import loader
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import files,Folder
from .encryption_util import *
# import os,zipfile
# from mysite.settings import BASE_DIR

def home(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        folders = Folder.objects.filter(user=user,parent_folder=None)
        if request.method == 'POST':
            folder_name = request.POST['folder_name']
            parent_folder_id = request.POST.get('parent_folder_id')
            parent_folder = None
            if parent_folder_id:
                parent_folder = get_object_or_404(Folder, id=parent_folder_id)
            Folder.objects.create(user=request.user, name=folder_name, parent_folder=parent_folder)
        
        return render(request, 'myfiles.html', {'folders':folders, 'files_by':user})
    
    print(request.user.id)
    encrypted_userid = encrypt(request.user.id)
    return render(request,'index.html',{'id':encrypted_userid })

def about(request):
    encrypted_userid = encrypt(request.user.id)
    return render(request, 'about.html',{'id':encrypted_userid })

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['password2']
        if password==confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request,'this Email is already in use')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'username already exists')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request,"passwords didn't match")
            return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('myfiles',pk=encrypt(request.user.id))
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('login')

    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='login')
def uploading(request,pk):
        if request.method=="POST":
            aa=request.POST,request.FILES
            if aa:
                client_file=request.FILES.getlist('file') 
                for fil in client_file:
                            folder = get_object_or_404(Folder, id=pk)
                            new_file=files(user=request.user,file=fil, folder=folder)
                            new_file.save()

                return redirect('folder_contents',folder_id=pk)
        return render(request, 'uploading.html')

@login_required(login_url='login')
def folders(request,pk):
    pk=decrypt(pk)
    user = get_object_or_404(User, id=pk)
    folders = Folder.objects.filter(user=user,parent_folder=None)
    if request.method == 'POST':
        folder_name = request.POST['folder_name']
        parent_folder_id = request.POST.get('parent_folder_id')
        parent_folder = None
        if parent_folder_id:
            parent_folder = get_object_or_404(Folder, id=parent_folder_id)
        Folder.objects.create(user=request.user, name=folder_name, parent_folder=parent_folder)
        
    return render(request, 'myfiles.html', {'folders':folders, 'files_by':user})

@login_required(login_url='login')
def folder_contents(request, folder_id):
    encrypted_userid = encrypt(request.user.id)
    folders = Folder.objects.filter(user=request.user,parent_folder=None)
    # folder = get_object_or_404(Folder, id=folder_id) 
    try:
        folder = Folder.objects.get(id=folder_id)
    except Folder.DoesNotExist:
        return HttpResponse('not found', status=404)

    if folder.user != request.user:
        return HttpResponseForbidden('You do not have persmission to acces this folder')
    else:
        subfolders = Folder.objects.filter(parent_folder=folder) 
        filess = files.objects.filter(folder=folder)
        if request.method == 'POST':
            folder_name = request.POST['folder_name']
            parent_folder_id = request.POST.get('parent_folder_id')
            parent_folder = None
            if parent_folder_id:
                parent_folder = get_object_or_404(Folder, id=parent_folder_id)
            Folder.objects.create(user=request.user, name=folder_name, parent_folder=parent_folder)
            if parent_folder_id:
                return redirect('folder_contents',folder_id=parent_folder_id)

        return render(request, 'folder_contents.html', {'folders':folders,'folder': folder, 'subfolders': subfolders, 'files': filess, 'id':encrypted_userid,})

def delete_file(request,pk):
    fil=get_object_or_404(files, id=pk)
    context={
        'file_name': fil
    }
    if  request.user != fil.user:
        return HttpResponse("can't proceed unauthorized access")
    else:
        fil.delete()
    
    return render(request,'delete.html', context)

def delete_folder(request,pk):
    encrypted_userid = encrypt(request.user.id)
    folder=get_object_or_404(Folder, id=pk)
    if  request.user != folder.user:
        return HttpResponse("can't proceed unauthorized access")
    else:
        folder.delete()
    return render(request, 'delete_folder.html', {'folder':folder,'id':encrypted_userid})

# def download_folder_zip(request):
#     folder = get_object_or_404(Folder, id=32)
#     subfolders=Folder.objects.filter(parent_folder=folder)
#     file=files.objects.filter(folder=folder)
#     zip_file_path = f'mysite\media\{folder}.zip'
#     # for fil in file:
#     #     print(fil)
#     with zipfile.ZipFile(zip_file_path ,mode='w') as zipf:
#         for x in file:
#             print(x)
#             zipf.write(f'mysite\media\{x}')
#     return render(request,'download_folder_zip.html')

def download_file(request,file_name):
    file=get_object_or_404(files, file=file_name)
    return render(request, 'download.html', {'file':file})

