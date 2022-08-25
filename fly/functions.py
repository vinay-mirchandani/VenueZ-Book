def handle_uploaded_file(f):
    print("-----",f.name)
    with open('fly/static/image/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
