def handle_uploaded_file(f):
    with open('src/projectRoot/media/uploadtest.txt', 'a+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)